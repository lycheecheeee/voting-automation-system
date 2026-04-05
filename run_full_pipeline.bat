@echo off
REM 完整自動化執行腳本

setlocal enabledelayedexpansion

cls
echo ============================================================
echo 經濟通投票圖片生成系統 (完整流程)
echo Ollama + ComfyUI + Google Drive
echo ============================================================
echo.

REM 檢查服務
echo [檢查] 驗證環境...
echo.

REM 檢查 Ollama
echo  檢查 Ollama...
curl -s http://localhost:11434/api/generate -X POST -d "{\"model\":\"mistral\",\"prompt\":\"test\",\"stream\":false}" >nul 2>&1
if errorlevel 1 (
    echo  ✗ Ollama 未啟動
    echo    執行: ollama serve
    echo.
) else (
    echo  ✓ Ollama 已連接
)

REM 檢查 ComfyUI
echo  檢查 ComfyUI...
curl -s http://localhost:8188 >nul 2>&1
if errorlevel 1 (
    echo  ✗ ComfyUI 未啟動
    echo    執行: cd C:\ComfyUI && python main.py
    echo.
) else (
    echo  ✓ ComfyUI 已連接
)

echo.
echo [開始] 執行生成腳本
echo.

REM 使用 Anaconda Python
set PYTHON_PATH=C:\Bert-VITS2-Cantonese\anaconda3\python.exe

if not exist "%PYTHON_PATH%" (
    echo ERROR: Python 未找到
    echo 預期位置: %PYTHON_PATH%
    pause
    exit /b 1
)

REM 執行生成腳本
"%PYTHON_PATH%" ollama_comfyui_voting.py

echo.
echo ============================================================
echo 完成!
echo ============================================================
echo.
echo 生成的圖片位置:
echo   C:\ComfyUI\output\
echo.
echo 下一步: 手動上傳到 Google Drive
echo   https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH
echo.
pause
