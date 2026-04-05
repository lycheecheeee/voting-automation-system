from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import textwrap

def generate_voting_image(article, output_dir="output_images", background_image=None):
    """生成經濟通風格投票圖片"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 圖片尺寸（9:16 手機直向，或 16:9 橫向）
    width, height = 1080, 1350
    
    # 顏色
    red_bg = (220, 30, 37)  # 經濟通紅色
    red_dark = (180, 20, 27)
    white = (255, 255, 255)
    yellow = (255, 210, 0)  # 高亮黃色
    text_color = (50, 50, 50)
    
    # 建立圖片
    img = Image.new('RGB', (width, height), red_bg)
    draw = ImageDraw.Draw(img)
    
    # 嘗試加載字體
    try:
        logo_font = ImageFont.truetype("arial.ttf", 32)
        headline_font = ImageFont.truetype("arial.ttf", 56)
        question_font = ImageFont.truetype("arial.ttf", 48)
        option_font = ImageFont.truetype("arial.ttf", 28)
        button_font = ImageFont.truetype("arial.ttf", 26)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        headline_font = ImageFont.load_default()
        question_font = ImageFont.load_default()
        option_font = ImageFont.load_default()
        button_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        logo_font = ImageFont.load_default()
    
    # 背景圖片（可選）
    if background_image and os.path.exists(background_image):
        try:
            bg = Image.open(background_image)
            bg = bg.resize((width, int(height * 0.35)), Image.Resampling.LANCZOS)
            img.paste(bg, (0, 0))
        except:
            pass
    
    # 頂部紅色漸層區域
    draw.rectangle([(0, 0), (width, int(height * 0.4))], fill=red_bg)
    
    # Logo（左上角）
    draw.text((30, 20), "etnet", fill=white, font=logo_font)
    
    # 分類標籤（右上角）
    category = article.get('category', '國際政治')
    category_w = draw.textbbox((0, 0), category, font=small_font)[2]
    draw.rectangle(
        [(width - category_w - 50, 20), (width - 20, 55)],
        fill=yellow,
        outline=yellow
    )
    draw.text((width - category_w - 40, 28), category, fill=(200, 50, 50), font=small_font)
    
    # 引號
    quote_y = 80
    draw.text((30, quote_y), "\"", fill=white, font=headline_font)
    
    # 主要問題（白色大字）
    question = article['question']
    
    # 自動換行
    wrapper = textwrap.TextWrapper(width=15)
    wrapped_question = wrapper.wrap(text=question)
    
    y_offset = quote_y + 20
    for i, line in enumerate(wrapped_question[:3]):  # 最多3行
        # 檢查是否需要高亮某些詞
        if '應否' in line or '點樣' in line or '係咪' in line:
            # 將整行設為黃色
            draw.text((70, y_offset), line, fill=yellow, font=question_font)
        else:
            draw.text((70, y_offset), line, fill=white, font=question_font)
        y_offset += 70
    
    # 詳細背景說明（較小字）
    y_offset += 40
    reason = article.get('reason', '')
    if reason:
        wrapper_reason = textwrap.TextWrapper(width=20)
        wrapped_reason = wrapper_reason.wrap(text=reason)
        
        for line in wrapped_reason[:2]:  # 最多2行
            draw.text((50, y_offset), line, fill=white, font=option_font)
            y_offset += 45
    
    # 投票選項區域
    y_offset += 40
    draw.text((50, y_offset), "投票選項：", fill=yellow, font=option_font)
    y_offset += 60
    
    # 繪製選項（卡片式）
    for i, option in enumerate(article.get('options', [])[:4], 1):
        # 選項背景卡片
        card_height = 65
        draw.rectangle(
            [(40, y_offset), (width - 40, y_offset + card_height)],
            fill=(255, 255, 255, 200) if i % 2 == 0 else red_dark,
            outline=white if i % 2 == 0 else yellow,
            width=3
        )
        
        # 選項文字
        option_text = f"{i}. {option}"
        text_color = (50, 50, 50) if i % 2 == 0 else white
        draw.text((70, y_offset + 15), option_text, fill=text_color, font=option_font)
        
        y_offset += card_height + 15
    
    # 下方 CTA 按鈕區域
    button_y = height - 120
    
    # 白色按鈕背景
    button_radius = 15
    draw.rectangle(
        [(width - 300, button_y), (width - 30, button_y + 80)],
        fill=white,
        outline=white
    )
    
    # 按鈕文字
    button_text = "立即投票"
    draw.text((width - 250, button_y + 18), button_text, fill=red_bg, font=button_font)
    
    # 底部日期 + 版權
    draw.text((30, height - 50), datetime.now().strftime("%Y年%m月%d日"), 
              fill=white, font=small_font)
    draw.text((width - 200, height - 50), "經濟通投票系統", fill=white, font=small_font)
    
    # 保存圖片
    filename = f"{output_dir}/voting_{article['id']}_{datetime.now().strftime('%Y%m%d')}.png"
    img.save(filename, quality=95)
    print(f"✓ 生成圖片: {filename}")
    return filename

def generate_all_images(articles, output_dir="output_images"):
    """為所有議題生成圖片"""
    images = []
    for article in articles:
        try:
            img_path = generate_voting_image(article, output_dir)
            images.append(img_path)
        except Exception as e:
            print(f"✗ 生成圖片失敗 (#{article['id']}): {e}")
            import traceback
            traceback.print_exc()
    
    return images

if __name__ == "__main__":
    from app import SAMPLE_ARTICLES
    print("生成所有投票圖片（經濟通風格）...")
    images = generate_all_images(SAMPLE_ARTICLES)
    print(f"\n✓ 成功生成 {len(images)} 張圖片")
    print(f"位置: output_images/")
