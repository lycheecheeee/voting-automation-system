# 投票自動化系統 - 排程設定

## macOS / Linux (cron)

編輯 crontab：
```bash
crontab -e
```

加入呢行（每週一早上 9 點執行）：
```
0 9 * * 1 /path/to/voting-automation/run_automation.sh
```

## Windows (Task Scheduler)

1. 開啟「工作排程程式」(Task Scheduler)
2. 建立基本工作
3. 名稱：`Voting Automation`
4. 觸發程序：週期性 → 週一 09:00
5. 操作：執行程式 → `C:\path\to\run_automation.bat`

內容（run_automation.bat）：
```batch
@echo off
cd C:\path\to\voting-automation
docker compose up --pull always
```

## 雲端排程（推薦）

### GitHub Actions
建立 `.github/workflows/voting.yml`：
```yaml
name: Weekly Voting Automation
on:
  schedule:
    - cron: '0 9 * * 1'  # 每週一 09:00 UTC

jobs:
  voting:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - name: Run voting automation
        run: docker compose up --pull always
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: voting-report
          path: |
            voting_report.html
            output_images/
```

### AWS Lambda / Google Cloud Functions
部署為無伺服器函式，用 CloudScheduler/EventBridge 觸發
