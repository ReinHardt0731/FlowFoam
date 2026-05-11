@echo off
setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"
call "F:\ResearchFiles\Openfoam\aerodynamics\openfoam\v2412\setEnvVariables-v2412.bat"
if errorlevel 1 exit /b %errorlevel%
cd /d "%SCRIPT_DIR%"
if errorlevel 1 exit /b %errorlevel%
set MAX_CORES=4
set SNAPPY_MODE=On
set MPI_LAUNCHER=
set MPI_NP_FLAG=-np
where mpirun >nul 2>&1 && set MPI_LAUNCHER=mpirun
if not defined MPI_LAUNCHER (
  where mpiexec >nul 2>&1 && set MPI_LAUNCHER=mpiexec
  if defined MPI_LAUNCHER set MPI_NP_FLAG=-n
)
blockMesh
set SNAPPY_CORES=%MAX_CORES%
if !SNAPPY_CORES! GEQ 2 if not defined MPI_LAUNCHER (
  echo MPI launcher not found (mpirun/mpiexec). Running snappyHexMesh in serial.
  set SNAPPY_CORES=1
)
surfaceFeatureExtract
if !SNAPPY_CORES! GEQ 2 (
  powershell -Command "(Get-Content system/decomposeParDict) -replace '^(numberOfSubdomains\s+)\d+;','$1'+$env:SNAPPY_CORES+';' | Set-Content system/decomposeParDict"
  decomposePar -force
  %MPI_LAUNCHER% %MPI_NP_FLAG% !SNAPPY_CORES! snappyHexMesh -overwrite -parallel
  reconstructParMesh -constant
  for /D %%d in (processor*) do rmdir /S /Q %%d
) else (
  snappyHexMesh -overwrite
)
findstr /R /C:"aircraft_" constant\polyMesh\boundary >nul
if %ERRORLEVEL% EQU 0 (
  echo Merging aircraft_* patches into aircraft via createPatch
  createPatch -overwrite
)
checkMesh -meshQuality > log.checkMesh 2>&1
for /f "tokens=2 delims=: " %%a in ('findstr /R /C:"cells:[ ]*[0-9][0-9]*" log.checkMesh') do set NCELLS=%%a
if not defined NCELLS set NCELLS=0
set /a CORES=NCELLS/50000
if !CORES! LSS 2 set CORES=1
if !CORES! GTR %MAX_CORES% set CORES=%MAX_CORES%
echo Mesh cells: !NCELLS! ^| recommended cores: !CORES! (max %MAX_CORES%)
if !CORES! GEQ 2 if not defined MPI_LAUNCHER (
  echo MPI launcher not found (mpirun/mpiexec). Running solver in serial.
  set CORES=1
)
if !CORES! GEQ 2 (
  powershell -Command "(Get-Content system/decomposeParDict) -replace '^(numberOfSubdomains\s+)\d+;','$1'+$env:CORES+';' | Set-Content system/decomposeParDict"
  decomposePar -force
  %MPI_LAUNCHER% %MPI_NP_FLAG% !CORES! simpleFoam -parallel
  reconstructPar -latestTime
  for /D %%d in (processor*) do rmdir /S /Q %%d
) else (
  simpleFoam
)
