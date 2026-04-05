# 經濟通投票圖片生成系統 - 完整部署說明

## 🚀 一鍵啟動（推薦）

### 方法 1: 全自動（一個命令）

```powershell
cd C:\voting-automation
.\start_all.bat
```

這個腳本會同時開啟：
- Ollama (文本生成)
- ComfyUI (圖片生成)
- 自動執行生成任務

---

## 📋 分步執行（如果上面失敗）

### Step 1: 安裝 ComfyUI

```powershell
cd C:\voting-automation
.\install_comfyui.bat
```

這會自動：
- 檢查 Python 和 Git
- 克隆 ComfyUI 源代碼
- 安裝所有依賴

### Step 2: 下載 Stable Diffusion 模型

```powershell
cd C:\voting-automation
python download_model.py
```

會下載 DreamShaper 8 (1.5GB)

或手動：
1. 訪問：https://huggingface.co/Lykon/DreamShaper
2. 下載任何 `.safetensors` 檔案
3. 放到：`C:\ComfyUI\models\checkpoints\`

### Step 3: 啟動服務

**Terminal 1 - Ollama：**
```powershell
ollama serve
```

**Terminal 2 - ComfyUI：**
```powershell
cd C:\ComfyUI
python main.py
```

訪問：http://localhost:8188

**Terminal 3 - 執行生成：**
```powershell
cd C:\voting-automation
python ollama_comfyui_voting.py
```

---

## ✅ 完整流程

1. **Ollama** 讀取投票題目
2. **Ollama** 用 Mistral 生成專業 SD Prompt
3. **ComfyUI** 用 Stable Diffusion 生成圖片
4. 圖片自動保存到 `C:\ComfyUI\output\`
5. 手動上傳到 Google Drive

---

## 📊 預期輸出

5 張圖片：
```
voting_1_xxxxx.png  (中美關係)
voting_2_xxxxx.png  (特朗普回歸)
voting_3_xxxxx.png  (烏克蘭)
voting_4_xxxxx.png  (科技競賽)
voting_5_xxxxx.png  (亞太地緣)
```

每張約 1.5-2MB，質量高

---

## ⏱️ 時間預估

- 安裝 ComfyUI: 5 分鐘
- 下載模型: 15-30 分鐘（取決於網速）
- 生成 5 張圖: 15-60 分鐘（取決於 CPU/GPU）

**總計：30-90 分鐘**

---

## 🔧 故障排除

### ComfyUI 啟動慢
正常現象。首次加載模型需時間。

### 生成圖片超級慢（1-2分鐘/張）
因為用 CPU。可以：
- 安裝 CUDA (NVIDIA GPU)
- 用輕量模型 (TinySD)
- 降低生成步數 (15 → 10)

### Ollama 超時
增加超時時間（modify script）或檢查網絡

### 模型不存在
確保 `.safetensors` 檔案在 `C:\ComfyUI\models\checkpoints\`

---

## 📤 上傳到 Google Drive

生成完成後，手動上傳：

1. 打開 Google Drive
2. 進入資料夾：https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH
3. 建立新資料夾：`投票_20260405`
4. 上傳 `C:\ComfyUI\output\` 中的所有 PNG

---

## 🎯 下一步（自動化）

後續可以：
1. 寫 Python 腳本自動上傳（Google Drive API）
2. 設定 Windows Task Scheduler 每週執行
3. 集成到 Web 應用（Flask）
4. 發送 Slack/Email 通知

---

## 📞 需要幫助？

檢查以下：
1. `ollama serve` 是否運行
2. `http://localhost:8188` 是否可訪問
3. 模型檔案是否存在於正確位置
4. Python 版本 >= 3.8

