# 用 AI 生成投票圖片

## 選項 1: Replicate（推薦）

**免費額度：** 每月 100 次生成免費

### 設定步驟

1. **註冊 Replicate**
   ```
   https://replicate.com/
   ```

2. **複製 API Token**
   - 登入 → Settings → API Tokens
   - 複製 Token (格式: `r8_xxxxx...`)

3. **設定環境變數**
   
   Windows:
   ```powershell
   $env:REPLICATE_API_TOKEN = "r8_your_token"
   ```
   
   或建立 `.env` 檔案:
   ```
   REPLICATE_API_TOKEN=r8_your_token
   GOOGLE_DRIVE_FOLDER_ID=1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH
   ```

4. **執行生成**
   ```bash
   python generate_with_ai.py
   ```

---

## 選項 2: Hugging Face（免費）

使用開源模型，無需信用卡

```python
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="hf_xxxxx")

image = client.text_to_image(
    prompt="你的提示詞",
    model="stabilityai/stable-diffusion-3"
)
```

---

## 選項 3: Local（離線）

用 Stable Diffusion 本地執行

```bash
pip install diffusers torch
python local_generate.py
```

---

## Prompt 範例

```
Design a professional voting poll image in etnet style.

Main question in large white text: "你認為中美應否尋求和解？"
Category: 中美關係
Style: Red background (#DC1E25), yellow accents, white vote button
Format: 1080x1350 vertical

Include:
- etnet logo top left
- Yellow category tag top right
- 4 voting option circles
- "Vote Now" button bottom right
- Professional financial news aesthetic
```

---

## 成本比較

| 服務 | 免費額度 | 每1000張成本 |
|------|---------|-----------|
| Replicate | 100/月 | $1 |
| Hugging Face | 無限(慢) | $0 |
| Stable Diffusion API | 無 | $0.01-0.05 |
| Local | 無限 | $0 (需要GPU) |

---

## 故障排除

**Q: Token 無效**
A: 確保複製了完整 token，無多餘空白

**Q: 生成失敗**
A: 檢查 prompt 是否包含不允許的內容

**Q: 圖片質量不好**
A: 改用更詳細的 prompt，或試試其他模型

---

## 下一步

1. 註冊 Replicate (5分鐘)
2. 複製 API Token
3. 執行 `python generate_with_ai.py`
4. 自動上傳到 Google Drive
