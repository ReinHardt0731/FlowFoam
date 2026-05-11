from ._controller_common import *

def pressure_state_keys():
    return ["pressure_data", "pressure_meta"]


class PressureIOMixin:
    def open_convergence_plot(self):
        if not _MATPLOTLIB_AVAILABLE or FigureCanvas is None or Figure is None:
            QMessageBox.warning(
                self.ui.aerodynamics_tab,
                "Convergence Plot",
                "Matplotlib is not available in this environment.",
            )
            return
        dialog = self._ensure_convergence_dialog()
        if dialog is None:
            return
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        self._conv_refresh_from_log()

    def _ensure_convergence_dialog(self):
        if self._conv_dialog is not None:
            return self._conv_dialog
        try:
            dialog = QDialog(self.ui.aerodynamics_tab)
            dialog.setWindowTitle("Convergence Plot")
            dialog.setModal(False)
            layout = QVBoxLayout(dialog)
            toolbar = QHBoxLayout()
            self.btn_conv_refresh = QPushButton("Refresh", dialog)
            self.btn_conv_clear = QPushButton("Clear", dialog)
            toolbar.addWidget(self.btn_conv_refresh)
            toolbar.addWidget(self.btn_conv_clear)
            toolbar.addStretch(1)
            layout.addLayout(toolbar)
            fig = Figure(figsize=(8.0, 6.0), tight_layout=True)
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas, 1)
            self._conv_fig = fig
            self._conv_canvas = canvas
            self._conv_resid_ax = fig.add_subplot(2, 1, 1)
            self._conv_coeff_ax = fig.add_subplot(2, 1, 2)
            self.btn_conv_refresh.clicked.connect(self._conv_refresh_from_log)
            self.btn_conv_clear.clicked.connect(self._conv_clear_data)
            dialog.finished.connect(self._on_convergence_dialog_closed)
            dialog.resize(900, 700)
            self._conv_dialog = dialog
            self._conv_redraw(force=True)
            return dialog
        except Exception as exc:
            QMessageBox.warning(
                self.ui.aerodynamics_tab,
                "Convergence Plot",
                f"Failed to initialize plotting backend: {exc}",
            )
            return None

    def _on_convergence_dialog_closed(self):
        if self._conv_redraw_timer is not None:
            self._conv_redraw_timer.stop()

    def _conv_reset_data(self):
        self._conv_residuals = {}
        self._conv_coeffs = {"x": [], "Cd": [], "Cl": [], "Cm": []}
        self._conv_current_time = None
        self._conv_resid_iter = 0
        self._conv_coeff_iter = 0
        self._conv_log_buffer = ""

    def _conv_clear_data(self):
        self._conv_reset_data()
        self._conv_redraw(force=True)

    def _conv_get_log_path(self):
        exe = self._execution_state()
        last_logs = exe.get("last_logs", {}) if isinstance(exe.get("last_logs", {}), dict) else {}
        log_path = str(last_logs.get("solve", "")).strip()
        if log_path:
            path = Path(log_path)
            if path.is_file():
                return path
        case_dir = self._execution_case_dir()
        fallback = case_dir / "log.solve.txt"
        if fallback.is_file():
            return fallback
        return None

    def _conv_refresh_from_log(self):
        path = self._conv_get_log_path()
        if path is None:
            QMessageBox.information(
                self.ui.aerodynamics_tab,
                "Convergence Plot",
                "Solve log not found yet. Run a solve to generate log.solve.txt.",
            )
            return
        self._conv_reset_data()
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                for raw in handle:
                    self._conv_parse_line(raw.strip())
        except Exception as exc:
            QMessageBox.warning(
                self.ui.aerodynamics_tab,
                "Convergence Plot",
                f"Failed to read log: {exc}",
            )
            return
        self._conv_redraw(force=True)

    def _conv_feed_log_text(self, text):
        dialog = getattr(self, "_conv_dialog", None)
        if dialog is None or not dialog.isVisible():
            return
        chunk = str(text)
        if not chunk:
            return
        buffer = getattr(self, "_conv_log_buffer", "") + chunk
        lines = buffer.splitlines()
        if buffer and not buffer.endswith(("\n", "\r")):
            self._conv_log_buffer = lines.pop() if lines else buffer
        else:
            self._conv_log_buffer = ""
        for line in lines:
            self._conv_parse_line(line.strip())
        self._conv_maybe_redraw()

    def _conv_parse_line(self, line):
        if not line:
            return
        time_value = _parse_convergence_time(line)
        if time_value is not None:
            self._conv_current_time = time_value
        residual = _parse_convergence_residual(line)
        if residual is not None:
            field, value = residual
            if self._conv_current_time is not None:
                x_value = self._conv_current_time
            else:
                x_value = self._conv_resid_iter
                self._conv_resid_iter += 1
            self._conv_append_residual(field, x_value, value)
        coeffs = _parse_convergence_coeffs(line)
        if coeffs is not None:
            cd, cl, cm = coeffs
            if self._conv_current_time is not None:
                x_value = self._conv_current_time
            else:
                x_value = self._conv_coeff_iter
                self._conv_coeff_iter += 1
            self._conv_append_coeffs(x_value, cd, cl, cm)

    def _conv_append_residual(self, field, x_value, y_value):
        series = self._conv_residuals.setdefault(field, {"x": [], "y": []})
        series["x"].append(x_value)
        series["y"].append(y_value)

    def _conv_append_coeffs(self, x_value, cd, cl, cm):
        self._conv_coeffs["x"].append(x_value)
        self._conv_coeffs["Cd"].append(cd)
        self._conv_coeffs["Cl"].append(cl)
        self._conv_coeffs["Cm"].append(cm)

    def _conv_maybe_redraw(self):
        if self._conv_canvas is None:
            return
        now = time.monotonic()
        interval = float(getattr(self, "_conv_draw_interval", 0.7))
        if (now - self._conv_last_draw) >= interval:
            self._conv_redraw(force=True)
            return
        if self._conv_redraw_timer is None:
            self._conv_redraw_timer = QTimer(self.ui.aerodynamics_tab)
            self._conv_redraw_timer.setSingleShot(True)
            self._conv_redraw_timer.timeout.connect(self._conv_on_redraw_timer)
        if not self._conv_redraw_timer.isActive():
            delay_ms = int(max(100, (interval - (now - self._conv_last_draw)) * 1000))
            self._conv_redraw_timer.start(delay_ms)

    def _conv_on_redraw_timer(self):
        self._conv_redraw(force=True)

    def _conv_redraw(self, force=False):
        if self._conv_canvas is None or self._conv_fig is None:
            return
        if not force:
            return
        self._conv_last_draw = time.monotonic()
        ax_resid = self._conv_resid_ax
        ax_coeff = self._conv_coeff_ax
        if ax_resid is None or ax_coeff is None:
            return
        ax_resid.clear()
        ax_coeff.clear()
        plotted = False
        order = ["p", "Ux", "Uy", "Uz", "U", "k", "omega"]
        for field in order:
            series = self._conv_residuals.get(field)
            if not series:
                continue
            x_vals = series["x"]
            y_vals = series["y"]
            if not x_vals or not y_vals:
                continue
            ax_resid.plot(x_vals, y_vals, label=field)
            plotted = True
        if plotted:
            ax_resid.set_yscale("log")
            ax_resid.set_ylabel("Initial residual")
            ax_resid.set_xlabel("Iteration/Time")
            ax_resid.grid(True, which="both", linestyle="--", alpha=0.35)
            ax_resid.legend(loc="best", fontsize="small")
        else:
            ax_resid.text(0.5, 0.5, "No residual data", ha="center", va="center", transform=ax_resid.transAxes)
        coeff_x = self._conv_coeffs.get("x", [])
        if coeff_x:
            ax_coeff.plot(coeff_x, self._conv_coeffs.get("Cd", []), label="Cd")
            ax_coeff.plot(coeff_x, self._conv_coeffs.get("Cl", []), label="Cl")
            ax_coeff.plot(coeff_x, self._conv_coeffs.get("Cm", []), label="Cm")
            ax_coeff.set_ylabel("Coefficient")
            ax_coeff.set_xlabel("Iteration/Time")
            ax_coeff.grid(True, linestyle="--", alpha=0.35)
            ax_coeff.legend(loc="best", fontsize="small")
        else:
            ax_coeff.text(0.5, 0.5, "No coefficient data", ha="center", va="center", transform=ax_coeff.transAxes)
        try:
            self._conv_canvas.draw_idle()
        except Exception:
            pass

    def load_pressure_csv_from_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui.aerodynamics_tab,
            "Load Pressure CSV",
            "",
            "CSV Files (*.csv);;All Files (*.*)",
        )
        if not file_path:
            return
        self.load_pressure_csv(file_path)

    def load_pressure_csv(self, file_path):
        try:
            data = self._parse_pressure_csv(file_path)
            self.current_data = data
            self._populate_field_selector(data)
            default_key = self._pick_default_field_key(data)
            self._render_field_plot(data, default_key)
            self._save_pressure_state(data, default_key)
        except Exception as exc:
            QMessageBox.critical(self.ui.aerodynamics_tab, "Pressure Data Error", str(exc))

    def _populate_field_selector(self, data):
        self.field_selector.blockSignals(True)
        self.field_selector.clear()
        self.field_key_map = {}
        for key in data["field_order"]:
            display = data["field_labels"].get(key, key)
            self.field_selector.addItem(display)
            self.field_key_map[display] = key
        self.field_selector.blockSignals(False)
        enabled = self.field_selector.count() > 0
        self.field_selector.setEnabled(enabled)
        self.refresh_plot_btn.setEnabled(enabled)
        if hasattr(self, "btn_clear_pressure_data"):
            self.btn_clear_pressure_data.setEnabled(enabled)
        self._update_pressure_controls_visibility()

    def _pick_default_field_key(self, data):
        priority = ["cp", "p", "u_mag", "wall_shear_mag", "yplus", "k", "omega", "nut"]
        for key in priority:
            if key in data["fields"]:
                return key
        return data["field_order"][0]

    def _on_field_changed(self, _index):
        if self.current_data is None:
            return
        display = self.field_selector.currentText()
        key = self.field_key_map.get(display)
        if key:
            self._render_field_plot(self.current_data, key)
            self._save_pressure_state(self.current_data, key)

    def _on_refresh_clicked(self):
        if self.current_data is None:
            QMessageBox.information(self.ui.aerodynamics_tab, "Aerodynamics", "Load a CSV first.")
            return
        display = self.field_selector.currentText()
        key = self.field_key_map.get(display)
        if not key:
            return
        self._render_field_plot(self.current_data, key)
        self._save_pressure_state(self.current_data, key)

    def clear_pressure_plot(self):
        self.current_data = None
        self.field_key_map = {}
        if hasattr(self, "field_selector"):
            blocked = self.field_selector.blockSignals(True)
            self.field_selector.clear()
            self.field_selector.blockSignals(blocked)
            self.field_selector.setEnabled(False)
        if hasattr(self, "refresh_plot_btn"):
            self.refresh_plot_btn.setEnabled(False)
        if hasattr(self, "btn_clear_pressure_data"):
            self.btn_clear_pressure_data.setEnabled(False)
        aero_state = self.state.setdefault("aerodynamics", {})
        aero_state["pressure_data"] = None
        aero_state["pressure_meta"] = None
        self._refresh_viewer_scene()
        self._update_pressure_controls_visibility()

    def _parse_pressure_csv(self, path):
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError("CSV is empty.")
        norm = {}
        for col in df.columns:
            cleaned = str(col).strip().strip('"').strip().lower()
            norm[col] = cleaned
        df = df.rename(columns=norm)
        x_col = "points:0" if "points:0" in df.columns else "x"
        y_col = "points:1" if "points:1" in df.columns else ("y" if "y" in df.columns else None)
        z_col = "points:2" if "points:2" in df.columns else ("z" if "z" in df.columns else None)
        if x_col not in df.columns:
            raise ValueError("Missing x coordinate. Expected 'Points:0' or 'x'.")
        x = pd.to_numeric(df[x_col], errors="coerce")
        y = pd.to_numeric(df[y_col], errors="coerce") if y_col else None
        z = pd.to_numeric(df[z_col], errors="coerce") if z_col else None
        fields = {}
        labels = {}

        def add_scalar(key, label, col_name):
            if col_name in df.columns:
                arr = pd.to_numeric(df[col_name], errors="coerce")
                fields[key] = arr.to_numpy(dtype=float)
                labels[key] = label

        add_scalar("cp", "Pressure Coefficient (Cp)", "cp")
        add_scalar("p", "Pressure (p)", "p")
        add_scalar("k", "Turbulent Kinetic Energy (k)", "k")
        add_scalar("nut", "Turbulent Viscosity (nut)", "nut")
        add_scalar("omega", "Specific Dissipation (omega)", "omega")
        add_scalar("yplus", "Wall yPlus", "yplus")
        u0, u1, u2 = "u:0", "u:1", "u:2"
        if u0 in df.columns and u1 in df.columns and u2 in df.columns:
            ux = pd.to_numeric(df[u0], errors="coerce").to_numpy(dtype=float)
            uy = pd.to_numeric(df[u1], errors="coerce").to_numpy(dtype=float)
            uz = pd.to_numeric(df[u2], errors="coerce").to_numpy(dtype=float)
            fields["u_x"] = ux
            fields["u_y"] = uy
            fields["u_z"] = uz
            fields["u_mag"] = np.sqrt(ux * ux + uy * uy + uz * uz)
            labels["u_x"] = "Velocity Ux"
            labels["u_y"] = "Velocity Uy"
            labels["u_z"] = "Velocity Uz"
            labels["u_mag"] = "Velocity Magnitude |U|"
        s0, s1, s2 = "wallshearstress:0", "wallshearstress:1", "wallshearstress:2"
        if s0 in df.columns and s1 in df.columns and s2 in df.columns:
            sx = pd.to_numeric(df[s0], errors="coerce").to_numpy(dtype=float)
            sy = pd.to_numeric(df[s1], errors="coerce").to_numpy(dtype=float)
            sz = pd.to_numeric(df[s2], errors="coerce").to_numpy(dtype=float)
            fields["wall_shear_x"] = sx
            fields["wall_shear_y"] = sy
            fields["wall_shear_z"] = sz
            fields["wall_shear_mag"] = np.sqrt(sx * sx + sy * sy + sz * sz)
            labels["wall_shear_x"] = "Wall Shear Stress X"
            labels["wall_shear_y"] = "Wall Shear Stress Y"
            labels["wall_shear_z"] = "Wall Shear Stress Z"
            labels["wall_shear_mag"] = "Wall Shear Magnitude"
        if not fields:
            raise ValueError("No plottable fields found in pressure CSV.")
        invalid_base = x.isna()
        if y is not None:
            invalid_base = invalid_base | y.isna()
        if z is not None:
            invalid_base = invalid_base | z.isna()
        for key, values in fields.items():
            if np.isnan(values).any() or invalid_base.any():
                bad = int(np.isnan(values).sum() + invalid_base.sum())
                raise ValueError(f"Field '{labels.get(key, key)}' has {bad} invalid numeric row(s).")
        field_order = list(fields.keys())
        return {
            "path": path,
            "x": x.to_numpy(dtype=float),
            "y": y.to_numpy(dtype=float) if y is not None else None,
            "z": z.to_numpy(dtype=float) if z is not None else None,
            "fields": fields,
            "field_labels": labels,
            "field_order": field_order,
            "point_count": int(len(df)),
        }

    def _save_pressure_state(self, data_dict, selected_key):
        aero_state = self.state.setdefault("aerodynamics", {})
        x = data_dict["x"]
        y = data_dict["y"]
        z = data_dict["z"]
        aero_state["pressure_data"] = {
            "x": x.tolist(),
            "y": y.tolist() if y is not None else None,
            "z": z.tolist() if z is not None else None,
            "fields": {k: v.tolist() for k, v in data_dict["fields"].items()},
        }
        selected_vals = data_dict["fields"][selected_key]
        aero_state["pressure_meta"] = {
            "source_path": data_dict["path"],
            "point_count": data_dict["point_count"],
            "available_fields": data_dict["field_order"],
            "selected_field": selected_key,
            "selected_field_label": data_dict["field_labels"].get(selected_key, selected_key),
            "selected_min": float(np.min(selected_vals)),
            "selected_max": float(np.max(selected_vals)),
            "loaded_at": datetime.now().isoformat(timespec="seconds"),
        }
