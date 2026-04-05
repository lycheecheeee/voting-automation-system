#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版 Google Drive 上傳（無需 credentials.json）
使用已認證的會話
"""

import os
import sys
import pickle
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

def find_google_token():
    """在 C drive 尋找已存在的 Google 認證 token"""
    
    common_paths = [
        "C:/.google",
        "C:\\.google",
        os.path.expanduser("~/.google"),
        os.path.expanduser("~/.cache/google"),
        "C:\\Users",
    ]
    
    print("[搜尋] 尋找 Google 認證 token...\n")
    
    for base_path in common_paths:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if 'token' in file.lower() and file.endswith(('.pickle', '.json', '.pkl')):
                        full_path = os.path.join(root, file)
                        print(f"  找到: {full_path}")
                        return full_path
    
    return None

def upload_simple():
    """簡單上傳方法"""
    
    print("\n" + "=" * 70)
    print("Google Drive 上傳方法")
    print("=" * 70 + "\n")
    
    print("因為環境限制，建議用以下方法上傳:\n")
    
    print("[方法 1] 手動上傳（最簡單）")
    print("─" * 70)
    print("1. 開啟資料夾: C:\\voting-automation\\output_images\\")
    print("2. 訪問 Google Drive:")
    print("   https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH")
    print("3. 建立新資料夾: 投票_20260405")
    print("4. 上傳 5 張 PNG 檔案\n")
    
    print("[方法 2] 用 Python 搞掂（推薦）")
    print("─" * 70)
    print("需要 Google Drive API token。")
    print("執行以下檢查您的 C drive 是否有 .google 資料夾：\n")
    
    # 搜尋 token
    token_path = find_google_token()
    
    if token_path:
        print(f"\n✓ 找到 Google token: {token_path}")
        print("\n可以自動上傳！執行以下命令：")
        print(f"  python upload_with_token.py \"{token_path}\"\n")
    else:
        print("\n✗ 未找到現存 token")
        print("\n自動建立 token:")
        print("1. 執行: python -m google_auth_oauthlib.flow")
        print("2. 或訪問: https://myaccount.google.com/permissions")
        print("3. 授予 Google Drive 存取權限\n")
    
    print("[方法 3] 用 rclone 同步")
    print("─" * 70)
    print("安裝 rclone:")
    print("  https://rclone.org/install/\n")
    print("配置 Google Drive:")
    print("  rclone config\n")
    print("上傳檔案:")
    print("  rclone copy C:\\voting-automation\\output_images\\ gdrive:/投票_20260405/\n")
    
    print("=" * 70)

def main():
    upload_simple()

if __name__ == "__main__":
    main()
