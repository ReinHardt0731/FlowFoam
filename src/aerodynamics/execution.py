from ._controller_common import *
from project_paths import default_workspace_case_dir, workspace_runtime_dir_for_case

def execution_stage_names():
    return ["surfaceFeatureExtract", "blockMesh", "snappyHexMesh", "checkMesh", "simpleFoam"]


class ExecutionMixin:
    def _execution_state(self):
        exe = self.openfoam.setdefault("execution", {})
        exe.setdefault("case_dir", "")
        exe.setdefault("status", "idle")
        exe.setdefault("active_stage", "none")
        exe.setdefault("last_run_started_at", "")
        exe.setdefault("last_run_finished_at", "")
        exe.setdefault("last_error", "")
        exe.setdefault("last_logs", {})
        exe.setdefault("results", {})
        return exe

    def _set_execution_controls_running(self, running):
        is_running = bool(running)
        for panel_name, panel in getattr(self, "panel_widgets", {}).items():
            if panel_name != "Solve":
                panel.setEnabled(not is_running)
        for widget_name in (
            "btn_pick_export_path",
            "input_export_path",
            "chk_write_scripts",
            "chk_surface_feature_extract",
            "btn_save_cfd_config",
            "btn_load_cfd_config",
            "btn_preview_files",
            "btn_generate_case",
            "btn_run_pipeline",
            "btn_run_domain_mesh",
            "btn_run_surface_features",
            "btn_run_snappy_mesh",
            "btn_run_checkmesh",
            "btn_run_solve",
            "btn_run_post",
            "btn_export_vtk",
            "btn_load_vtk",
            "cmb_vtk_mesh",
            "btn_ribbon_generate_case",
            "btn_ribbon_update_case",
            "btn_ribbon_run_selected",
            "btn_ribbon_run_pipeline",
            "btn_ribbon_run_domain_mesh",
            "btn_ribbon_run_surface_features",
            "btn_ribbon_run_snappy_mesh",
            "btn_ribbon_run_checkmesh",
            "btn_ribbon_run_solve",
            "btn_ribbon_run_post",
            "btn_ribbon_export_vtk",
            "btn_ribbon_load_vtk",
            "btn_ribbon_open_latest_log",
            "cmb_ribbon_solver",
            "cmb_ribbon_stage",
            "cmb_ribbon_vtk_target",
            "cmb_ribbon_result_field",
        ):
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.setEnabled(not is_running)
        if hasattr(self, "btn_cancel_run"):
            self.btn_cancel_run.setEnabled(is_running)
        if hasattr(self.ui, "btn_ribbon_stop_run"):
            self.ui.btn_ribbon_stop_run.setEnabled(is_running)

    def _append_run_log(self, text):
        msg = str(text)
        console_output = getattr(self, "console_output", None)
        if console_output is not None:
            console_output.appendPlainText(msg.rstrip("\n"))
            console_output.ensureCursorVisible()
        elif hasattr(self, "txt_run_log"):
            self.txt_run_log.appendPlainText(msg.rstrip("\n"))
            self.txt_run_log.ensureCursorVisible()
        log_file = getattr(self, "_of_log_file", None)
        if log_file is not None:
            log_file.write(msg)
            if not msg.endswith("\n"):
                log_file.write("\n")
            log_file.flush()
        if getattr(self, "_conv_dialog", None) is not None:
            self._conv_feed_log_text(msg)

    def _clear_run_log_output(self):
        if self.console_output is not None:
            self.console_output.clear()
        elif hasattr(self, "txt_run_log"):
            self.txt_run_log.clear()

    def clear_console_output(self):
        self._clear_run_log_output()

    def set_console_output(self, widget):
        self.console_output = widget

    def _execution_case_dir(self):
        exe = self._execution_state()
        case_dir = str(exe.get("case_dir") or "").strip()
        if not case_dir:
            case_dir = str(self.openfoam.get("export", {}).get("output_path", "")).strip()
        if not case_dir:
            case_dir = str(default_workspace_case_dir())
        return Path(case_dir)

    def _latest_log_path(self):
        exe = self._execution_state()
        last_logs = exe.get("last_logs", {}) if isinstance(exe.get("last_logs", {}), dict) else {}
        preferred = (
            "solve",
            "check_mesh",
            "snappy_mesh",
            "surface_features",
            "domain_mesh",
            "post",
            "vtk_export",
        )
        for key in preferred:
            log_path = str(last_logs.get(key, "")).strip()
            if log_path:
                path = Path(log_path)
                if path.is_file():
                    return path
        case_dir = self._execution_case_dir()
        candidates = sorted(case_dir.glob("log*.txt"), key=lambda item: item.stat().st_mtime if item.exists() else 0.0, reverse=True)
        return candidates[0] if candidates else None

    def open_case_folder(self):
        case_dir = self._execution_case_dir()
        if not case_dir.exists():
            QMessageBox.warning(self._dialog_parent(), "OpenFOAM Case", f"Case directory not found:\n{case_dir}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(case_dir)))

    def open_latest_log(self):
        log_path = self._latest_log_path()
        if log_path is None:
            QMessageBox.information(self._dialog_parent(), "OpenFOAM Log", "No run log was found yet.")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(log_path)))

    def _dialog_parent(self):
        for name in ("viewer_host", "aerodynamics_tab"):
            parent = getattr(self.ui, name, None)
            if parent is not None:
                return parent
        return None

    def _to_wsl_path(self, path):
        raw = str(path).replace("\\", "/")
        match = re.match(r"^([A-Za-z]):/(.*)$", raw)
        if match:
            drive = match.group(1).lower()
            rest = match.group(2)
            return f"/mnt/{drive}/{rest}"
        return raw

    def _shell_quote(self, text):
        val = str(text)
        return "'" + val.replace("'", "'\"'\"'") + "'"

    def _cmd_quote(self, text):
        val = str(text).replace('"', '""')
        return f'"{val}"'

    def _windows_openfoam_bootstrap_path(self):
        exe = self._execution_state()
        return _find_windows_openfoam_bootstrap(exe.get("windows_bootstrap", ""))

    def _needs_openfoam_env(self, cmd):
        for token in cmd:
            name = str(token)
            if name in OPENFOAM_COMMANDS and shutil.which(name) is None:
                return True
        return False

    def _find_mpi_launcher(self):
        for exe, flag in (("mpirun", "-np"), ("mpiexec", "-n")):
            if shutil.which(exe):
                return exe, flag
        msmpi_bin = str(os.environ.get("MSMPI_BIN", "")).strip()
        if msmpi_bin:
            cand = Path(msmpi_bin) / "mpiexec.exe"
            if cand.is_file():
                return str(cand), "-n"
        for path in (
            "C:/Program Files/Microsoft MPI/Bin/mpiexec.exe",
            "C:/Program Files (x86)/Microsoft MPI/Bin/mpiexec.exe",
        ):
            cand = Path(path)
            if cand.is_file():
                return str(cand), "-n"
        return None, None

    def _queue_create_patch_if_needed(self, case_dir, tri_name, log_path):
        boundary = Path(case_dir) / "constant" / "polyMesh" / "boundary"
        if not boundary.is_file():
            self._append_run_log("[warn] boundary file not found; skipping createPatch.")
            return None
        try:
            text = boundary.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            self._append_run_log(f"[warn] Failed to read boundary file ({exc}); skipping createPatch.")
            return None
        pattern = re.compile(rf"^\\s*{re.escape(tri_name)}_", re.MULTILINE)
        if not pattern.search(text):
            self._append_run_log(f"[info] No patches matching {tri_name}_*; skipping createPatch.")
            return None
        entry = {
            "stage": "snappy_mesh",
            "cmd": ["createPatch", "-overwrite"],
            "desc": "createPatch",
            "log_path": str(log_path),
        }
        self._append_run_log(f"[info] Scheduling createPatch to merge {tri_name}_* into {tri_name}.")
        self._of_queue = [entry] + list(self._of_queue)
        return None

    def _build_native_bootstrap_wrapper(self, cmd, cwd, bootstrap):
        workdir = Path(cwd)
        runtime_dir = workspace_runtime_dir_for_case(workdir)
        script_path = runtime_dir / "run_openfoam_cmd.bat"
        command_line = subprocess.list2cmdline([str(x) for x in cmd])
        content = (
            "@echo off\r\n"
            f'call "{bootstrap}"\r\n'
            "if errorlevel 1 exit /b %errorlevel%\r\n"
            f'cd /d "{workdir}"\r\n'
            "if errorlevel 1 exit /b %errorlevel%\r\n"
            f"{command_line}\r\n"
        )
        script_path.write_text(content, encoding="utf-8", newline="\r\n")
        return script_path

    def _wsl_has_command(self, exe_name):
        if shutil.which("wsl.exe") is None:
            return False
        init = "for f in /opt/openfoam*/etc/bashrc; do [ -f \"$f\" ] && . \"$f\" && break; done"
        try:
            probe = subprocess.run(
                ["wsl.exe", "bash", "-lc", f"{init} >/dev/null 2>&1; command -v {self._shell_quote(exe_name)}"],
                capture_output=True,
                text=True,
                timeout=4,
            )
            return probe.returncode == 0 and bool((probe.stdout or "").strip())
        except Exception:
            return False

    def _resolve_openfoam_launch(self, cmd, cwd):
        if not cmd:
            return None, None, ""
        exe = str(cmd[0])
        bootstrap = self._windows_openfoam_bootstrap_path()
        if bootstrap is not None and self._needs_openfoam_env(cmd):
            wrapper = self._build_native_bootstrap_wrapper(cmd, cwd, bootstrap)
            return ["cmd.exe", "/d", "/c", str(wrapper)], None, "native-bootstrap"
        if shutil.which(exe):
            return [str(x) for x in cmd], str(cwd), "native"
        if bootstrap is not None:
            wrapper = self._build_native_bootstrap_wrapper(cmd, cwd, bootstrap)
            return ["cmd.exe", "/d", "/c", str(wrapper)], None, "native-bootstrap"
        if self._wsl_has_command(exe):
            wsl_cwd = self._to_wsl_path(cwd)
            joined = " ".join(self._shell_quote(x) for x in cmd)
            init = "for f in /opt/openfoam*/etc/bashrc; do [ -f \"$f\" ] && . \"$f\" && break; done"
            script = f"{init} >/dev/null 2>&1; cd {self._shell_quote(wsl_cwd)} && {joined}"
            return ["wsl.exe", "bash", "-lc", script], None, "wsl"
        return None, None, ""

    def _build_stage_commands(self, stage, case_dir):
        stage_name = str(stage)
        sim = self.openfoam.get("simulation", {})
        mesh = self.openfoam.get("mesh", {})
        check_mesh_enabled = bool(self.openfoam.get("check_mesh", {}).get("enabled", True))
        solver = str(self.openfoam.get("workflow", "simpleFoam"))
        use_parallel = bool(sim.get("use_parallel", False))
        mpi_cores = max(1, int(sim.get("mpi_cores", 1) or 1))
        snappy_mode = str(mesh.get("snappy_parallel_mode", "Off"))
        run_snappy_parallel = use_parallel and mpi_cores > 1 and snappy_mode in ("On", "Auto")
        run_solver_parallel = use_parallel and mpi_cores > 1
        mpi_launcher, mpi_flag = self._find_mpi_launcher()
        tri_name = str(self.openfoam.get("geometry", {}).get("tri_surface_name", "aircraft")).strip() or "aircraft"

        def warn_missing_mpi(label):
            message = f"[warn] MPI launcher not found (mpirun/mpiexec). Running {label} in serial."
            return {"stage": stage_name, "kind": "callable", "fn": lambda m=message: self._append_run_log(m)}

        if stage_name == "domain_mesh":
            return [
                {
                    "stage": "domain_mesh",
                    "cmd": ["blockMesh"],
                    "desc": "blockMesh",
                    "log_path": str(case_dir / "log.domain_mesh.txt"),
                }
            ]
        if stage_name == "surface_features":
            return [
                {
                    "stage": "surface_features",
                    "cmd": ["surfaceFeatureExtract"],
                    "desc": "surfaceFeatureExtract",
                    "log_path": str(case_dir / "log.surface_features.txt"),
                }
            ]
        if stage_name == "snappy_mesh":
            commands = []
            if run_snappy_parallel and not mpi_launcher:
                commands.append(warn_missing_mpi("snappyHexMesh"))
                run_snappy_parallel = False
            if run_snappy_parallel:
                commands.extend(
                    [
                        {
                            "stage": "snappy_mesh",
                            "cmd": ["decomposePar", "-force"],
                            "desc": "decomposePar (mesh)",
                            "log_path": str(case_dir / "log.snappy_mesh.txt"),
                        },
                        {
                            "stage": "snappy_mesh",
                            "cmd": [mpi_launcher, mpi_flag, str(mpi_cores), "snappyHexMesh", "-overwrite", "-parallel"],
                            "desc": "snappyHexMesh (parallel)",
                            "log_path": str(case_dir / "log.snappy_mesh.txt"),
                        },
                        {
                            "stage": "snappy_mesh",
                            "cmd": ["reconstructParMesh", "-constant"],
                            "desc": "reconstructParMesh",
                            "log_path": str(case_dir / "log.snappy_mesh.txt"),
                        },
                    ]
                )
            else:
                commands.append(
                    {
                        "stage": "snappy_mesh",
                        "cmd": ["snappyHexMesh", "-overwrite"],
                        "desc": "snappyHexMesh",
                        "log_path": str(case_dir / "log.snappy_mesh.txt"),
                    }
                )
            commands.append(
                {
                    "stage": "snappy_mesh",
                    "kind": "callable",
                    "fn": lambda cdir=case_dir, name=tri_name, log=str(case_dir / "log.snappy_mesh.txt"): self._queue_create_patch_if_needed(
                        cdir, name, log
                    ),
                }
            )
            return commands
        if stage_name == "check_mesh":
            check_cmd = ["checkMesh", "-meshQuality"] if check_mesh_enabled else ["checkMesh"]
            return [
                {
                    "stage": "check_mesh",
                    "cmd": check_cmd,
                    "desc": "checkMesh",
                    "log_path": str(case_dir / "log.check_mesh.txt"),
                }
            ]
        if stage_name == "solve":
            commands = []
            if run_solver_parallel and not mpi_launcher:
                commands.append(warn_missing_mpi(solver))
                run_solver_parallel = False
            if run_solver_parallel:
                commands.extend(
                    [
                        {
                            "stage": "solve",
                            "cmd": ["decomposePar", "-force"],
                            "desc": "decomposePar (solve)",
                            "log_path": str(case_dir / "log.solve.txt"),
                        },
                        {
                            "stage": "solve",
                            "cmd": [mpi_launcher, mpi_flag, str(mpi_cores), solver, "-parallel"],
                            "desc": f"{solver} (parallel)",
                            "log_path": str(case_dir / "log.solve.txt"),
                        },
                        {
                            "stage": "solve",
                            "cmd": ["reconstructPar", "-latestTime"],
                            "desc": "reconstructPar",
                            "log_path": str(case_dir / "log.solve.txt"),
                        },
                    ]
                )
            else:
                commands.append(
                    {
                        "stage": "solve",
                        "cmd": [solver],
                        "desc": solver,
                        "log_path": str(case_dir / "log.solve.txt"),
                    }
                )
            return commands
        return []

    def _build_execution_plan(self, stages):
        case_dir = self._execution_case_dir()
        plan = []
        has_case = (case_dir / "system" / "controlDict").is_file()
        for stage in stages:
            if stage == "generate":
                plan.append({"kind": "callable", "stage": "generate", "fn": lambda: self.export_openfoam_case(case_dir)})
                continue
            if stage in ("domain_mesh", "surface_features", "snappy_mesh", "check_mesh", "solve"):
                if not has_case and not any(p.get("stage") == "generate" for p in plan):
                    plan.append({"kind": "callable", "stage": "generate", "fn": lambda: self.export_openfoam_case(case_dir)})
                    has_case = True
                for cmd in self._build_stage_commands(stage, case_dir):
                    cmd.setdefault("kind", "process")
                    plan.append(cmd)
                continue
            if stage == "post":
                plan.append({"kind": "callable", "stage": "post", "fn": lambda: self._parse_force_coeffs(case_dir)})
        return case_dir, plan

    def run_openfoam_stage(self, stage):
        stage_name = str(stage).strip().lower()
        if stage_name not in {"generate", "domain_mesh", "surface_features", "snappy_mesh", "check_mesh", "solve", "post"}:
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Run", f"Unsupported stage: {stage}")
            return
        # Recover from stale UI state where status was left as running but no process/queue exists.
        if self._of_process is None and not self._of_queue and self._execution_state().get("status") == "running":
            self._set_openfoam_value("execution.status", "idle")
            self._set_openfoam_value("execution.active_stage", "none")
            self._set_execution_controls_running(False)
            self._sync_widgets_from_state()
        if self._of_process is not None or self._of_queue:
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Run", "A run is already in progress.")
            return
        case_dir = self._execution_case_dir()
        if not self._require_allowed_case_dir(case_dir, "Run OpenFOAM"):
            return
        errors = self._validate_openfoam_state()
        if errors and stage_name != "post":
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Setup", "\n".join(errors))
            return
        case_dir, plan = self._build_execution_plan([stage_name])
        if stage_name == "post" and not (case_dir / "system" / "controlDict").is_file():
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Run", f"Case not found: {case_dir}")
            return
        self._set_openfoam_value("execution.case_dir", str(case_dir))
        self._set_openfoam_value("execution.status", "running")
        self._set_openfoam_value("execution.active_stage", stage_name)
        self._set_openfoam_value("execution.last_run_started_at", datetime.now().isoformat(timespec="seconds"))
        self._set_openfoam_value("execution.last_run_finished_at", "")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_logs", {})
        self._of_cancel_requested = False
        self._of_run_mode = "stage"
        self._of_requested_stage = stage_name
        self._last_check_mesh_report = None
        self._of_queue = plan
        self._of_current = None
        self._clear_run_log_output()
        self._append_run_log(f"[{datetime.now().isoformat(timespec='seconds')}] Started stage: {stage_name}")
        self._set_execution_controls_running(True)
        self._sync_widgets_from_state()
        self._run_next_openfoam_entry()

    def run_openfoam_pipeline(self):
        if self._of_process is None and not self._of_queue and self._execution_state().get("status") == "running":
            self._set_openfoam_value("execution.status", "idle")
            self._set_openfoam_value("execution.active_stage", "none")
            self._set_execution_controls_running(False)
            self._sync_widgets_from_state()
        if self._of_process is not None or self._of_queue:
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Run", "A run is already in progress.")
            return
        case_dir = self._execution_case_dir()
        if not self._require_allowed_case_dir(case_dir, "Run OpenFOAM"):
            return
        errors = self._validate_openfoam_state()
        if errors:
            QMessageBox.warning(self.ui.aerodynamics_tab, "OpenFOAM Setup", "\n".join(errors))
            return
        stages = ["generate", "domain_mesh", "surface_features", "snappy_mesh", "check_mesh", "solve", "post"]
        case_dir, plan = self._build_execution_plan(stages)
        self._set_openfoam_value("execution.case_dir", str(case_dir))
        self._set_openfoam_value("execution.status", "running")
        self._set_openfoam_value("execution.active_stage", "generate")
        self._set_openfoam_value("execution.last_run_started_at", datetime.now().isoformat(timespec="seconds"))
        self._set_openfoam_value("execution.last_run_finished_at", "")
        self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_logs", {})
        self._of_cancel_requested = False
        self._of_run_mode = "pipeline"
        self._of_requested_stage = "pipeline"
        self._last_check_mesh_report = None
        self._of_queue = plan
        self._of_current = None
        self._clear_run_log_output()
        self._append_run_log(f"[{datetime.now().isoformat(timespec='seconds')}] Started pipeline run")
        self._set_execution_controls_running(True)
        self._sync_widgets_from_state()
        self._run_next_openfoam_entry()

    def cancel_openfoam_run(self):
        if self._of_process is None and not self._of_queue:
            return
        self._of_cancel_requested = True
        self._append_run_log("Cancellation requested...")
        if self._of_process is not None:
            self._of_process.kill()
        else:
            self._complete_openfoam_run("canceled")

    def _run_next_openfoam_entry(self):
        if self._of_cancel_requested:
            self._complete_openfoam_run("canceled")
            return
        if not self._of_queue:
            self._complete_openfoam_run("completed")
            return
        entry = self._of_queue.pop(0)
        self._of_current = entry
        stage = entry.get("stage", "none")
        self._set_openfoam_value("execution.active_stage", stage)
        self._sync_widgets_from_state()
        if entry.get("kind") == "callable":
            try:
                result = entry["fn"]()
                if stage == "post" and isinstance(result, dict):
                    self._set_openfoam_value("execution.results", result)
                self._append_run_log(f"[ok] {stage}")
            except Exception as exc:
                self._fail_openfoam_run(f"{stage} failed: {exc}")
                return
            self._run_next_openfoam_entry()
            return
        cmd = entry.get("cmd", [])
        if not cmd:
            self._run_next_openfoam_entry()
            return
        launch_cmd, launch_cwd, backend = self._resolve_openfoam_launch(cmd, str(self._execution_case_dir()))
        if launch_cmd is None:
            self._fail_openfoam_run(
                "Executable not found in PATH: "
                f"{cmd[0]}\n"
                "OpenFOAM tools are unavailable to this app process.\n"
                "Install/load OpenFOAM in your shell PATH, or install OpenFOAM in WSL and ensure `wsl bash -lc 'command -v blockMesh'` works."
            )
            return
        log_path = entry.get("log_path", "")
        if log_path:
            log_file = Path(log_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            last_logs = dict(self._execution_state().get("last_logs", {}))
            last_logs[stage] = str(log_file)
            self._set_openfoam_value("execution.last_logs", last_logs)
            self._of_log_file = open(log_file, "a", encoding="utf-8")
        if backend == "native-bootstrap":
            self._append_run_log("[info] Native executable not found in PATH. Running through Windows OpenFOAM bootstrap.")
        elif backend == "wsl":
            self._append_run_log("[info] Native executable not found. Running command through WSL.")
        self._append_run_log(f"$ {' '.join(cmd)}")
        self._start_process(cmd=launch_cmd, cwd=launch_cwd, env=None)

    def _complete_openfoam_run(self, status):
        final_status = str(status)
        finished_stage = getattr(self, "_of_requested_stage", "")
        run_mode = getattr(self, "_of_run_mode", "")
        self._set_openfoam_value("execution.status", final_status)
        self._set_openfoam_value("execution.active_stage", "none")
        if final_status == "completed":
            self._set_openfoam_value("execution.last_error", "")
        self._set_openfoam_value("execution.last_run_finished_at", datetime.now().isoformat(timespec="seconds"))
        self._of_queue = []
        self._of_current = None
        self._of_cancel_requested = False
        self._of_requested_stage = ""
        try:
            self._refresh_post_process_state(self._execution_case_dir())
        except Exception:
            pass
        self._set_execution_controls_running(False)
        self._sync_widgets_from_state()
        mesh_report = getattr(self, "_last_check_mesh_report", None)
        mesh_warnings = bool(mesh_report and mesh_report.get("has_violations"))
        if final_status == "completed":
            self._append_run_log(f"[done] Operation completed: {finished_stage or run_mode}")
            parent = getattr(getattr(self, "ui", None), "aerodynamics_tab", None)
            if parent is not None:
                if run_mode == "stage":
                    if finished_stage == "check_mesh" and mesh_warnings:
                        QMessageBox.warning(
                            parent,
                            "OpenFOAM Run",
                            "Stage finished, but checkMesh reported mesh-quality warnings.\nReview the warning dialogs and CFD Console log.",
                        )
                    else:
                        QMessageBox.information(
                            parent,
                            "OpenFOAM Run",
                            f"Stage finished successfully:\n{finished_stage}",
                        )
                else:
                    if mesh_warnings:
                        QMessageBox.warning(
                            parent,
                            "OpenFOAM Run",
                            "Pipeline finished, but checkMesh reported mesh-quality warnings.\nReview the warning dialogs and CFD Console log.",
                        )
                    else:
                        QMessageBox.information(parent, "OpenFOAM Run", "Pipeline finished successfully.")
        elif final_status == "canceled":
            self._append_run_log("[done] Operation canceled.")

    def _fail_openfoam_run(self, message):
        err = str(message)
        self._set_openfoam_value("execution.status", "failed")
        self._set_openfoam_value("execution.last_error", err)
        self._set_openfoam_value("execution.active_stage", "none")
        self._set_openfoam_value("execution.last_run_finished_at", datetime.now().isoformat(timespec="seconds"))
        self._of_queue = []
        self._of_current = None
        self._of_cancel_requested = False
        self._of_requested_stage = ""
        self._append_run_log(f"[error] {err}")
        self._set_execution_controls_running(False)
        self._sync_widgets_from_state()

    def _start_process(self, cmd, cwd, env):
        if self._of_process is not None:
            raise RuntimeError("Process already running")
        process = QProcess(self.ui.aerodynamics_tab)
        process.setProgram(str(cmd[0]))
        process.setArguments([str(x) for x in cmd[1:]])
        if cwd:
            process.setWorkingDirectory(str(cwd))
        if isinstance(env, dict):
            process_env = QProcessEnvironment.systemEnvironment()
            for key, value in env.items():
                process_env.insert(str(key), str(value))
            process.setProcessEnvironment(process_env)
        process.readyReadStandardOutput.connect(self._on_process_stdout)
        process.readyReadStandardError.connect(self._on_process_stderr)
        process.finished.connect(self._on_process_finished)
        process.start()
        self._of_process = process

    def _on_process_stdout(self):
        if self._of_process is None:
            return
        data = bytes(self._of_process.readAllStandardOutput()).decode("utf-8", errors="replace")
        if data:
            self._append_run_log(data)

    def _on_process_stderr(self):
        if self._of_process is None:
            return
        data = bytes(self._of_process.readAllStandardError()).decode("utf-8", errors="replace")
        if data:
            self._append_run_log(data)

    def _is_normal_exit_status(self, exit_status):
        try:
            if exit_status == QProcess.ExitStatus.NormalExit:
                return True
        except Exception:
            pass
        try:
            if exit_status == QProcess.NormalExit:
                return True
        except Exception:
            pass
        try:
            return str(exit_status).lower().endswith("normalexit")
        except Exception:
            return False

    def _on_process_finished(self, exit_code, exit_status):
        cmd = self._of_current.get("cmd", []) if isinstance(self._of_current, dict) else []
        log_path = self._of_current.get("log_path", "") if isinstance(self._of_current, dict) else ""
        if self._of_log_file is not None:
            self._of_log_file.flush()
            self._of_log_file.close()
            self._of_log_file = None
        if self._of_process is not None:
            self._of_process.deleteLater()
            self._of_process = None
        if self._of_cancel_requested:
            self._complete_openfoam_run("canceled")
            return
        try:
            exit_code_i = int(exit_code)
            normal_exit = self._is_normal_exit_status(exit_status)
            if (not normal_exit) or exit_code_i != 0:
                details = f"Command failed ({exit_code_i}): {' '.join(cmd)}"
                if log_path:
                    details += f"\nLog: {log_path}"
                self._fail_openfoam_run(details)
                return
            if cmd and str(cmd[0]) == "checkMesh":
                self._last_check_mesh_report = self._handle_check_mesh_result(log_path)
            self._append_run_log(f"[ok] {' '.join(cmd)}")
            if self._of_queue:
                self._run_next_openfoam_entry()
            else:
                self._complete_openfoam_run("completed")
        except Exception as exc:
            self._fail_openfoam_run(f"Process finalize error: {exc}")
