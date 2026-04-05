#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 HunyuanImage 生成投票圖片
"""

import requests
import json
import os
import sys
from datetime import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# HunyuanImage 服務配置
HUNYUAN_URL = "http://localhost:6201"
HUNYUAN_ENDPOINT = f"{HUNYUAN_URL}/api/generate"

ARTICLES = [
    {
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "中美關係",
        "prompt": "Professional voting poll poster. Chinese text: '你認為中美應否尋求和解?' Red background #DC1E25, yellow category tag '中美關係', white bold text, etnet financial news style, voting options, vote button, government building background, 1080x1350"
    },
    {
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "category": "國際政治",
        "prompt": "Professional voting poll poster. Chinese text: '特朗普重返政治舞台，你有無睇好?' Red background, yellow highlights, white text, etnet style, political theme, 1080x1350"
    }
]

def test_hunyuan_connection():
    """測試 HunyuanImage 連接"""
    
    print("[測試] 連接 HunyuanImage...")
    
    try:
        response = requests.get(f"{HUNYUAN_URL}/health", timeout=5)
        print(f"✓ HunyuanImage 已連接 (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ HunyuanImage 未連接")
        print(f"  確保服務在 {HUNYUAN_URL} 執行")
        return False
    except Exception as e:
        print(f"✗ 連接失敗: {e}")
        return False

def generate_with_hunyuan(prompt, article_id):
    """用 HunyuanImage 生成圖片"""
    
    print(f"  [生成] 正在用 HunyuanImage 生成圖片...")
    
    try:
        payload = {
            "prompt": prompt,
            "negative_prompt": "ugly, blurry, low quality",
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
            "height": 1350,
            "width": 1080,
            "seed": article_id * 1000
        }
        
        response = requests.post(
            HUNYUAN_ENDPOINT,
            json=payload,
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # 假設返回 base64 或圖片 URL
            if 'image' in result:
                # 保存圖片
                import base64
                from PIL import Image
                from io import BytesIO
                
                img_data = base64.b64decode(result['image'])
                img = Image.open(BytesIO(img_data))
                
                os.makedirs("output_images", exist_ok=True)
                filename = f"output_images/voting_{article_id}_hunyuan.png"
                img.save(filename, quality=95)
                
                print(f"  ✓ 圖片已生成: {filename}")
                return filename
            
            elif 'url' in result:
                # 下載圖片
                img_response = requests.get(result['url'])
                filename = f"output_images/voting_{article_id}_hunyuan.png"
                os.makedirs("output_images", exist_ok=True)
                
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"  ✓ 圖片已下載: {filename}")
                return filename
            
            else:
                print(f"  ⚠️  返回格式未知: {result.keys()}")
                return None
        
        else:
            print(f"  ✗ 錯誤 {response.status_code}: {response.text}")
            return None
        
    except requests.exceptions.Timeout:
        print(f"  ✗ 生成超時（可能在處理中...）")
        return None
    except Exception as e:
        print(f"  ✗ 異常: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "=" * 70)
    print("用 HunyuanImage 生成投票圖片")
    print("=" * 70 + "\n")
    
    # 測試連接
    if not test_hunyuan_connection():
        print("\n[錯誤] 無法連接 HunyuanImage")
        print("確保執行: docker ps | grep hunyuan-image")
        sys.exit(1)
    
    print()
    
    # 生成圖片
    for article in ARTICLES[:2]:  # 先試 2 張
        print(f"[#{article['id']}] {article['title']}")
        
        result = generate_with_hunyuan(article['prompt'], article['id'])
        
        if result:
            print(f"✓ 完成\n")
        else:
            print(f"✗ 失敗\n")
    
    print("=" * 70)
    print("[完成]")
    print("=" * 70)

if __name__ == "__main__":
    main()
