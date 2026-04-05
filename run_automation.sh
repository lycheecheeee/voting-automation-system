# Voting Automation System

#!/bin/bash
# 排程腳本：每週一早上 9 點執行

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGFILE="$WORK_DIR/voting_$(date +%Y%m%d_%H%M%S).log"

echo "Starting voting automation at $(date)" >> "$LOGFILE"

# 方法 1：本地執行（需要安裝 Python + Ollama）
# cd "$WORK_DIR"
# python main.py >> "$LOGFILE" 2>&1

# 方法 2：Docker Compose 執行（推薦）
cd "$WORK_DIR"
docker compose up --pull always >> "$LOGFILE" 2>&1

echo "Completed at $(date)" >> "$LOGFILE"

# 可選：上傳報告到雲端（Google Drive、Dropbox 等）
# rclone copy voting_report.html gdrive:/Voting/
# rclone copy output_images/ gdrive:/Voting/images/
