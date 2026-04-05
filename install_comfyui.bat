@echo off
REM ComfyUI 一鍵安裝腳本 (Windows)
REM 自動下載、安裝、配置 ComfyUI + Stable Diffusion

setlocal enabledelayedexpansion

cls
echo ============================================================
echo ComfyUI 一鍵安裝器 (Windows)
echo ============================================================
echo.

REM 檢查 Python
echo [1/5] 檢查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 未安裝或未在 PATH
    echo 請下載: https://www.python.org/
    pause
    exit /b 1
)
echo OK: Python 已安裝
echo.

REM 檢查 Git
echo [2/5] 檢查 Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git 未安裝
    echo 請下載: https://git-scm.com/
    pause
    exit /b 1
)
echo OK: Git 已安裝
echo.

REM 建立目錄
echo [3/5] 建立目錄結構...
if not exist "C:\ComfyUI" (
    mkdir C:\ComfyUI
    echo 已建立 C:\ComfyUI
) else (
    echo C:\ComfyUI 已存在
)

if not exist "C:\ComfyUI\models\checkpoints" (
    mkdir C:\ComfyUI\models\checkpoints
)

echo OK: 目錄已準備
echo.

REM 克隆 ComfyUI
echo [4/5] 下載 ComfyUI...
cd C:\ComfyUI

if not exist ".git" (
    git clone https://github.com/comfyanonymous/ComfyUI.git .
    echo OK: ComfyUI 已下載
) else (
    echo ComfyUI 已存在，跳過下載
)
echo.

REM 安裝依賴
echo [5/5] 安裝 Python 依賴...
if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
    echo OK: 依賴已安裝
) else (
    echo venv 已存在，跳過
)
echo.

REM 下載模型提示
echo ============================================================
echo 安裝完成!
echo ============================================================
echo.
echo 下一步: 下載 Stable Diffusion 模型
echo.
echo 選項 A: 輕量模型 (推薦，1.5GB)
echo   訪問: https://huggingface.co/Lykon/DreamShaper
echo   下載任何 .safetensors 檔案
echo   放到: C:\ComfyUI\models\checkpoints\
echo.
echo 選項 B: 官方模型 (4GB+)
echo   訪問: https://huggingface.co/runwayml/stable-diffusion-v1-5
echo   下載 v1-5-pruned-emaonly.ckpt
echo.
echo 或執行自動下載:
echo   python download_model.py
echo.
echo 完成後，執行:
echo   python main.py
echo.
pause
