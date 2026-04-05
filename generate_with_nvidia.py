#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 NVIDIA API 生成高質量投票圖片
"""

import os
import sys
import requests
import json
import base64
from datetime import datetime
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# NVIDIA API 配置
NVIDIA_API_KEY = "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"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# 圖像生成端點
IMAGE_GENERATION_API = f"{NVIDIA_BASE_URL}/images/generations"

ARTICLES = [
    {
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "中美關係",
        "prompt": "Professional voting poll poster design. Main question in large white bold Chinese text: '你認為中美應否尋求和解?' Red background color #DC1E25, yellow accent color #FFD200 for category tag '中美關係'. Four voting options with radio buttons. White 'Vote Now' button bottom right. etnet financial news style. Government building background image. Modern professional design. 1080x1350 vertical format."
    },
    {
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "category": "國際政治",
        "prompt": "Professional voting poll poster. Chinese text: '特朗普重返政治舞台，你有無睇好?' Red background, yellow highlights for category '國際政治'. White bold text, four voting options, vote button. Political news aesthetic, etnet style. Professional design. 1080x1350."
    },
    {
        "id": 3,
        "title": "美俄烏克蘭局勢",
        "question": "西方應否繼續支持烏克蘭？",
        "category": "美俄關係",
        "prompt": "Voting poll poster design. Question in Chinese: '西方應否繼續支持烏克蘭?' Red background, yellow category tag '美俄關係'. White text, professional layout, voting options, vote button. International news style, etnet design. 1080x1350."
    },
    {
        "id": 4,
        "title": "科技競賽升級",
        "question": "科技國族主義係咪必然趨勢？",
        "category": "中美關係",
        "prompt": "Professional voting poll poster. Chinese question: '科技國族主義係咪必然趨勢?' Red background, yellow accent for '中美關係'. Four voting options, white text, modern design. Tech news aesthetic. 1080x1350."
    },
    {
        "id": 5,
        "title": "亞太地緣政治",
        "question": "香港應點樣應對亞太局勢？",
        "category": "國際政治",
        "prompt": "Voting poll design. Chinese text: '香港應點樣應對亞太局勢?' Red background, yellow tag '國際政治'. White voting options, professional layout, vote button. News design style. 1080x1350."
    }
]

def test_nvidia_connection():
    """測試 NVIDIA API 連接"""
    
    print("[測試] 連接 NVIDIA API...")
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json"
    }
    
    try:
        # 簡單測試
        response = requests.get(
            f"{NVIDIA_BASE_URL}/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ NVIDIA API 已連接")
            return True
        else:
            print(f"✗ NVIDIA API 錯誤: {response.status_code}")
            print(f"  {response.text[:200]}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("✗ 無法連接 NVIDIA API")
        return False
    except Exception as e:
        print(f"✗ 連接失敗: {e}")
        return False

def generate_with_nvidia(prompt, article_id):
    """用 NVIDIA API 生成圖片"""
    
    print(f"  [生成] 正在生成圖片...")
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, blurry, low quality, distorted",
        "num_images": 1,
        "image_size": "1080x1350",
        "quality": "hd",
        "steps": 50
    }
    
    try:
        response = requests.post(
            IMAGE_GENERATION_API,
            headers=headers,
            json=payload,
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # 檢查響應格式
            if 'data' in result and len(result['data']) > 0:
                # Base64 編碼的圖片
                img_base64 = result['data'][0].get('data') or result['data'][0].get('base64')
                
                if img_base64:
                    # 解碼並保存
                    import base64
                    from PIL import Image
                    from io import BytesIO
                    
                    img_data = base64.b64decode(img_base64)
                    img = Image.open(BytesIO(img_data))
                    
                    os.makedirs("output_images", exist_ok=True)
                    filename = f"output_images/voting_{article_id}_nvidia.png"
                    img.save(filename, quality=95)
                    
                    print(f"  ✓ 圖片已生成: {filename}")
                    return filename
            
            # 檢查 URL 響應
            elif 'images' in result and len(result['images']) > 0:
                img_url = result['images'][0]
                
                img_response = requests.get(img_url, timeout=30)
                filename = f"output_images/voting_{article_id}_nvidia.png"
                os.makedirs("output_images", exist_ok=True)
                
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"  ✓ 圖片已下載: {filename}")
                return filename
            
            else:
                print(f"  ⚠️  返回格式未知:")
                print(f"     {list(result.keys())}")
                print(f"     {str(result)[:300]}")
                return None
        
        else:
            print(f"  ✗ 錯誤 {response.status_code}")
            print(f"     {response.text[:300]}")
            return None
    
    except requests.exceptions.Timeout:
        print(f"  ✗ 生成超時（可能在處理...）")
        return None
    except Exception as e:
        print(f"  ✗ 異常: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("\n" + "=" * 70)
    print("用 NVIDIA API 生成高質量投票圖片")
    print("=" * 70 + "\n")
    
    # 測試連接
    if not test_nvidia_connection():
        print("\n[錯誤] 無法連接 NVIDIA API")
        sys.exit(1)
    
    print()
    
    # 生成圖片
    generated = []
    
    for article in ARTICLES:
        print(f"[#{article['id']}] {article['title']}")
        
        result = generate_with_nvidia(article['prompt'], article['id'])
        
        if result:
            generated.append(result)
            print(f"✓ 完成\n")
        else:
            print(f"✗ 失敗\n")
    
    print("=" * 70)
    print(f"[完成] 成功生成 {len(generated)}/5 張圖片")
    print("=" * 70)
    
    if generated:
        print(f"\n位置: {os.path.abspath('output_images')}\n")
        for f in generated:
            print(f"  ✓ {f}")

if __name__ == "__main__":
    main()
