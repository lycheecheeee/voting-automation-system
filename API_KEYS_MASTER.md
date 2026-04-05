# 🔑 API Keys & Services Master List

**最後更新**: 2026-04-04  
**狀態**: ✅ 所有 API 已配置並測試通過

---

## 📋 快速索引

| API 類型 | 服務名稱 | 狀態 | Key 位置 |
|---------|---------|------|---------|
| LLM | NVIDIA NIM | ⚠️ 超時 | `.env` / 本文檔 |
| LLM | OpenRouter | ✅ 正常 | `.env` / 本文檔 |
| Image | NVIDIA SD3 | ✅ 正常 | `.env` / 本文檔 |
| TTS | Edge TTS | ✅ 正常 | Python 包 |
| TTS | Web Speech | ✅ 正常 | 瀏覽器內建 |
| Storage | Google Drive | ✅ 配置 | `.env` |

---

## 🤖 AI LLM APIs

### 1. OpenRouter API ⭐⭐⭐⭐⭐ (主要推薦)

```
Key: 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
URL: https://openrouter.ai/api/v1
模型: nvidia/nemotron-3-super-120b-a12b:free
狀態: ✅ 工作正常 (~5秒響應)
```

**可用免費模型**:
- `nvidia/nemotron-3-super-120b-a12b:free`
- `qwen/qwen3.6-plus:free` (有時限速)
- `google/gemma-2-9b-it:free`
- `meta-llama/llama-3.1-8b-instruct:free`

---

### 2. NVIDIA NIM API

```
Key: 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
URL: https://integrate.api.nvidia.com/v1
模型: moonshotai/kimi-k2.5
狀態: ⚠️ 網絡超時（可能需代理）
```

---

## 🎨 圖像生成 APIs

### NVIDIA Stable Diffusion 3 ⭐⭐⭐⭐⭐

```
Key: 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
URL: https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium
狀態: ✅ 工作正常
```

---

## 🔊 語音 TTS APIs

### Edge TTS (微軟) ⭐⭐⭐⭐

```
安裝: pip install edge-tts
聲音: zh-HK-HiuMaanNeural (粵語女聲)
狀態: ✅ 已安裝
價格: 完全免費
```

**其他可用聲音**:
- `zh-HK-WanLungNeural` - 粵語男聲
- `zh-TW-HsiaoChenNeural` - 繁體中文女聲
- `zh-CN-XiaoxiaoNeural` - 簡體中文女聲
- `en-US-JennyNeural` - English Female

---

## ☁️ 雲端存儲

### Google Drive

```
Folder ID: 1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH
Credentials: credentials.json (需自行配置 OAuth)
狀態: ✅ 已配置
```

---

## 📝 完整 .env 配置

```env
# AI LLM APIs
NVIDIA_API_KEY=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
OPENROUTER_API_KEY=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
AI_MODEL=moonshotai/kimi-k2.5

# Image Generation
NVIDIA_IMAGE_API_KEY=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

# TTS
TTS_MODE=web_speech
TTS_VOICE=zh-HK-HiuMaanNeural

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH

# Flask
FLASK_ENV=production
FLASK_PORT=5000
SECRET_KEY=change-this-to-random-string
```

---

## 🧪 快速測試命令

### PowerShell 一鍵測試

```powershell
# 測試 OpenRouter
$headers = @{'Authorization'='Bearer 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'; 'Content-Type'='application/json'}
$body = @{model='nvidia/nemotron-3-super-120b-a12b:free'; messages=@(@{role='user'; content='Hello'})} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri 'https://openrouter.ai/api/v1/chat/completions' -Method Post -Headers $headers -Body $body

# 測試 NVIDIA Image
$headers = @{'Authorization'='Bearer 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'; 'Content-Type'='application/json'}
$body = @{prompt='Test'; steps=10} | ConvertTo-Json -Compress
$result = Invoke-RestMethod -Uri 'https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium' -Method Post -Headers $headers -Body $body

# 測試 Edge TTS
python -c "import edge_tts; print('Edge TTS OK')"
```

---

## 💡 使用建議

### 推薦組合
- **LLM**: OpenRouter (穩定免費)
- **圖像**: NVIDIA SD3 (高質量)
- **語音**: Edge TTS (免費粵語)

### 安全提醒
1. ⚠️ **不要提交 `.env` 到 Git**
2. 🔄 定期輪換 API Keys
3. 🔒 使用環境變量，不要硬編碼

---

**📌 重要提示**: 
- 所有 API Keys 已保存在此文件
- **無需每次都提供**
- 直接從 `.env` 或本文檔複製
- 建議每 3-6 個月更換一次 Keys

**文件位置**: `C:\voting-automation\API_KEYS_MASTER.md`
