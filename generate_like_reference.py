#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成一模一樣嘅經濟通投票圖片（按你個 reference 設計）
- 頂部背景圖片
- 大白色粗體文字
- 黃色高亮詞語
- 引號 + 主問題 + 副題
- 右下角斜角按鈕
"""

import os
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import urllib.request

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

ARTICLES = [
    {
        "id": 1,
        "title": "中美關係",
        "main_q": "你認為中美應否",
        "highlight": "尋求和解",
        "sub_q": "定會更加對立？",
        "options": ["同意", "不同意", "無定睇", "無意見"]
    },
    {
        "id": 2,
        "title": "特朗普回歸",
        "main_q": "特朗普重返政治舞台",
        "highlight": "你有無睇好",
        "sub_q": "佢嘅政策會帶來轉變？",
        "options": ["睇好", "睇淡", "無定睇", "無意見"]
    },
    {
        "id": 3,
        "title": "烏克蘭",
        "main_q": "西方應否",
        "highlight": "繼續支持烏克蘭",
        "sub_q": "定要停止援助？",
        "options": ["支持", "停止", "適度", "無意見"]
    },
    {
        "id": 4,
        "title": "科技競賽",
        "main_q": "科技國族主義",
        "highlight": "係咪必然趨勢",
        "sub_q": "定只係暫時現象？",
        "options": ["趨勢", "暫時", "無定", "無意見"]
    },
    {
        "id": 5,
        "title": "亞太局勢",
        "main_q": "香港應點樣",
        "highlight": "應對亞太局勢",
        "sub_q": "定應該保持中立？",
        "options": ["防守", "平衡", "遠離", "無意見"]
    }
]

def create_placeholder_bg():
    """建立佔位符背景圖片（灰色建築物）"""
    # 簡單灰色背景（代表建築物）
    bg = Image.new('RGB', (1080, 400), (180, 180, 180))
    draw = ImageDraw.Draw(bg)
    
    # 簡單線條模擬窗戶
    for x in range(0, 1080, 80):
        for y in range(0, 400, 80):
            draw.rectangle([(x+10, y+10), (x+60, y+60)], outline=(150, 150, 150), width=2)
    
    return bg

def generate_image_like_reference(article):
    """生成一模一樣嘅投票圖片"""
    
    width, height = 1080, 1500  # 更高嘅比例
    
    # 顏色
    red = (200, 20, 30)
    white = (255, 255, 255)
    yellow = (255, 210, 0)
    
    # 建立圖片
    img = Image.new('RGB', (height, width), red)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # 顏色轉換（因為 rotate 的關係，改用正常方向）
    img = Image.new('RGB', (width, height), red)
    draw = ImageDraw.Draw(img)
    
    # 字體
    try:
        font_etnet = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 40)
        font_quote = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 80)
        font_main = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 64)
        font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 48)
        font_button = ImageFont.truetype("C:\\Windows\\Fonts\\simhei.ttf", 45)
    except Exception as e:
        print(f"字體錯誤: {e}")
        return None
    
    # 頂部背景圖片（簡單灰色）
    bg = create_placeholder_bg()
    img.paste(bg, (0, 0))
    
    # etnet logo (右上)
    draw.text((width - 150, 30), "etnet", fill=white, font=font_etnet)
    
    # 紅色覆蓋層（約 50% 透明）
    overlay = Image.new('RGBA', (width, height), (200, 20, 30, 180))
    img.paste(Image.alpha_composite(
        Image.new('RGBA', (width, height), (0, 0, 0, 0)),
        overlay
    ), (0, 0), overlay)
    
    # 重新建立 draw
    draw = ImageDraw.Draw(img)
    
    # 引號 + 主問題
    y_pos = 420
    
    draw.text((50, y_pos), '「', fill=white, font=font_quote)
    
    y_pos += 80
    
    # 主問題（拆分為 main + highlight + sub）
    main_q = article['main_q']
    highlight = article['highlight']
    sub_q = article['sub_q']
    
    # 第一行：main_q
    draw.text((80, y_pos), main_q, fill=white, font=font_main)
    y_pos += 75
    
    # 第二行：highlight (黃色)
    draw.text((80, y_pos), highlight, fill=yellow, font=font_main)
    y_pos += 75
    
    # 第三行：sub_q (白色)
    draw.text((80, y_pos), sub_q, fill=white, font=font_sub)
    
    # 右下角按鈕（斜角設計）
    btn_x = width - 280
    btn_y = height - 180
    
    # 白色矩形
    draw.rectangle(
        [(btn_x, btn_y), (btn_x + 240, btn_y + 140)],
        fill=white, outline=white
    )
    
    # 斜線（模擬斜角）
    draw.line([(btn_x + 20, btn_y), (btn_x + 240, btn_y + 50)], fill=red, width=8)
    
    # 按鈕文字
    draw.text((btn_x + 60, btn_y + 35), "立即", fill=red, font=font_button)
    draw.text((btn_x + 60, btn_y + 80), "投票", fill=red, font=font_button)
    
    # 保存
    os.makedirs("output_images", exist_ok=True)
    
    # 旋轉 90 度（因為之前寬高搞反了）
    filename = f"output_images/voting_{article['id']}_like_ref.png"
    img.save(filename, quality=95)
    
    return filename

def main():
    print("\n" + "=" * 70)
    print("生成一模一樣嘅投票圖片（按 reference 設計）")
    print("=" * 70 + "\n")
    
    print("[開始] 生成 5 張圖片\n")
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"[{i}/5] {article['title']}", end=" ... ")
        sys.stdout.flush()
        
        try:
            filename = generate_image_like_reference(article)
            if filename:
                print(f"✓")
            else:
                print(f"✗")
        except Exception as e:
            print(f"✗ {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 70)
    print("[完成]")
    print("=" * 70)

if __name__ == "__main__":
    main()
