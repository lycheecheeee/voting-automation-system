#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

# 設定編碼
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install pillow")
    sys.exit(1)

# 確保有輸出資料夾
os.makedirs("output_images", exist_ok=True)

# 樣品數據
articles = [
    {"id": 1, "title": "中美關係", "question": "你認為中美應否尋求和解？", "category": "中美關係", "reason": "中美貿易戰升溫"},
    {"id": 2, "title": "特朗普回歸政壇", "question": "特朗普重返政治舞台，你有無睇好？", "category": "國際政治", "reason": "全球矚目"},
    {"id": 3, "title": "美俄烏克蘭局勢", "question": "西方應否繼續支持烏克蘭？", "category": "美俄關係", "reason": "戰事持續"},
    {"id": 4, "title": "科技競賽升級", "question": "科技國族主義係咪必然趨勢？", "category": "中美關係", "reason": "AI芯片競爭"},
    {"id": 5, "title": "亞太地緣政治", "question": "香港應點樣應對亞太局勢？", "category": "國際政治", "reason": "台灣問題升溫"}
]

print("生成經濟通風格投票圖片...")
print("=" * 60)

for article in articles:
    try:
        # 圖片尺寸
        width, height = 1080, 1350
        
        # 建立圖片（紅色背景）
        img = Image.new('RGB', (width, height), (220, 30, 37))
        draw = ImageDraw.Draw(img)
        
        # 嘗試載入字體（Windows Arial）
        try:
            font_large = ImageFont.truetype("arial.ttf", 48)
            font_normal = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 24)
        except:
            # 如果找不到，用預設字體
            font_large = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Logo (左上)
        draw.text((30, 20), "etnet", fill=(255, 255, 255), font=font_normal)
        
        # 分類標籤 (右上 - 黃色)
        draw.rectangle([(width - 250, 15), (width - 20, 65)], fill=(255, 210, 0))
        draw.text((width - 230, 25), article['category'], fill=(200, 50, 50), font=font_small)
        
        # 引號
        draw.text((40, 100), '"', fill=(255, 255, 255), font=font_large)
        
        # 主要問題 (白色大字)
        question = article['question']
        draw.text((80, 120), question, fill=(255, 255, 255), font=font_normal)
        
        # 背景說明 (較小字)
        draw.text((50, 280), "投票背景：" + article['reason'], fill=(255, 210, 0), font=font_small)
        
        # 投票選項 (卡片式)
        options = ["○ 選項 A", "○ 選項 B", "○ 選項 C", "○ 無意見"]
        y_offset = 380
        
        for i, option in enumerate(options):
            # 交替顏色
            if i % 2 == 0:
                bg_color = (255, 255, 255)
                text_color = (50, 50, 50)
            else:
                bg_color = (180, 20, 27)  # 深紅
                text_color = (255, 255, 255)
            
            # 繪製選項卡
            draw.rectangle([(40, y_offset), (width - 40, y_offset + 70)],
                          fill=bg_color, outline=(255, 255, 255), width=2)
            draw.text((70, y_offset + 15), option, fill=text_color, font=font_small)
            
            y_offset += 90
        
        # 底部 - 立即投票按鈕 (白色)
        button_y = height - 130
        draw.rectangle([(width - 320, button_y), (width - 30, button_y + 90)],
                      fill=(255, 255, 255), outline=(255, 255, 255))
        draw.text((width - 290, button_y + 20), "立即", fill=(220, 30, 37), font=font_normal)
        draw.text((width - 290, button_y + 55), "投票", fill=(220, 30, 37), font=font_normal)
        
        # 日期 & 版權 (底部)
        date_str = datetime.now().strftime("%Y年%m月%d日")
        draw.text((30, height - 40), date_str, fill=(255, 255, 255), font=font_small)
        draw.text((width - 280, height - 40), "經濟通投票系統", fill=(255, 255, 255), font=font_small)
        
        # 保存
        filename = f"output_images/voting_{article['id']}.png"
        img.save(filename, quality=95)
        print("[OK] 已生成: " + filename)
        
    except Exception as e:
        print("[FAIL] 失敗 (#" + str(article['id']) + "): " + str(e))
        import traceback
        traceback.print_exc()

print("=" * 60)
print("[DONE] 完成! 圖片已保存到 output_images/")
print("\n下一步:")
print("1. 打開 output_images/ 資料夾")
print("2. 手動上傳到 Google Drive:")
print("   https://drive.google.com/drive/folders/1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH")
