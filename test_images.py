"""
快速測試：生成樣品圖片（唔需要 Google Drive 認證）
"""

from image_generator import generate_all_images, generate_voting_image
from datetime import datetime
import json

# 樣品數據
SAMPLE_ARTICLES = [
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "中美關係",
        "options": ["同意", "不同意", "部份贊同", "無意見"],
        "controversy": 85,
        "hotness": 88,
        "reason": "中美貿易戰持續升溫，影響全球經濟。香港作為國際金融中心，息息相關。",
        "editor_statement": "本週中美關係再成網絡熱話。在全球政治格局轉變下，中美和解的可能性成為各界關注焦點。"
    },
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "category": "國際政治",
        "options": ["睇好", "睇淡", "無定睇", "無意見"],
        "controversy": 82,
        "hotness": 90,
        "reason": "特朗普作為前美國總統再次涉足政治，引起全球矚目。",
        "editor_statement": "特朗普重返政治舞台，引起全球矚目。其貿易保護主義政策、對華態度等，將深遠影響亞太局勢。"
    },
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 3,
        "title": "美俄烏克蘭局勢",
        "question": "西方應否繼續支持烏克蘭？",
        "category": "美俄關係",
        "options": ["應該支持", "應該停止", "應適度支持", "無意見"],
        "controversy": 78,
        "hotness": 75,
        "reason": "烏克蘭戰事持續，西方援助政策成為焦點。",
        "editor_statement": "烏克蘭局勢持續演變，西方國家的援助政策引起激烈辯論。"
    },
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 4,
        "title": "科技競賽升級",
        "question": "科技國族主義係咪必然趨勢？",
        "category": "中美關係",
        "options": ["係必然趨勢", "唔係必然", "因情況而異", "無意見"],
        "controversy": 72,
        "hotness": 82,
        "reason": "中美科技戰升級，芯片、AI等領域成為競爭焦點。",
        "editor_statement": "科技競賽成為中美競爭的新戰場。國族主義色彩日濃。"
    },
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 5,
        "title": "亞太地緣政治",
        "question": "香港應點樣應對亞太局勢？",
        "category": "國際政治",
        "options": ["加強防守", "尋求平衡", "遠離競爭", "無意見"],
        "controversy": 80,
        "hotness": 78,
        "reason": "台灣問題升溫，南海局勢緊張。香港處於地緣政治漩渦。",
        "editor_statement": "亞太地區已成為全球最具戰略意義的地帶。"
    }
]

if __name__ == "__main__":
    import os
    
    # 建立輸出資料夾
    os.makedirs("output_images", exist_ok=True)
    
    print("=" * 60)
    print("生成樣品圖片（經濟通風格）")
    print("=" * 60)
    
    # 生成所有圖片
    images = generate_all_images(SAMPLE_ARTICLES, "output_images")
    
    print("\n" + "=" * 60)
    print(f"✓ 成功生成 {len(images)} 張圖片")
    print("=" * 60)
    print("\n生成位置：")
    for img in images:
        print(f"  - {img}")
    
    print("\n可以用以下方式查看：")
    print("  1. 開啟 output_images/ 資料夾直接睇圖")
    print("  2. 上傳到 Google Drive 分享")
    print("  3. 用網頁應用查看（http://localhost:5000）")
    
    print("\n如需調整設計，編輯 image_generator.py 中的參數：")
    print("  - 顏色：red_bg, red_dark, yellow 等")
    print("  - 字體大小：headline_font, question_font 等")
    print("  - 版面：y_offset, rectangle 座標等")
