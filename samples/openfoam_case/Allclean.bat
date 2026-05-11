@echo off
cd /d "%~dp0"
if errorlevel 1 exit /b %errorlevel%
rmdir /S /Q constant\polyMesh 2>nul
for /D %%d in (processor*) do rmdir /S /Q %%d
