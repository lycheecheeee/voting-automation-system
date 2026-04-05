import json
import os
from datetime import datetime

def generate_html_report(news_file="news.json", topics_file="voting_topics.json", 
                         images_dir="output_images", output_file="voting_report.html"):
    """生成 HTML 報告"""
    
    # 讀取數據
    try:
        with open(news_file, 'r', encoding='utf-8') as f:
            news = json.load(f)
    except:
        news = []
    
    try:
        with open(topics_file, 'r', encoding='utf-8') as f:
            topics = json.load(f)
    except:
        topics = []
    
    # HTML 模板
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投票工作報告 - {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{ 
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 36px; margin-bottom: 10px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .section {{ margin-bottom: 50px; }}
        .section h2 {{ 
            font-size: 24px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .news-item {{
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        .news-item h3 {{ color: #667eea; font-size: 16px; margin-bottom: 8px; }}
        .news-item p {{ font-size: 13px; color: #666; line-height: 1.6; }}
        .news-item .source {{ color: #999; font-size: 12px; margin-top: 8px; }}
        .voting-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        .voting-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .voting-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #667eea;
        }}
        .voting-card h3 {{ color: #667eea; margin-bottom: 15px; font-size: 16px; }}
        .voting-card .question {{ font-weight: bold; color: #333; margin-bottom: 15px; }}
        .voting-card .option {{
            padding: 10px;
            margin: 8px 0;
            background: #f5f5f5;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .voting-card .option:hover {{ background: #e8eaf6; }}
        .image-placeholder {{
            text-align: center;
            margin-top: 15px;
        }}
        .image-placeholder img {{
            max-width: 100%;
            border-radius: 4px;
            margin-top: 10px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗳️ 投票工作報告</h1>
            <p>生成於 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>
        
        <div class="content">
            <!-- 新聞來源 -->
            <div class="section">
                <h2>📰 今週國際新聞摘要</h2>
                {''.join([f'''
                <div class="news-item">
                    <h3>{article['title']}</h3>
                    <p>{article['summary']}</p>
                    <div class="source">📌 {article['source']} | {article['published'][:10]}</div>
                </div>
                ''' for article in news[:8]])}
            </div>
            
            <!-- 投票題目 -->
            <div class="section">
                <h2>🎯 生成嘅投票題目 ({len(topics)} 個)</h2>
                <div class="voting-section">
                    {''.join([f'''
                    <div class="voting-card">
                        <h3>投票 #{topic['id']}</h3>
                        <div class="question">{topic['question']}</div>
                        {''.join([f'<div class="option">○ {opt}</div>' for opt in topic['options']])}
                        <div class="image-placeholder">
                            {f'<img src="{images_dir}/voting_{topic['id']}.png" alt="投票圖片 {topic['id']}">' if os.path.exists(f'{images_dir}/voting_{topic['id']}.png') else ''}
                        </div>
                    </div>
                    ''' for topic in topics])}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>自動化投票工作系統 | 每週一早上 9 點生成</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存 HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated report: {output_file}")
    return output_file

if __name__ == "__main__":
    print("Generating HTML report...")
    generate_html_report()
