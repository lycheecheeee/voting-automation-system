import json
import csv
import os
from datetime import datetime

def generate_excel_report(articles_file="voting_articles.json", output_dir="output"):
    """生成 CSV 表格（Excel 相容）"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except:
        print(f"{articles_file} not found.")
        return None
    
    # CSV 檔案路徑
    csv_file = f"{output_dir}/voting_topics_{datetime.now().strftime('%Y%m%d')}.csv"
    
    # 定義欄位
    fieldnames = [
        "題號",
        "日期",
        "主題",
        "精簡背景連問法",
        "建議選項",
        "副題",
        "副題選項",
        "值得問的原因",
        "爭議度",
        "網上熱度",
        "版主聲明",
        "FB feed文字",
        "FB圖片文字",
        "Banner文稿",
        "Article footer文字",
        "Message to Voting group",
        "App push Title",
        "App push Headline"
    ]
    
    # 寫入 CSV
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, article in enumerate(articles, 1):
            row = {
                "題號": i,
                "日期": article.get('date', ''),
                "主題": article.get('title', ''),
                "精簡背景連問法": article.get('question', ''),
                "建議選項": " / ".join(article.get('options', [])),
                "副題": article.get('sub_question', ''),
                "副題選項": article.get('sub_options', ''),
                "值得問的原因": article.get('reason', ''),
                "爭議度": article.get('controversy', ''),
                "網上熱度": article.get('hotness', ''),
                "版主聲明": article.get('editor_statement', ''),
                "FB feed文字": article.get('fb_feed', ''),
                "FB圖片文字": article.get('fb_image_text', ''),
                "Banner文稿": article.get('banner', ''),
                "Article footer文字": article.get('footer', ''),
                "Message to Voting group": article.get('group_message', ''),
                "App push Title": article.get('app_title', ''),
                "App push Headline": article.get('app_headline', '')
            }
            writer.writerow(row)
    
    print(f"Generated Excel report: {csv_file}")
    return csv_file

def generate_markdown_report(articles_file="voting_articles.json", output_dir="output"):
    """生成 Markdown 報告"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        with open(articles_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except:
        return None
    
    md_file = f"{output_dir}/voting_report_{datetime.now().strftime('%Y%m%d')}.md"
    
    content = f"""# 投票議題報告
生成日期：{datetime.now().strftime('%Y年%m月%d日')}

---

## 開場白

早晨！今日草擬咗以下題目，請大家睇睇：

---

"""
    
    for i, article in enumerate(articles, 1):
        content += f"""
## {i}. {article['title']}

**日期：** {article.get('date', '')}

### 背景問題
{article.get('question', '')}

### 建議選項
{' / '.join(article.get('options', []))}

### 爭議度 & 熱度
- 爭議度：{article.get('controversy', '?')}/100
- 網上熱度：{article.get('hotness', '?')}/100

### 版主聲明
{article.get('editor_statement', '')}

### 文案

**FB Feed文字：**
```
{article.get('fb_feed', '')}
```

**FB圖片文字：**
```
{article.get('fb_image_text', '')}
```

**Banner文稿：**
```
{article.get('banner', '')}
```

**Article Footer文字：**
```
{article.get('footer', '')}
```

**Message to Voting Group：**
```
{article.get('group_message', '')}
```

**App Push：**
- Title: {article.get('app_title', '')}
- Headline: {article.get('app_headline', '')}

---

"""
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated Markdown report: {md_file}")
    return md_file

if __name__ == "__main__":
    print("生成報告...")
    
    excel = generate_excel_report()
    md = generate_markdown_report()
    
    print("\n✓ 報告已生成")
