# 投票自動化系統使用指南

## 功能概述

自動搜尋國際新聞 → 生成投票題目 → 製作圖片 → 生成報告

- **新聞來源**：BBC、Reuters、Bloomberg、The Guardian RSS feeds
- **題目生成**：本地 Mistral AI 模型（免費）
- **圖片生成**：Python Pillow
- **輸出**：JSON + HTML 報告 + PNG 圖片
- **排程**：每週一早上 9 點

## 快速開始

### 前置需求
- Docker & Docker Compose
- 或 Python 3.11+ + Ollama

### 方法 1：Docker Compose（推薦）

```bash
cd voting-automation
docker compose up --pull always
```

首次執行會自動：
1. 下載 Ollama 模型
2. 啟動 Ollama 服務
3. 執行投票自動化
4. 生成報告

輸出檔案：
- `voting_report.html` - 用瀏覽器打開查看
- `output_images/` - 投票圖片
- `news.json` - 新聞資料
- `voting_topics.json` - 題目資料

### 方法 2：本地執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動 Ollama（另一個終端）
ollama serve

# 拉取 Mistral 模型
ollama pull mistral

# 執行
python main.py
```

## 排程設定

### macOS / Linux (cron)
```bash
crontab -e
# 加入：0 9 * * 1 /path/to/voting-automation/run_automation.sh
```

### Windows (Task Scheduler)
見 SCHEDULING.md

### GitHub Actions
見 SCHEDULING.md

## 自訂選項

編輯 `news_fetcher.py` 更改新聞來源：
```python
NEWS_FEEDS = [
    "https://...",  # 自訂 RSS feed
]
```

編輯 `topic_generator.py` 調整題目風格：
```python
prompt = """Your custom prompt..."""
```

## 常見問題

**Q: 執行失敗說找不到 Mistral 模型**
A: 第一次執行時需要下載模型（約 5GB），或手動執行：
```bash
docker compose exec ollama ollama pull mistral
```

**Q: 生成的題目質量不好**
A: Mistral 是輕量模型。改用更強大的模型：
```bash
ollama pull neural-chat  # 或 llama2
```
再編輯 `topic_generator.py` 改變 model="mistral" → model="neural-chat"

**Q: 想用 OpenAI API 而不是本地模型**
A: 編輯 `topic_generator.py`：
```python
import openai
# 改為調用 OpenAI API
```

**Q: 想自動上傳到 Google Drive / Dropbox**
A: 安裝 rclone：
```bash
rclone config  # 配置雲端帳號
# 編輯 run_automation.sh 加入上傳命令
```

## 進階：集成到網站

生成的 `voting_report.html` 可以：
1. 放到 web server（nginx、Apache）
2. 用 Python Flask / Django 包裝
3. 集成到現有網站

## 日誌

查看執行日誌：
```bash
cat voting_*.log
```

## 支持的 Ollama 模型

- `mistral` - 輕量、快速（推薦）
- `neural-chat` - 更好質量
- `llama2` - 更強大但慢
- `orca-mini` - 最輕量

拉取模型：
```bash
docker compose exec ollama ollama pull <model_name>
```
