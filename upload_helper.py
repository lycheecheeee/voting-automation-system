"""
簡單圖片上傳（無需 Google Drive API）
直接上傳到你指定的 Google Drive 資料夾

用法：
1. 生成圖片：python test_images.py
2. 手動上傳 output_images/ 資料夾到你的 Drive
   或用以下指令自動上傳（需要 rclone）
"""

import os
import json
from datetime import datetime

def create_upload_instructions():
    """生成上傳說明"""
    
    instructions = """
    ============================================================
    📤 手動上傳圖片到 Google Drive
    ============================================================
    
    資料夾位置：output_images/
    Drive 連結：https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH
    
    方式 1：手動上傳（最簡單）
    ───────────────────────
    1. 開啟 Google Drive
    2. 進入共享資料夾
    3. 建立新資料夾：投票_20260405
    4. 上傳 output_images/ 內所有 PNG 檔案
    
    方式 2：用 Python + Google Drive API
    ──────────────────────────────────
    # 見 google_drive_uploader.py
    
    方式 3：用 rclone（Linux/Mac）
    ────────────────────────────
    # 安裝 rclone
    $ curl https://rclone.org/install.sh | sudo bash
    
    # 配置
    $ rclone config
    # 選擇 "Google Drive" 選項
    # 授權你的帳號
    
    # 上傳
    $ rclone copy output_images/ gdrive:/投票_20260405/
    
    方式 4：GitHub Actions 自動上傳
    ───────────────────────────────
    # 見 DEPLOYMENT.md
    
    ============================================================
    
    生成的檔案：
    """
    
    if os.path.exists("output_images"):
        files = os.listdir("output_images")
        if files:
            instructions += f"\n    已生成 {len(files)} 張圖片：\n"
            for f in sorted(files):
                instructions += f"      ✓ {f}\n"
        else:
            instructions += "\n    (尚未生成圖片)\n"
    
    instructions += "\n    ============================================================\n"
    
    return instructions

if __name__ == "__main__":
    print(create_upload_instructions())
    
    # 保存上傳說明到檔案
    with open("UPLOAD_INSTRUCTIONS.txt", "w", encoding='utf-8') as f:
        f.write(create_upload_instructions())
    
    print("\n✓ 上傳說明已保存到 UPLOAD_INSTRUCTIONS.txt")
