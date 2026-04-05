#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 AI 生成投票圖片（Replicate API）
支持免費使用
"""

import os
import sys
import requests
from datetime import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Replicate API (免費)
REPLICATE_API_TOKEN = "r8_XXXXXXXXXXXX"  # 需要註冊

def generate_image_with_ai(article, api_token=None):
    """用 AI 生成投票圖片"""
    
    if not api_token:
        print("Error: Replicate API token 未設定")
        print("1. 訪問 https://replicate.com/")
        print("2. 註冊免費帳號")
        print("3. 複製 API token")
        print("4. 編輯 generate_with_ai.py，填入 REPLICATE_API_TOKEN")
        return None
    
    # 構造 Prompt
    question = article['question']
    category = article['category']
    
    prompt = f"""
    Design a professional voting poll image in the style of etnet (Hong Kong financial news site).
    
    Main question in large white text: "{question}"
    Category tag in yellow: {category}
    
    Style requirements:
    - Red background (#DC1E25) - etnet brand color
    - Large white bold Chinese text for question
    - Yellow accent color (#FFD200)
    - Professional layout with voting options
    - White "Vote Now" button at bottom right
    - Clean, modern design suitable for social media
    - Aspect ratio: 1080x1350 (vertical mobile format)
    - Include 4 voting option circles
    - Date at bottom: {datetime.now().strftime("%Y年%m月%d日")}
    - etnet logo at top left
    """
    
    try:
        # 使用 Replicate API
        print(f"[AI生圖] 正在為 '{article['title']}' 生成圖片...")
        
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json",
            },
            json={
                "version": "db945719c34f8d607d2408dc989e8e4e",  # Stable Diffusion 3
                "input": {
                    "prompt": prompt,
                    "aspect_ratio": "9:16",  # 1080x1350
                    "output_format": "png"
                }
            }
        )
        
        if response.status_code == 201:
            prediction_id = response.json()['id']
            print(f"  → Prediction ID: {prediction_id}")
            print(f"  → 生成中，請稍候...")
            
            # 輪詢結果
            import time
            while True:
                result = requests.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers={"Authorization": f"Token {api_token}"}
                )
                
                status = result.json()['status']
                
                if status == 'succeeded':
                    image_url = result.json()['output'][0]
                    print(f"  ✓ 成功! 圖片URL: {image_url}")
                    
                    # 下載圖片
                    filename = download_image(image_url, article['id'])
                    return filename
                    
                elif status == 'failed':
                    print(f"  ✗ 失敗: {result.json()['error']}")
                    return None
                
                elif status == 'processing':
                    print(f"  ⏳ 正在處理...")
                    time.sleep(2)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

def download_image(url, article_id):
    """下載 AI 生成的圖片"""
    try:
        os.makedirs("output_images", exist_ok=True)
        
        response = requests.get(url, timeout=30)
        filename = f"output_images/voting_{article_id}_ai.png"
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename
    except Exception as e:
        print(f"下載失敗: {e}")
        return None

def get_api_token_from_env():
    """從環境變數或檔案讀取 API token"""
    # 方法 1: 環境變數
    token = os.environ.get('REPLICATE_API_TOKEN')
    if token:
        return token
    
    # 方法 2: .env 檔案
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('REPLICATE_API_TOKEN='):
                    return line.split('=')[1].strip()
    except:
        pass
    
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("用 AI 生成投票圖片（Replicate）")
    print("=" * 60)
    
    # 樣品數據
    articles = [
        {"id": 1, "title": "中美關係", "question": "你認為中美應否尋求和解？", "category": "中美關係"},
        {"id": 2, "title": "特朗普回歸政壇", "question": "特朗普重返政治舞台，你有無睇好？", "category": "國際政治"},
    ]
    
    # 取得 API token
    api_token = get_api_token_from_env()
    
    if not api_token:
        print("\n[需要設定] Replicate API Token")
        print("\n步驟:")
        print("1. 訪問 https://replicate.com/")
        print("2. Sign up (免費)")
        print("3. 複製你的 API token")
        print("4. 建立 .env 檔案，加入:")
        print("   REPLICATE_API_TOKEN=r8_xxxxx")
        print("\n或設定環境變數:")
        print("   set REPLICATE_API_TOKEN=r8_xxxxx")
        sys.exit(1)
    
    print(f"[API] Token 已載入\n")
    
    # 生成圖片
    for article in articles:
        result = generate_image_with_ai(article, api_token)
        if result:
            print(f"[成功] {article['title']}: {result}\n")
        else:
            print(f"[失敗] {article['title']}\n")
    
    print("=" * 60)
    print("完成!")
