"""
Google Drive 上傳模組
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials as UserCredentials
from google.colab import auth as colab_auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
from datetime import datetime

# Google Drive API 範圍
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveUploader:
    def __init__(self, credentials_file='credentials.json'):
        """初始化 Google Drive 客戶端"""
        self.service = None
        self.credentials_file = credentials_file
        self.authenticate()
    
    def authenticate(self):
        """認證 Google Drive"""
        creds = None
        
        # 檢查是否有現存令牌
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # 如果沒有有效令牌，進行認證
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # 使用 credentials.json 檔案進行認證
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # 保存令牌
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """建立 Google Drive 資料夾"""
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        try:
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            folder_id = folder.get('id')
            print(f"✓ 建立資料夾: {folder_name} (ID: {folder_id})")
            return folder_id
        except Exception as e:
            print(f"✗ 建立資料夾失敗: {e}")
            return None
    
    def upload_file(self, file_path, folder_id=None, file_name=None):
        """上傳檔案到 Google Drive"""
        if not os.path.exists(file_path):
            print(f"✗ 檔案不存在: {file_path}")
            return None
        
        if not file_name:
            file_name = os.path.basename(file_path)
        
        file_metadata = {'name': file_name}
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        try:
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            file_id = file.get('id')
            share_link = file.get('webViewLink')
            
            print(f"✓ 上傳: {file_name}")
            print(f"  ID: {file_id}")
            print(f"  連結: {share_link}")
            
            return {
                'id': file_id,
                'name': file_name,
                'link': share_link
            }
        except Exception as e:
            print(f"✗ 上傳失敗: {e}")
            return None
    
    def upload_folder(self, local_folder_path, drive_folder_id):
        """上傳整個資料夾"""
        uploaded_files = []
        
        if not os.path.isdir(local_folder_path):
            print(f"✗ 資料夾不存在: {local_folder_path}")
            return uploaded_files
        
        for file_name in os.listdir(local_folder_path):
            file_path = os.path.join(local_folder_path, file_name)
            
            if os.path.isfile(file_path):
                result = self.upload_file(file_path, drive_folder_id)
                if result:
                    uploaded_files.append(result)
        
        return uploaded_files
    
    def find_folder(self, folder_name):
        """搜尋 Google Drive 資料夾"""
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=10
            ).execute()
            
            files = results.get('files', [])
            if files:
                return files[0]['id']
            return None
        except Exception as e:
            print(f"✗ 搜尋資料夾失敗: {e}")
            return None
    
    def share_file(self, file_id, email=None, role='reader'):
        """分享檔案"""
        try:
            if email:
                permission = {
                    'type': 'user',
                    'role': role,
                    'emailAddress': email
                }
            else:
                permission = {
                    'type': 'anyone',
                    'role': role
                }
            
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
            print(f"✓ 檔案已分享")
            return True
        except Exception as e:
            print(f"✗ 分享失敗: {e}")
            return False

def upload_voting_files_to_drive(folder_id, csv_file, json_file, images_dir):
    """上傳所有投票檔案到 Google Drive"""
    
    uploader = GoogleDriveUploader()
    
    # 建立本週資料夾
    week_folder_name = f"投票_{datetime.now().strftime('%Y%m%d')}"
    week_folder_id = uploader.create_folder(week_folder_name, folder_id)
    
    if not week_folder_id:
        print("✗ 建立週資料夾失敗")
        return None
    
    uploaded = {
        'csv': None,
        'json': None,
        'images': []
    }
    
    # 上傳 CSV
    if os.path.exists(csv_file):
        result = uploader.upload_file(csv_file, week_folder_id)
        if result:
            uploaded['csv'] = result
    
    # 上傳 JSON
    if os.path.exists(json_file):
        result = uploader.upload_file(json_file, week_folder_id)
        if result:
            uploaded['json'] = result
    
    # 上傳圖片
    if os.path.isdir(images_dir):
        uploaded['images'] = uploader.upload_folder(images_dir, week_folder_id)
    
    return uploaded

if __name__ == "__main__":
    # 測試：上傳檔案到指定資料夾
    # FOLDER_ID = "1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH"
    
    # uploader = GoogleDriveUploader()
    # result = uploader.upload_file("voting_topics_20260405.csv", FOLDER_ID)
    # print(result)
    pass
