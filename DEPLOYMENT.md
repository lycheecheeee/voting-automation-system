# 經濟通投票議題生成系統 - 部署指南

## 🚀 快速開始

### 1. 本地執行

```bash
# 安裝依賴
pip install flask requests feedparser

# 執行 Web 應用
python run.py

# 訪問：http://localhost:5000
```

### 2. Docker 本地執行

```bash
docker compose up
# 訪問：http://localhost:5000
```

### 3. 雲端部署（推薦）

#### **Railway（最簡單）**

1. 註冊 https://railway.app
2. 用 GitHub 連接你的倉庫
3. 自動部署到 `https://your-app.railway.app`

#### **Render**

1. 註冊 https://render.com
2. 建立 Web Service
3. 連接 GitHub 倉庫
4. 設定：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:5000 app:app`

#### **Heroku**（免費額度已取消，但仍可用）

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

#### **AWS Lightsail / Google Cloud Run**

使用 Docker 鏡像部署

---

## 📋 功能

### 網頁界面

- ✅ 查看 5 個投票議題
- ✅ 點擊查看詳細文案
- ✅ 複製 Facebook / App 文案
- ✅ 下載 CSV / JSON 報告
- ✅ 即時統計資訊

### API 端點

```
GET  /                      # 主頁
GET  /api/articles          # 獲取所有議題
GET  /api/article/<id>      # 獲取單個議題
POST /api/generate          # 生成新議題
GET  /api/export/csv        # 下載 CSV
GET  /api/export/json       # 下載 JSON
GET  /api/stats             # 統計資訊
GET  /health                # 健康檢查
```

### cURL 使用範例

```bash
# 獲取所有議題
curl http://localhost:5000/api/articles

# 獲取單個議題詳情
curl http://localhost:5000/api/article/1

# 下載 CSV
curl http://localhost:5000/api/export/csv -o voting.csv

# 生成新議題
curl -X POST http://localhost:5000/api/generate
```

---

## 🔄 自動排程

### GitHub Actions（建議）

建立 `.github/workflows/voting.yml`：

```yaml
name: Weekly Voting
on:
  schedule:
    - cron: '0 1 * * 1'  # 每週一 UTC 01:00 (香港 09:00)

jobs:
  voting:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Generate voting topics
        run: python main.py
      - name: Commit results
        run: |
          git config user.name "Voting Bot"
          git config user.email "bot@example.com"
          git add output/
          git commit -m "Auto: Generate voting topics"
          git push
```

### Railway Cron Job

在 Railway 儀表板設定 Cron Job：

```bash
# 每週一 09:00 香港時間
0 9 * * 1 python main.py
```

---

## 📊 數據流

```
Web 瀏覽器
    ↓
Flask 應用 (app.py)
    ↓
API 端點
    ↓
JSON / CSV 報告
```

---

## 🔐 環境變數（可選）

建立 `.env` 檔案：

```
FLASK_ENV=production
SECRET_KEY=your-secret-key
OLLAMA_HOST=http://ollama:11434  # 如需 AI 生成
```

---

## 📱 訪問方式

### 本地
- http://localhost:5000

### 雲端（Railway 例）
- https://voting-automation-production.up.railway.app

### 手機
- 用手機瀏覽器訪問上述地址

---

## 💾 備份報告

所有報告自動保存到 `output/` 資料夾：

```
output/
├── voting_topics_20260405.csv
├── voting_topics_20260412.csv
└── voting_report_*.md
```

雲端部署時自動同步到 GitHub。

---

## ⚙️ 自訂修改

### 修改投票議題

編輯 `app.py` 中的 `SAMPLE_ARTICLES` 陣列。

### 修改 UI 樣式

編輯 `templates/index.html` 中的 `<style>` 部分。

### 集成實時新聞

取消註解 `app.py` 中的 `news_fetcher.py` 調用，啟用自動搜尋新聞。

---

## 🆘 故障排除

### 頁面不載入

```bash
# 檢查伺服器狀態
curl http://localhost:5000/health
```

### CSV 下載失敗

確保 Python 版本 ≥ 3.8

### Render 部署失敗

檢查 Build Logs，確保所有依賴正確安裝。

---

## 📈 下一步

1. ✅ 集成實時新聞爬蟲
2. ✅ 加入數據庫（PostgreSQL）存儲歷史
3. ✅ 認證系統（只允許編輯團隊使用）
4. ✅ 投票統計儀表板
5. ✅ Slack / Discord 通知

---

## 聯絡

問題或建議？提交 Issue 或 Pull Request。
