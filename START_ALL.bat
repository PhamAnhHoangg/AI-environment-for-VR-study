@echo off
title German Medical VR — Start All Services
color 0A
echo.
echo  ============================================================
echo    German Medical VR  —  Starting all services
echo  ============================================================
echo.

REM ── Python path ────────────────────────────────────────────────────────────
REM Uses "python" from PATH. To use another interpreter: set VR_PYTHON=C:\path\to\python.exe
set PYTHON=python
if defined VR_PYTHON set PYTHON=%VR_PYTHON%

REM Services listen on this computer only. Set VR_LAN=1 if a headset on your network must reach them.
if "%VR_LAN%"=="1" set VR_BIND_HOST=0.0.0.0

set ROOT=%~dp0

REM ── Kill existing windows by title (closes the terminal window too) ─────────
echo  Stopping previous session...
taskkill /FI "WINDOWTITLE eq Ollama" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq Whisper :7864" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq Gradio :7863" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq Room AI :7865" /F /T 2>nul
taskkill /FI "WINDOWTITLE eq TTS :7866" /F /T 2>nul
REM ── Also kill by port in case titles differ ───────────────────────────────
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":7863 "') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":7864 "') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":7865 "') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":7866 "') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":11434 "') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul

REM ── 1. Ollama ──────────────────────────────────────────────────────────────
echo  [1/5] Ollama (port 11434)...
start "Ollama" cmd /k "ollama serve"
timeout /t 4 /nobreak >nul

REM ── 2. Whisper transcription server ────────────────────────────────────────
echo  [2/5] Checking openai-whisper install...
"%PYTHON%" -c "import whisper" 2>nul || (
    echo  openai-whisper not found — installing now...
    "%PYTHON%" -m pip install openai-whisper --quiet
    echo  Done.
)
echo  [2/5] Whisper server (port 7864)...
start "Whisper :7864" cmd /k """%PYTHON%"" ""%ROOT%whisper_server.py"""
timeout /t 2 /nobreak >nul

REM ── 3. Main Gradio chat + builder app ──────────────────────────────────────
echo  [3/5] Gradio chat app (port 7863)...
start "Gradio :7863" cmd /k """%PYTHON%"" ""%ROOT%gradio_app_v2.py"""
timeout /t 2 /nobreak >nul

REM ── 4. Room AI generator ───────────────────────────────────────────────────
echo  [4/5] Room AI generator (port 7865)...
start "Room AI :7865" cmd /k """%PYTHON%"" ""%ROOT%room_ai_gradio.py"""
timeout /t 2 /nobreak >nul

REM ── 5. Doctor TTS voice server ──────────────────────────────────────────────
echo  [5/5] Doctor TTS voice (port 7866)...
"%PYTHON%" -c "import edge_tts" 2>nul || (
    echo  edge-tts not found — installing now...
    "%PYTHON%" -m pip install edge-tts --quiet
)
"%PYTHON%" -c "import pyttsx3" 2>nul || (
    echo  pyttsx3 not found — installing now...
    "%PYTHON%" -m pip install pyttsx3 --quiet
)
start "TTS :7866" cmd /k """%PYTHON%"" ""%ROOT%tts_server.py"""

echo.
echo  ============================================================
echo    All services started!
echo.
echo    Ollama (AI model)    http://localhost:11434
echo    Whisper (voice)      http://localhost:7864
echo    Chat + Builder       http://localhost:7863
echo    Room AI generator    http://localhost:7865
echo    Doctor TTS voice     http://localhost:7866
echo  ============================================================
echo.
echo  You can close this window — services run in their own tabs.
pause
