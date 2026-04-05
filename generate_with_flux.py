#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 OpenRouter Flux API 生成高質量投票圖片
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

# 從環境變數讀取 API key（如果有）
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY') or "sk-or-v1-your-key-here"

# Flux 模型
FLUX_MODELS = [
    "black-forest-labs/flux-1.1-pro",  # 最好質量
    "black-forest-labs/flux-pro",      # 次選
    "black-forest-labs/flux-realism",  # 寫實風格
]

OPENROUTER_URL = "https://openrouter.ai/api/v1/images/generations"

ARTICLES = [
    {
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "prompt": "Professional voting poll poster, Chinese text '你認為中美應否尋求和解?' in large white bold font, red background #DC1E25, yellow category tag '中美關係', four voting options with circles, white vote button bottom right, etnet financial news style, government building backdrop, modern design, 1080x1350"
    },
    {
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "prompt": "Voting poll poster design, Chinese text '特朗普重返政治舞台，你有無睇好?' in white, red background, yellow accent for category, four vote options, professional news design, etna financial style, 1080x1350"
    },
    {
        "id": 3,
        "title": "美俄烏克蘭局勢",
        "question": "西方應否繼續支持烏克蘭？",
        "prompt": "Professional voting poll design, Chinese question '西方應否繼續支持烏克蘭?' white text on red background, yellow category tag, voting options, modern layout, news style, 1080x1350"
    },
    {
        "id": 4,
        "title": "科技競賽升級",
        "question": "科技國族主義係咪必然趨勢？",
        "prompt": "Voting poll poster, Chinese text '科技國族主義係咪必然趨勢?' large white font, red background, yellow accents, voting options, professional tech news design, 1080x1350"
    },
    {
        "id": 5,
        "title": "亞太地緣政治",
        "question": "香港應點樣應對亞太局勢？",
        "prompt": "Professional voting poll, Chinese question '香港應點樣應對亞太局勢?' white text, red background, yellow category, voting options, news style layout, 1080x1350"
    }
]

def generate_with_flux(prompt, article_id, model_index=0):
    """用 Flux 生成圖片"""
    
    model = FLUX_MODELS[min(model_index, len(FLUX_MODELS) - 1)]
    
    print(f"  [Flux] 用 {model.split('/')[-1]} 生成...")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "width": 1080,
        "height": 1350,
        "num_images": 1,
        "quality": "hd"
    }
    
    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # 檢查響應
            if 'data' in result and len(result['data']) > 0:
                img_base64 = result['data'][0].get('b64_json')
                
                if img_base64:
                    from PIL import Image
                    from io import BytesIO
                    
                    img_data = base64.b64decode(img_base64)
                    img = Image.open(BytesIO(img_data))
                    
                    os.makedirs("output_images", exist_ok=True)
                    filename = f"output_images/voting_{article_id}_flux.png"
                    img.save(filename, quality=95)
                    
                    print(f"  ✓ 已生成: {filename}")
                    return filename
            
            print(f"  ⚠️  返回格式: {list(result.keys())}")
            return None
        
        elif response.status_code == 402:
            print(f"  ✗ 額度不足 (402)")
            return None
        
        elif response.status_code == 401:
            print(f"  ✗ API key 無效 (401)")
            return None
        
        else:
            print(f"  ✗ 錯誤 {response.status_code}")
            error_msg = response.text
            if len(error_msg) > 200:
                error_msg = error_msg[:200]
            print(f"     {error_msg}")
            return None
    
    except requests.exceptions.Timeout:
        print(f"  ✗ 超時（可能在處理...）")
        return None
    except Exception as e:
        print(f"  ✗ 異常: {e}")
        return None

def main():
    print("\n" + "=" * 70)
    print("用 Flux API 生成高質量投票圖片")
    print("=" * 70 + "\n")
    
    # 檢查 API key
    if OPENROUTER_API_KEY == "sk-or-v1-your-key-here":
        print("[錯誤] OpenRouter API key 未配置")
        print("\n設定方法：")
        print("1. 訪問 https://openrouter.ai/keys")
        print("2. 複製你的 API key")
        print("3. 設定環境變數:")
        print("   set OPENROUTER_API_KEY=sk-or-v1-your-key")
        print("\n或編輯 .env 檔案:")
        print("   OPENROUTER_API_KEY=sk-or-v1-xxx")
        sys.exit(1)
    
    print("[配置] 使用 OpenRouter Flux API\n")
    
    generated = []
    
    for article in ARTICLES:
        print(f"[#{article['id']}] {article['title']}")
        
        result = generate_with_flux(article['prompt'], article['id'])
        
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
    else:
        print("\n[提示] 無法生成圖片，可能原因：")
        print("  1. API key 無效或額度不足")
        print("  2. OpenRouter 未支持該模型")
        print("  3. 網路連接問題")

if __name__ == "__main__":
    main()
