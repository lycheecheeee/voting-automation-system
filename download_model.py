#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動下載 Stable Diffusion 模型
"""

import os
import requests
import json
from pathlib import Path

def download_file(url, destination, chunk_size=8192):
    """下載檔案（帶進度條）"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    downloaded = 0
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total_size * 100) if total_size else 0
                print(f"\r下載: {percent:.1f}% ({downloaded/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB)", end='')
    
    print()  # 換行

def download_dreamshaper():
    """下載 DreamShaper 模型"""
    
    model_dir = Path("C:/ComfyUI/models/checkpoints")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # DreamShaper 8 (1.5GB，輕量)
    model_url = "https://huggingface.co/Lykon/DreamShaper/resolve/main/DreamShaper_8_pruned.safetensors"
    model_path = model_dir / "dreamshaper_8.safetensors"
    
    if model_path.exists():
        print(f"[已存在] {model_path}")
        return
    
    print(f"[下載] DreamShaper 8 (1.5GB)...")
    print(f"目標: {model_path}")
    print()
    
    try:
        download_file(model_url, str(model_path))
        print(f"[完成] 模型已保存")
    except Exception as e:
        print(f"[失敗] {e}")
        print("\n手動下載:")
        print(f"  1. 訪問: {model_url}")
        print(f"  2. 點擊「下載」")
        print(f"  3. 放到: {model_path}")

def main():
    print("=" * 60)
    print("Stable Diffusion 模型下載器")
    print("=" * 60)
    print()
    
    download_dreamshaper()
    
    print()
    print("=" * 60)
    print("下載完成!")
    print("執行 ComfyUI: python main.py")

if __name__ == "__main__":
    main()
