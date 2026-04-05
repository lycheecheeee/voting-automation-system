#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

# 簡化版：直接生成示範數據
today = datetime.now().strftime('%Y-%m-%d')

articles = [
    {
        "date": today,
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "中美關係",
        "options": ["同意", "不同意", "部份贊同", "無意見"],
        "controversy": 85,
        "hotness": 88,
        "reason": "中美貿易戰持續升溫，影響全球經濟。香港作為國際金融中心，息息相關。",
        "editor_statement": "本週中美關係再成網絡熱話。在全球政治格局轉變下，中美和解的可能性成為各界關注焦點。此議題涉及香港未來發展方向，值得深入探討。",
        "fb_feed": "新題出爐🗳️\n\n你認為中美應否尋求和解？\n\n唔同立場有咩理據？投票話俾我地知！\n\n#中美關係 #國際政治",
        "fb_image_text": "你點睇？中美應否尋求和解？",
        "banner": "你點睇？中美關係",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n你認為中美應否尋求和解？",
        "app_title": "【你點睇？】中美關係",
        "app_headline": "你認為中美應否尋求和解？投票現已開放！"
    },
    {
        "date": today,
        "id": 2,
        "title": "特朗普回歸政壇",
        "question": "特朗普重返政治舞台，你有無睇好？",
        "category": "國際政治",
        "options": ["睇好", "睇淡", "無定睇", "無意見"],
        "controversy": 82,
        "hotness": 90,
        "reason": "特朗普重返政治舞台，其政策主張引起國際關注。對香港經濟及地緣政治有重大影響。",
        "editor_statement": "特朗普作為前美國總統再次涉足政治，引起全球矚目。其貿易保護主義政策、對華態度等，將深遠影響亞太局勢及香港未來。",
        "fb_feed": "新題出爐🗳️\n\n特朗普重返政治舞台，你有無睇好？\n\n佢的回歸會帶來咩轉變？投票話俾我地知！\n\n#特朗普 #美國政治",
        "fb_image_text": "你點睇？特朗普重返政治舞台",
        "banner": "你點睇？特朗普回歸",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n特朗普重返政治舞台，你有無睇好？",
        "app_title": "【你點睇？】特朗普回歸",
        "app_headline": "特朗普重返政治舞台，你有無睇好？投票現已開放！"
    },
    {
        "date": today,
        "id": 3,
        "title": "美俄烏克蘭局勢",
        "question": "西方應否繼續支持烏克蘭？",
        "category": "美俄關係",
        "options": ["應該支持", "應該停止", "應適度支持", "無意見"],
        "controversy": 78,
        "hotness": 75,
        "reason": "烏克蘭戰事持續，西方援助政策成為焦點。涉及全球秩序重組及香港地位問題。",
        "editor_statement": "烏克蘭局勢持續演變，西方國家的援助政策引起激烈辯論。從經濟、安全、人道等多角度，都值得深入討論。",
        "fb_feed": "新題出爐🗳️\n\n西方應否繼續支持烏克蘭？\n\n點睇呢個複雜的國際問題？投票話俾我地知！\n\n#烏克蘭 #國際關係",
        "fb_image_text": "你點睇？西方應否支持烏克蘭",
        "banner": "你點睇？烏克蘭局勢",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n西方應否繼續支持烏克蘭？",
        "app_title": "【你點睇？】烏克蘭局勢",
        "app_headline": "西方應否繼續支持烏克蘭？投票現已開放！"
    },
    {
        "date": today,
        "id": 4,
        "title": "科技競賽升級",
        "question": "你認為科技國族主義係咪必然趨勢？",
        "category": "中美關係",
        "options": ["係必然趨勢", "唔係必然", "因情況而異", "無意見"],
        "controversy": 72,
        "hotness": 82,
        "reason": "中美科技戰升級，芯片、AI等領域成為競爭焦點。香港作為科技樞紐，前景堪憂。",
        "editor_statement": "科技競賽成為中美競爭的新戰場。國族主義色彩日濃，企業面臨選擇。香港科技產業如何應對？值得思考。",
        "fb_feed": "新題出爐🗳️\n\n你認為科技國族主義係咪必然趨勢？\n\n香港科技業點樣應對？投票話俾我地知！\n\n#科技競賽 #中美關係",
        "fb_image_text": "你點睇？科技國族主義趨勢",
        "banner": "你點睇？科技競賽",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n你認為科技國族主義係咪必然趨勢？",
        "app_title": "【你點睇？】科技競賽",
        "app_headline": "科技國族主義是必然趨勢嗎？投票現已開放！"
    },
    {
        "date": today,
        "id": 5,
        "title": "亞太地緣政治",
        "question": "亞太局勢緊張，香港應點樣應對？",
        "category": "國際政治",
        "options": ["加強防守", "尋求平衡", "遠離競爭", "無意見"],
        "controversy": 80,
        "hotness": 78,
        "reason": "台灣問題升溫，南海局勢緊張。香港處於地緣政治漩渦中心，應對策略至關重要。",
        "editor_statement": "亞太地區已成為全球最具戰略意義的地帶。香港如何在大國博弈中保護自身利益？此議題涉及香港未來生存發展，必須深思。",
        "fb_feed": "新題出爐🗳️\n\n亞太局勢緊張，香港應點樣應對？\n\n我地應點樣應戰？投票話俾我地知！\n\n#香港前景 #亞太局勢",
        "fb_image_text": "你點睇？香港應點樣應對亞太局勢",
        "banner": "你點睇？香港出路",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n亞太局勢緊張，香港應點樣應對？",
        "app_title": "【你點睇？】亞太局勢",
        "app_headline": "亞太局勢緊張，香港應點樣應對？投票現已開放！"
    }
]

# 保存
with open('voting_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("=" * 60)
print("早晨！今日草擬咗以下題目，請大家睇睇：")
print("=" * 60)

for article in articles:
    print(f"\n{article['id']}. {article['title']}")
    print(f"   問題: {article['question']}")
    print(f"   爭議度: {article['controversy']}/100 | 熱度: {article['hotness']}/100")

print("\n" + "=" * 60)
print("✓ 投票議題已生成（voting_articles.json）")
print("=" * 60)
