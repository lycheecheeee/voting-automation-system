#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama + ComfyUI 投票圖片生成整合
"""

import json
import requests
import os
import sys
from datetime import datetime
import time

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# 配置
OLLAMA_API = "http://localhost:11434/api/generate"
COMFYUI_API = "http://localhost:8188/prompt"
COMFYUI_HISTORY = "http://localhost:8188/history"
OUTPUT_DIR = "output_images"

# 樣品數據
ARTICLES = [
    {
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "中美關係",
        "reason": "中美貿易戰持續升溫"
    },
    {
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "category": "國際政治",
        "reason": "全球政治格局轉變"
    },
    {
        "id": 3,
        "title": "美俄烏克蘭局勢",
        "question": "西方應否繼續支持烏克蘭？",
        "category": "美俄關係",
        "reason": "戰事持續演變"
    },
    {
        "id": 4,
        "title": "科技競賽升級",
        "question": "科技國族主義係咪必然趨勢？",
        "category": "中美關係",
        "reason": "AI芯片競爭加劇"
    },
    {
        "id": 5,
        "title": "亞太地緣政治",
        "question": "香港應點樣應對亞太局勢？",
        "category": "國際政治",
        "reason": "台灣問題升溫"
    }
]

def check_services():
    """檢查 Ollama 和 ComfyUI 是否運行"""
    
    print("[檢查服務狀態]")
    
    # 檢查 Ollama
    try:
        response = requests.post(
            OLLAMA_API,
            json={"model": "mistral", "prompt": "test", "stream": False},
            timeout=5
        )
        print("  ✓ Ollama 已連接")
        ollama_ok = True
    except requests.exceptions.ConnectionError:
        print("  ✗ Ollama 未啟動")
        print("    執行: ollama serve")
        ollama_ok = False
    except Exception as e:
        print(f"  ✗ Ollama 錯誤: {e}")
        ollama_ok = False
    
    # 檢查 ComfyUI
    try:
        response = requests.get(
            COMFYUI_API.replace("/prompt", ""),
            timeout=5
        )
        print("  ✓ ComfyUI 已連接")
        comfyui_ok = True
    except requests.exceptions.ConnectionError:
        print("  ✗ ComfyUI 未啟動")
        print("    執行: cd C:\\ComfyUI && python main.py")
        comfyui_ok = False
    except Exception as e:
        print(f"  ✗ ComfyUI 錯誤: {e}")
        comfyui_ok = False
    
    return ollama_ok and comfyui_ok

def generate_sd_prompt_with_ollama(article):
    """用 Ollama 生成 Stable Diffusion Prompt"""
    
    question = article['question']
    category = article['category']
    reason = article['reason']
    
    prompt_template = f"""
根據以下資訊，生成一個適合 Stable Diffusion 的詳細英文 Prompt。

投票問題: {question}
分類: {category}
背景: {reason}

要求:
1. 紅色背景（深紅 #DC1E25）
2. 黃色高亮文字（#FFD200）
3. 白色大標題
4. 專業金融新聞風格（etnet）
5. 1080x1350 垂直格式
6. 包含 4 個投票選項圓圈
7. 右下角「Vote Now」按鈕（白色）
8. 左上角 etnet logo
9. 無中文，用視覺元素表達

輸出: 只需要 Stable Diffusion Prompt，500字以內，英文
"""
    
    try:
        print(f"    [Ollama] 生成 SD Prompt...")
        
        response = requests.post(
            OLLAMA_API,
            json={
                "model": "mistral",
                "prompt": prompt_template,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            prompt = response.json()['response'].strip()
            print(f"    ✓ Prompt 已生成 ({len(prompt)} 字)")
            return prompt
        else:
            print(f"    ✗ Ollama 錯誤")
            return None
            
    except requests.exceptions.Timeout:
        print(f"    ✗ Ollama 超時")
        return None
    except Exception as e:
        print(f"    ✗ 異常: {e}")
        return None

def generate_image_with_comfyui(sd_prompt, article_id, model_name="dreamshaper_8.safetensors"):
    """用 ComfyUI + Stable Diffusion 生成圖片"""
    
    # ComfyUI Workflow
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": model_name}
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": sd_prompt, "clip": ["1", 1]}
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": "ugly, distorted, blurry, low quality", "clip": ["1", 1]}
        },
        "4": {
            "class_type": "KSampler",
            "inputs": {
                "seed": article_id * 1000,
                "steps": 15,
                "cfg": 7.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["5", 0]
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": 1080,
                "height": 1350,
                "batch_size": 1
            }
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["4", 0], "vae": ["1", 2]}
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": f"voting_{article_id}",
                "images": ["6", 0]
            }
        }
    }
    
    try:
        print(f"    [ComfyUI] 提交生成任務...")
        
        response = requests.post(
            COMFYUI_API,
            json=workflow,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"    ✓ 任務已提交")
            return True
        else:
            print(f"    ✗ ComfyUI 錯誤: {response.status_code}")
            print(f"       {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"    ✗ 異常: {e}")
        return False

def main():
    """主程序"""
    
    print("\n" + "=" * 60)
    print("Ollama + ComfyUI 投票圖片生成系統")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 檢查服務
    print()
    if not check_services():
        print("\n[錯誤] 必要服務未啟動")
        print("\n請先執行:")
        print("  Terminal 1: ollama serve")
        print("  Terminal 2: cd C:\\ComfyUI && python main.py")
        sys.exit(1)
    
    print("\n[開始] 生成投票圖片\n")
    
    # 生成圖片
    for article in ARTICLES:
        print(f"[#{article['id']}] {article['title']}")
        
        # Step 1: 用 Ollama 生成 Prompt
        sd_prompt = generate_sd_prompt_with_ollama(article)
        
        if not sd_prompt:
            print(f"    [警告] 使用預設 Prompt")
            sd_prompt = f"A professional voting poll design, red background, question: {article['question']}, etnet financial news style, white text, yellow accents, vote buttons, 1080x1350"
        
        # Step 2: 用 ComfyUI 生成圖片
        print(f"    [生成] 正在生成圖片（可能需要 2-10 分鐘）...")
        
        if generate_image_with_comfyui(sd_prompt, article['id']):
            print(f"  ✓ 完成!\n")
        else:
            print(f"  ✗ 失敗\n")
        
        # 等待間隔
        time.sleep(2)
    
    print("=" * 60)
    print("✓ 全部完成!")
    print(f"圖片位置: {os.path.abspath(OUTPUT_DIR)}")
    print("\n下一步:")
    print("1. 檢查 ComfyUI output 資料夾的圖片")
    print("2. 手動上傳到 Google Drive")
    print(f"   https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH")

if __name__ == "__main__":
    main()
