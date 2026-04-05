#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動上傳投票圖片到 Google Drive
"""

import os
import sys
from datetime import datetime
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

def upload_to_drive():
    """上傳到 Google Drive"""
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.service_account import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.oauth2.credentials import Credentials as UserCredentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("需要安裝 Google API 庫：")
        print("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return False
    
    # Google Drive 資料夾 ID
    FOLDER_ID = "1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH"
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    print("\n" + "=" * 70)
    print("上傳投票圖片到 Google Drive")
    print("=" * 70 + "\n")
    
    # 認證
    creds = None
    
    # 檢查現存 token
    if os.path.exists('token.pickle'):
        import pickle
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # 如果無有效 token，執行認證流程
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 需要 credentials.json
            if not os.path.exists('credentials.json'):
                print("[錯誤] 未找到 credentials.json")
                print("\n設定方法：")
                print("1. 訪問 https://console.cloud.google.com/")
                print("2. 啟用 Google Drive API")
                print("3. 建立 OAuth 2.0 Desktop 認證")
                print("4. 下載 credentials.json")
                print("5. 放到本目錄")
                return False
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 保存 token
        import pickle
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # 建立 Drive 服務
    service = build('drive', 'v3', credentials=creds)
    
    print("[認證] Google Drive 已連接\n")
    
    # 建立週資料夾
    week_folder_name = f"投票_{datetime.now().strftime('%Y%m%d')}"
    
    print(f"[建立] 建立資料夾: {week_folder_name}")
    
    file_metadata = {
        'name': week_folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [FOLDER_ID]
    }
    
    try:
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f"  ✓ 資料夾已建立 (ID: {folder_id})\n")
    except Exception as e:
        print(f"  ✗ 建立失敗: {e}\n")
        return False
    
    # 上傳圖片
    images_dir = Path("output_images")
    
    if not images_dir.exists():
        print(f"[錯誤] 目錄不存在: {images_dir}")
        return False
    
    image_files = sorted(images_dir.glob("voting_*_cn.png"))
    
    if not image_files:
        print(f"[警告] 未找到圖片檔案")
        return False
    
    print(f"[開始] 上傳 {len(image_files)} 張圖片\n")
    
    uploaded_count = 0
    
    for i, img_path in enumerate(image_files, 1):
        filename = img_path.name
        print(f"[{i}/{len(image_files)}] {filename}", end=" ... ")
        sys.stdout.flush()
        
        try:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(str(img_path), mimetype='image/png')
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            file_id = file.get('id')
            link = file.get('webViewLink')
            
            print("✓")
            print(f"      連結: {link}")
            
            uploaded_count += 1
            
        except Exception as e:
            print(f"✗ {e}")
    
    print()
    print("=" * 70)
    print(f"[完成] 成功上傳 {uploaded_count}/{len(image_files)} 張圖片")
    print("=" * 70 + "\n")
    
    print(f"Google Drive 資料夾: {week_folder_name}")
    print(f"直接訪問: https://drive.google.com/drive/folders/{folder_id}\n")
    
    return uploaded_count == len(image_files)

if __name__ == "__main__":
    success = upload_to_drive()
    sys.exit(0 if success else 1)
