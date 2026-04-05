#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查服務 + 執行投票圖片生成
"""

import requests
import sys
import time
import os
from datetime import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

OLLAMA_API = "http://localhost:11434/api/generate"
COMFYUI_API = "http://localhost:8188/prompt"

def check_ollama():
    """檢查 Ollama"""
    try:
        response = requests.post(
            OLLAMA_API,
            json={"model": "mistral", "prompt": "test", "stream": False},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def check_comfyui():
    """檢查 ComfyUI"""
    try:
        response = requests.get(
            COMFYUI_API.replace("/prompt", ""),
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def main():
    print("=" * 70)
    print("經濟通投票圖片生成系統 - 自動執行")
    print("=" * 70)
    print()
    
    # 檢查服務
    print("[檢查] Ollama...", end=" ")
    sys.stdout.flush()
    
    if check_ollama():
        print("✓ 已連接")
    else:
        print("✗ 未運行")
        print("\n需要啟動 Ollama:")
        print("  執行: ollama serve")
        print("\n或在另一個 Terminal 運行:")
        print("  & 'C:\\Bert-VITS2-Cantonese\\anaconda3\\python.exe' -c \"import subprocess; subprocess.Popen('ollama serve')\"")
        sys.exit(1)
    
    print("[檢查] ComfyUI...", end=" ")
    sys.stdout.flush()
    
    if check_comfyui():
        print("✓ 已連接")
    else:
        print("✗ 未運行")
        print("\n需要啟動 ComfyUI:")
        print("  執行: cd C:\\ComfyUI && python main.py")
        sys.exit(1)
    
    print()
    print("[成功] 所有服務已就緒！")
    print()
    print("=" * 70)
    print("開始生成投票圖片")
    print("=" * 70)
    print()
    
    # 導入生成模組
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from ollama_comfyui_voting import ARTICLES, generate_sd_prompt_with_ollama, generate_image_with_comfyui
    
    os.makedirs("output_images", exist_ok=True)
    
    print("[開始] 處理 5 個投票議題\n")
    
    success_count = 0
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"[{i}/5] {article['title']}")
        print(f"      問題: {article['question']}")
        
        try:
            # Step 1: 生成 Prompt
            print("      [Ollama] 生成圖片 Prompt...")
            sd_prompt = generate_sd_prompt_with_ollama(article)
            
            if not sd_prompt:
                sd_prompt = f"A professional voting poll design with question '{article['question']}', red background #DC1E25, yellow accents #FFD200, white text, etnet financial news style, voting circles, vote button, 1080x1350 vertical format"
                print("      [警告] 使用預設 Prompt")
            else:
                print(f"      [成功] Prompt 已生成 ({len(sd_prompt)} 字)")
            
            # Step 2: 生成圖片
            print("      [ComfyUI] 生成圖片...")
            if generate_image_with_comfyui(sd_prompt, article['id']):
                print("      [成功] 圖片已生成")
                success_count += 1
            else:
                print("      [失敗] 圖片生成失敗")
            
        except Exception as e:
            print(f"      [錯誤] {e}")
        
        print()
        time.sleep(1)
    
    print("=" * 70)
    print(f"[完成] 成功生成 {success_count}/5 張圖片")
    print("=" * 70)
    print()
    print("輸出位置: C:\\ComfyUI\\output\\")
    print()
    print("下一步:")
    print("1. 開啟 C:\\ComfyUI\\output\\ 資料夾")
    print("2. 檢查生成的圖片")
    print("3. 手動上傳到 Google Drive:")
    print("   https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH")
    print()

if __name__ == "__main__":
    main()
