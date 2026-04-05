import json
import ollama
import re
from datetime import datetime

def generate_voting_articles(news_articles, num_articles=5):
    """用 Mistral 生成詳細投票議題（經濟通風格）"""
    
    # 準備新聞摘要
    news_context = "\n".join([
        f"- [{article['category']}] {article['title']}: {article['summary']}"
        for article in news_articles[:10]
    ])
    
    prompt = f"""你係經濟通網站嘅投票編輯，專門設計高討論度投票議題。

基於以下本週香港 + 國際政治新聞，請草擬 {num_articles} 個投票議題，每個須包含：

新聞背景：
{news_context}

對每個議題，請返回以下資訊（使用繁體中文）：

題號 (1-{num_articles})
日期：{datetime.now().strftime('%Y-%m-%d')}
主題：[簡潔標題，無數字]
精簡背景連問法：[封閉式問題，30字內]
建議選項：[4-5個選項，每個8字內，須包「無意見」]
爭議度：[0-100評分]
網上熱度：[0-100評分]
版主聲明：[書面語，200字內，簡述背景+爭議點]
FB feed文字：[口語化，150字內，包括投票概念]
FB圖片文字：[簡潔，50字內]
Banner文稿：[10字內]
Article footer文字：[總結文字，80字內]
Message to Voting group：[專業口吻]
App push Title：[吸引標題]
App push Headline：[主要內容，80字內]

注意：
- 題目要反映香港人關注的國際動態
- 聚焦中美關係、特朗普、美俄關係
- 必須有清晰的正反立場或多方意見
- 文字專業而吸引
- 無連結、無多餘HTML"""

    try:
        response = ollama.generate(
            model="mistral",
            prompt=prompt,
            stream=False
        )
        
        response_text = response['response']
        # 簡單解析（實際應該更複雜）
        articles = parse_voting_articles(response_text)
        return articles
    except Exception as e:
        print(f"Error with Mistral: {e}")
    
    # Fallback：生成示範
    return generate_sample_articles(news_articles, num_articles)

def parse_voting_articles(text):
    """解析 AI 輸出為結構化數據"""
    articles = []
    # 簡單分割
    blocks = text.split("題號")
    
    for block in blocks[1:]:  # 跳過第一個空白塊
        article = {}
        
        # 提取關鍵資訊
        lines = block.split("\n")
        for line in lines:
            if "日期：" in line:
                article['date'] = line.split("日期：")[1].strip()[:10]
            elif "主題：" in line:
                article['title'] = line.split("主題：")[1].strip()
            elif "精簡背景連問法：" in line:
                article['question'] = line.split("精簡背景連問法：")[1].strip()
            elif "建議選項：" in line:
                opts = line.split("建議選項：")[1].strip()
                article['options'] = [o.strip() for o in opts.split("、") if o.strip()]
            elif "爭議度：" in line:
                try:
                    article['controversy'] = int(re.search(r'\d+', line).group())
                except:
                    article['controversy'] = 70
            elif "網上熱度：" in line:
                try:
                    article['hotness'] = int(re.search(r'\d+', line).group())
                except:
                    article['hotness'] = 75
            elif "版主聲明：" in line:
                article['editor_statement'] = line.split("版主聲明：")[1].strip()
            elif "FB feed文字：" in line:
                article['fb_feed'] = line.split("FB feed文字：")[1].strip()
            elif "FB圖片文字：" in line:
                article['fb_image_text'] = line.split("FB圖片文字：")[1].strip()
            elif "Banner文稿：" in line:
                article['banner'] = line.split("Banner文稿：")[1].strip()
            elif "Article footer文字：" in line:
                article['footer'] = line.split("Article footer文字：")[1].strip()
            elif "Message to Voting group：" in line:
                article['group_message'] = line.split("Message to Voting group：")[1].strip()
            elif "App push Title：" in line:
                article['app_title'] = line.split("App push Title：")[1].strip()
            elif "App push Headline：" in line:
                article['app_headline'] = line.split("App push Headline：")[1].strip()
        
        if 'title' in article:
            articles.append(article)
    
    return articles

def generate_sample_articles(news_articles, num=5):
    """示範文章（當 AI 失敗時）"""
    samples = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    sample_templates = [
        {
            "title": "中美貿易關係",
            "question": "你認為中美應否尋求和解？",
            "category": "中美關係"
        },
        {
            "title": "特朗普回歸政壇",
            "question": "特朗普重返政治舞台，你有無睇好？",
            "category": "國際政治"
        },
        {
            "title": "美俄烏克蘭局勢",
            "question": "西方應否繼續支持烏克蘭？",
            "category": "美俄關係"
        },
        {
            "title": "科技競賽升級",
            "question": "你認為科技國族主義係咪必然趨勢？",
            "category": "中美關係"
        },
        {
            "title": "亞太地緣政治",
            "question": "亞太局勢緊張，香港應點樣應對？",
            "category": "國際政治"
        }
    ]
    
    for i, template in enumerate(sample_templates[:num]):
        article = {
            "date": today,
            "id": i + 1,
            "title": template['title'],
            "question": template['question'],
            "category": template['category'],
            "options": ["同意", "不同意", "部份贊同", "無意見"],
            "controversy": 70 + (i * 5),
            "hotness": 75 + (i * 4),
            "editor_statement": f"今週{template['title']}再成網絡熱話。{template['question']}呢個問題引起廣泛討論，涉及香港未來發展方向，值得深入探討。",
            "fb_feed": f"新題出爐🗳️\n\n{template['question']}\n\n唔同立場有咩理據？投票話俾我地知！",
            "fb_image_text": f"你點睇？{template['question']}",
            "banner": f"你點睇？{template['category']}",
            "footer": f"投票已截止，多謝參與！",
            "group_message": f"Hi all,\n新題已出，謝謝\n{template['question']}",
            "app_title": f"【你點睇？】{template['title']}",
            "app_headline": f"{template['question']} 投票現已開放！"
        }
        samples.append(article)
    
    return samples

def save_articles(articles, filename="voting_articles.json"):
    """保存投票議題"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(articles)} voting articles to {filename}")
    return articles

if __name__ == "__main__":
    try:
        with open("latest_news.json", 'r', encoding='utf-8') as f:
            news = json.load(f)
    except:
        print("latest_news.json not found. Run news_fetcher.py first.")
        exit(1)
    
    print("生成投票議題...")
    articles = generate_voting_articles(news, num_articles=5)
    save_articles(articles)
    
    print("\n" + "=" * 50)
    print("早晨！今日草擬咗以下題目，請大家睇睇：")
    print("=" * 50)
    for article in articles:
        print(f"\n{article.get('id', '?')}. {article['title']}")
        print(f"   問題: {article['question']}")
        print(f"   爭議度: {article.get('controversy', '?')}/100")
        print(f"   熱度: {article.get('hotness', '?')}/100")
