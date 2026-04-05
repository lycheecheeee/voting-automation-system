@echo off
REM 一鍵啟動所有服務的腳本

cls
echo ============================================================
echo 經濟通投票系統 - 一鍵啟動
echo ============================================================
echo.
echo 本腳本將在 3 個獨立窗口中啟動：
echo   1. Ollama (LLM 文本生成)
echo   2. ComfyUI (圖片生成)
echo   3. 執行生成任務
echo.
pause

REM 啟動 Ollama
echo [1/3] 啟動 Ollama...
start "Ollama" cmd /k "ollama serve"
timeout /t 3

REM 啟動 ComfyUI
echo [2/3] 啟動 ComfyUI...
start "ComfyUI" cmd /k "cd C:\ComfyUI && python main.py"
timeout /t 5

REM 執行生成
echo [3/3] 執行生成腳本...
start "生成投票圖片" cmd /k "%cd%\run_full_pipeline.bat"

echo.
echo 已啟動所有服務！
echo 訪問 ComfyUI: http://localhost:8188
echo.
pause
