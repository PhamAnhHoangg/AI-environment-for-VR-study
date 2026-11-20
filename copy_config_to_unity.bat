@echo off
if not defined UNITY_PROJECT_DIR (
    echo Set UNITY_PROJECT_DIR to your Unity project folder first.
    exit /b 1
)
copy /Y "%~dp0room_config.json" "%UNITY_PROJECT_DIR%\room_config.json"
echo Config copied to Unity project root.
