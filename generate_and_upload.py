#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版：直接生成 + 上傳到 Google Drive
不需要 Ollama / ComfyUI
"""

import os
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# 投票數據
ARTICLES = [
    {
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "中美關係",
        "options": ["同意", "不同意", "部份贊同", "無意見"]
    },
    {
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "category": "國際政治",
        "options": ["睇好", "睇淡", "無定睇", "無意見"]
    },
    {
        "id": 3,
        "title": "美俄烏克蘭局勢",
        "question": "西方應否繼續支持烏克蘭？",
        "category": "美俄關係",
        "options": ["應支持", "應停止", "適度支持", "無意見"]
    },
    {
        "id": 4,
        "title": "科技競賽升級",
        "question": "科技國族主義係咪必然趨勢？",
        "category": "中美關係",
        "options": ["係趨勢", "唔係", "因情況", "無意見"]
    },
    {
        "id": 5,
        "title": "亞太地緣政治",
        "question": "香港應點樣應對亞太局勢？",
        "category": "國際政治",
        "options": ["防守", "平衡", "遠離", "無意見"]
    }
]

def generate_image(article):
    """生成投票圖片"""
    
    # 圖片尺寸
    width, height = 1080, 1350
    
    # 顏色
    red_bg = (220, 30, 37)      # 經濟通紅
    red_dark = (180, 20, 27)    # 深紅
    white = (255, 255, 255)
    yellow = (255, 210, 0)      # 高亮黃
    
    # 建立圖片
    img = Image.new('RGB', (width, height), red_bg)
    draw = ImageDraw.Draw(img)
    
    # 字體
    try:
        font_large = ImageFont.truetype("arial.ttf", 56)
        font_normal = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except:
        font_large = font_normal = font_small = ImageFont.load_default()
    
    # Logo (左上)
    draw.text((40, 30), "etnet", fill=white, font=font_normal)
    
    # 分類 (右上 - 黃色)
    draw.rectangle([(width - 280, 20), (width - 20, 80)], fill=yellow)
    draw.text((width - 260, 32), article['category'], fill=(50, 50, 50), font=font_small)
    
    # 引號 + 問題
    draw.text((50, 130), '"', fill=yellow, font=font_large)
    
    question = article['question']
    y_pos = 160
    
    # 簡單換行
    if len(question) > 25:
        mid = len(question) // 2
        q1 = question[:mid]
        q2 = question[mid:]
        draw.text((80, y_pos), q1, fill=white, font=font_normal)
        y_pos += 70
        draw.text((80, y_pos), q2, fill=white, font=font_normal)
    else:
        draw.text((80, y_pos), question, fill=white, font=font_normal)
    
    # 投票選項
    y_pos = 380
    for i, option in enumerate(article['options']):
        # 交替顏色
        bg = white if i % 2 == 0 else red_dark
        text_color = (50, 50, 50) if i % 2 == 0 else white
        
        # 卡片
        draw.rectangle([(50, y_pos), (width - 50, y_pos + 80)],
                      fill=bg, outline=yellow, width=3)
        
        # 文字
        opt_text = f"○ {option}"
        draw.text((90, y_pos + 18), opt_text, fill=text_color, font=font_small)
        
        y_pos += 100
    
    # 按鈕 (右下 - 白色)
    btn_y = height - 140
    draw.rectangle([(width - 300, btn_y), (width - 40, btn_y + 110)],
                  fill=white, outline=white)
    draw.text((width - 270, btn_y + 20), "立即", fill=red_bg, font=font_normal)
    draw.text((width - 270, btn_y + 62), "投票", fill=red_bg, font=font_normal)
    
    # 日期 (底部)
    date_str = datetime.now().strftime("%Y年%m月%d日")
    draw.text((40, height - 50), date_str, fill=white, font=font_small)
    draw.text((width - 300, height - 50), "經濟通投票", fill=white, font=font_small)
    
    # 保存
    os.makedirs("output_images", exist_ok=True)
    filename = f"output_images/voting_{article['id']}.png"
    img.save(filename, quality=95)
    
    return filename

def upload_to_drive(image_path):
    """上傳到 Google Drive"""
    
    try:
        from google_drive_uploader import GoogleDriveUploader
        
        uploader = GoogleDriveUploader()
        
        # 建立週資料夾
        week_folder = f"投票_{datetime.now().strftime('%Y%m%d')}"
        folder_id = uploader.create_folder(
            week_folder,
            "1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH"
        )
        
        if folder_id:
            result = uploader.upload_file(image_path, folder_id)
            return result
        
        return None
    except Exception as e:
        print(f"[Drive] 上傳失敗: {e}")
        return None

def main():
    print("\n" + "=" * 70)
    print("經濟通投票圖片生成系統")
    print("=" * 70 + "\n")
    
    print("[開始] 生成 5 張投票圖片\n")
    
    generated_files = []
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"[{i}/5] {article['title']}")
        
        try:
            filename = generate_image(article)
            generated_files.append(filename)
            print(f"      ✓ 已生成: {filename}\n")
        except Exception as e:
            print(f"      ✗ 失敗: {e}\n")
    
    print("=" * 70)
    print(f"[完成] 已生成 {len(generated_files)} 張圖片")
    print("=" * 70 + "\n")
    
    # 嘗試上傳到 Drive
    print("[Drive] 嘗試上傳到 Google Drive...\n")
    
    try:
        from google_drive_uploader import GoogleDriveUploader
        
        uploader = GoogleDriveUploader()
        
        week_folder = f"投票_{datetime.now().strftime('%Y%m%d')}"
        folder_id = uploader.create_folder(
            week_folder,
            "1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH"
        )
        
        if folder_id:
            print(f"✓ 已建立資料夾: {week_folder}\n")
            
            for filename in generated_files:
                result = uploader.upload_file(filename, folder_id)
                if result:
                    print(f"✓ 已上傳: {filename}")
                    print(f"  連結: {result['link']}\n")
        else:
            print("✗ 建立 Drive 資料夾失敗\n")
            
    except ImportError:
        print("⚠️  Google Drive API 未配置")
        print("   手動上傳到:")
        print("   https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH\n")
    except Exception as e:
        print(f"⚠️  Drive 上傳失敗: {e}\n")
        print("   手動上傳位置:")
        for f in generated_files:
            print(f"   - {os.path.abspath(f)}")
    
    print("\n[完成]")

if __name__ == "__main__":
    main()
