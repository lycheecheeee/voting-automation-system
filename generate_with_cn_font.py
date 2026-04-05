#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用中文字體重新生成投票圖片
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
    """生成投票圖片（中文字體版）"""
    
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
    
    # 字體（用 SimHei 中文字體）
    try:
        font_logo = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 48)
        font_title = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 52)
        font_option = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 32)
        font_small = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 26)
    except Exception as e:
        print(f"字體載入失敗: {e}")
        return None
    
    # Logo (左上)
    draw.text((40, 30), "etnet", fill=white, font=font_logo)
    
    # 分類 (右上 - 黃色)
    category = article['category']
    cat_bbox = draw.textbbox((0, 0), category, font=font_small)
    cat_width = cat_bbox[2] - cat_bbox[0] + 30
    draw.rectangle(
        [(width - cat_width - 30, 15), (width - 20, 75)],
        fill=yellow
    )
    draw.text((width - cat_width - 10, 25), category, fill=(50, 50, 50), font=font_small)
    
    # 引號 + 問題
    draw.text((50, 130), '「', fill=yellow, font=font_title)
    
    question = article['question']
    y_pos = 160
    
    # 簡單換行（按長度）
    if len(question) > 20:
        # 找中點
        mid = len(question) // 2
        # 找最近的中文句號
        for i in range(mid - 2, mid + 2):
            if i < len(question) and question[i] in '？！，、':
                mid = i + 1
                break
        
        q1 = question[:mid]
        q2 = question[mid:]
        
        draw.text((90, y_pos), q1, fill=white, font=font_title)
        y_pos += 80
        draw.text((90, y_pos), q2, fill=white, font=font_title)
    else:
        draw.text((90, y_pos), question, fill=white, font=font_title)
    
    # 投票選項
    y_pos = 380
    for i, option in enumerate(article['options']):
        # 交替顏色
        bg = white if i % 2 == 0 else red_dark
        text_color = (50, 50, 50) if i % 2 == 0 else white
        
        # 卡片
        draw.rectangle(
            [(50, y_pos), (width - 50, y_pos + 80)],
            fill=bg, outline=yellow, width=3
        )
        
        # 文字
        opt_text = f"○ {option}"
        draw.text((90, y_pos + 18), opt_text, fill=text_color, font=font_option)
        
        y_pos += 100
    
    # 按鈕 (右下 - 白色)
    btn_y = height - 140
    draw.rectangle(
        [(width - 300, btn_y), (width - 40, btn_y + 110)],
        fill=white, outline=white
    )
    draw.text((width - 270, btn_y + 15), "立即", fill=red_bg, font=font_title)
    draw.text((width - 270, btn_y + 55), "投票", fill=red_bg, font=font_title)
    
    # 日期 (底部)
    date_str = datetime.now().strftime("%Y年%m月%d日")
    draw.text((40, height - 50), date_str, fill=white, font=font_small)
    draw.text((width - 280, height - 50), "經濟通投票", fill=white, font=font_small)
    
    # 保存
    os.makedirs("output_images", exist_ok=True)
    filename = f"output_images/voting_{article['id']}_cn.png"
    img.save(filename, quality=95)
    
    return filename

def main():
    print("\n" + "=" * 70)
    print("經濟通投票圖片生成系統 (中文字體版)")
    print("=" * 70 + "\n")
    
    print("[開始] 重新生成 5 張投票圖片 (附中文字體)\n")
    
    generated_files = []
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"[{i}/5] {article['title']}", end=" ... ")
        sys.stdout.flush()
        
        try:
            filename = generate_image(article)
            if filename:
                generated_files.append(filename)
                print(f"✓")
            else:
                print(f"✗ 字體問題")
        except Exception as e:
            print(f"✗ {e}")
    
    print()
    print("=" * 70)
    print(f"[完成] 已生成 {len(generated_files)} 張圖片")
    print("=" * 70 + "\n")
    
    for f in generated_files:
        print(f"✓ {f}")

if __name__ == "__main__":
    main()
