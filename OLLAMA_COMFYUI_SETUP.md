# Ollama + ComfyUI 完整部署指南

## 系統要求

- Ollama（已安裝）
- ComfyUI（需要下載）
- Python 3.11+
- 4GB+ RAM（推薦 8GB+）
- GPU（可選，用 CPU 較慢）

---

## Step 1: 安裝 ComfyUI

### Windows 環境

**方法 A: 下載便攜版（推薦）**

```powershell
# 建立工作目錄
mkdir C:\ComfyUI
cd C:\ComfyUI

# 下載最新版
# 訪問：https://github.com/comfyanonymous/ComfyUI/releases
# 下載 windows_portable_python_xxxxx.7z
# 解壓到 C:\ComfyUI
```

**方法 B: 用 Git 安裝**

```powershell
cd C:\
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 2: 下載必要模型

```powershell
cd C:\ComfyUI

# 建立模型資料夾
mkdir models\checkpoints
mkdir models\loras
mkdir models\vae

# 下載 Stable Diffusion 1.5（輕量）
# 訪問：https://huggingface.co/runwayml/stable-diffusion-v1-5
# 下載 v1-5-pruned-emaonly.ckpt（4GB）
# 放到 models\checkpoints\

# 或用輕量版（1.5GB）
cd models\checkpoints
# 訪問：https://huggingface.co/Lykon/DreamShaper
# 下載任何 .safetensors 檔案
```

---

## Step 3: 啟動 ComfyUI

```powershell
cd C:\ComfyUI

# 執行（會自動開瀏覽器）
python main.py

# 應該會看到：
# To see the GUI go to: http://127.0.0.1:8188
```

訪問：**http://localhost:8188**

---

## Step 4: 集成 Ollama

**安裝 Ollama + ComfyUI 整合**

```powershell
cd C:\ComfyUI\custom_nodes
git clone https://github.com/city96/ComfyUI_OllamaGPT.git
# 或
git clone https://github.com/sipherxyz/comfyui-art-venture.git
```

---

## Step 5: 建立自動化腳本

建立 `ollama_comfyui_voting.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合 Ollama + ComfyUI 生成投票圖片
"""

import json
import requests
import time
import os
from datetime import datetime

# 配置
OLLAMA_API = "http://localhost:11434/api/generate"
COMFYUI_API = "http://localhost:8188/prompt"
OUTPUT_DIR = "output_images"

def generate_prompt_with_ollama(article):
    """用 Ollama 生成圖片 Prompt"""
    
    question = article['question']
    category = article['category']
    
    prompt_template = f"""
    生成一個適合 Stable Diffusion 的詳細圖片 Prompt。
    
    要求：
    - 投票圖片，經濟通風格
    - 主要問題：{question}
    - 分類：{category}
    - 紅色背景（#DC1E25）
    - 黃色高亮
    - 白色文字
    - 專業金融新聞風格
    - 1080x1350 垂直格式
    - 包含投票選項
    - 「立即投票」按鈕
    
    用英文輸出 Prompt（500字以內）：
    """
    
    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "model": "mistral",
                "prompt": prompt_template,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            return response.json()['response']
        return None
    except Exception as e:
        print(f"Ollama 錯誤: {e}")
        return None

def generate_image_with_comfyui(prompt, article_id):
    """用 ComfyUI 生成圖片"""
    
    # ComfyUI Workflow（簡化版）
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "dreamshaper_8.safetensors"  # 改為你的模型
            }
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt,
                "clip": ["1", 1]
            }
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "ugly, bad quality",  # 負面提示
                "clip": ["1", 1]
            }
        },
        "4": {
            "class_type": "KSampler",
            "inputs": {
                "seed": article_id,
                "steps": 20,
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
            "inputs": {
                "samples": ["4", 0],
                "vae": ["1", 2]
            }
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
        print(f"[ComfyUI] 正在生成圖片 #{article_id}...")
        
        response = requests.post(
            COMFYUI_API,
            json=workflow
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"[成功] 圖片已生成")
            return True
        else:
            print(f"[失敗] ComfyUI 錯誤: {response.text}")
            return False
            
    except Exception as e:
        print(f"[錯誤] {e}")
        return False

def main():
    """主程序"""
    
    print("=" * 60)
    print("Ollama + ComfyUI 投票圖片生成系統")
    print("=" * 60)
    
    # 樣品數據
    articles = [
        {
            "id": 1,
            "title": "中美關係",
            "question": "你認為中美應否尋求和解？",
            "category": "中美關係"
        },
        {
            "id": 2,
            "title": "特朗普回歸政壇",
            "question": "特朗普重返政治舞台，你有無睇好？",
            "category": "國際政治"
        }
    ]
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 檢查連線
    print("\n[檢查] 連接 Ollama...")
    try:
        requests.post(OLLAMA_API, json={"model": "mistral", "prompt": "test", "stream": False}, timeout=5)
        print("  ✓ Ollama 已連接")
    except:
        print("  ✗ Ollama 未啟動。執行: ollama serve")
        return
    
    print("[檢查] 連接 ComfyUI...")
    try:
        requests.get(COMFYUI_API.replace("/prompt", ""), timeout=5)
        print("  ✓ ComfyUI 已連接")
    except:
        print("  ✗ ComfyUI 未啟動。執行: python main.py")
        return
    
    print("\n[開始] 生成投票圖片\n")
    
    # 生成圖片
    for article in articles:
        print(f"[#{ article['id']}] {article['title']}")
        
        # Step 1: 用 Ollama 生成 Prompt
        print("  1️⃣ 用 Ollama 生成 Prompt...")
        sd_prompt = generate_prompt_with_ollama(article)
        
        if not sd_prompt:
            print("  ✗ Prompt 生成失敗，使用預設")
            sd_prompt = f"A professional voting poll poster with question '{article['question']}', red background, yellow accents, white text, etnet style, 1080x1350"
        else:
            print(f"  ✓ Prompt 已生成")
        
        # Step 2: 用 ComfyUI 生成圖片
        print("  2️⃣ 用 ComfyUI 生成圖片...")
        if generate_image_with_comfyui(sd_prompt, article['id']):
            print(f"  ✓ 圖片已保存\n")
        else:
            print(f"  ✗ 圖片生成失敗\n")
    
    print("=" * 60)
    print("✓ 完成!")
    print(f"圖片位置: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
```

---

## 快速啟動

### Terminal 1: Ollama
```powershell
ollama serve
```

### Terminal 2: ComfyUI
```powershell
cd C:\ComfyUI
python main.py
```

### Terminal 3: 執行生成腳本
```powershell
cd voting-automation
python ollama_comfyui_voting.py
```

---

## 常見問題

**Q: ComfyUI 啟動很慢**
A: 第一次加載模型會下載 4GB+，請耐心等待

**Q: 生成圖片超級慢（5-10分鐘）**
A: 因為用 CPU。建議：
- 用輕量模型（TinySD）
- 或配置 GPU

**Q: 出現 CUDA 錯誤**
A: 無關，你無 NVIDIA GPU，用 CPU 就可以

**Q: 模型不存在**
A: 下載模型到 `models\checkpoints\`

---

## 下一步

1. ✅ 下載並安裝 ComfyUI
2. ✅ 下載 Stable Diffusion 模型
3. ✅ 啟動 Ollama + ComfyUI
4. ✅ 執行 `ollama_comfyui_voting.py`
5. ✅ 自動上傳到 Google Drive

開始執行？

