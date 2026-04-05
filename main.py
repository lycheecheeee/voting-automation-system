#!/usr/bin/env python3
"""
主程式：整合所有模組
執行順序：抓新聞 → 生成題目 → 生成報告
"""

import sys
import json
from datetime import datetime

def main():
    print("=" * 60)
    print("🗳️  經濟通投票議題自動生成系統")
    print(f"執行時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: 抓取本週新聞
    print("\n[1/3] 抓取本週香港 + 國際政治新聞...")
    try:
        from news_fetcher import fetch_weekly_news, analyze_news_for_voting, save_news
        articles = fetch_weekly_news(days=7, max_articles=20)
        hottest = analyze_news_for_voting(articles)
        save_news(hottest)
        print(f"✓ 成功抓取 {len(hottest)} 篇高潛力新聞")
    except Exception as e:
        print(f"✗ 新聞抓取失敗: {e}")
        return False
    
    # Step 2: 生成投票議題
    print("\n[2/3] 生成投票議題...")
    try:
        from topic_generator import generate_voting_articles, save_articles
        topics = generate_voting_articles(hottest, num_articles=5)
        save_articles(topics)
        print(f"✓ 成功生成 {len(topics)} 個投票議題")
        
        print("\n" + "=" * 60)
        print("早晨！今日草擬咗以下題目，請大家睇睇：")
        print("=" * 60)
        
        for topic in topics:
            print(f"\n{topic.get('id', '?')}. {topic['title']}")
            print(f"   問題: {topic['question']}")
            print(f"   爭議度: {topic.get('controversy', '?')}/100 | 熱度: {topic.get('hotness', '?')}/100")
    except Exception as e:
        print(f"✗ 題目生成失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: 生成報告
    print("\n[3/3] 生成報告...")
    try:
        from report_generator import generate_excel_report, generate_markdown_report
        
        excel_file = generate_excel_report()
        md_file = generate_markdown_report()
        
        print(f"✓ 成功生成報告")
    except Exception as e:
        print(f"✗ 報告生成失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ 所有工作完成！")
    print("=" * 60)
    print(f"\n📂 輸出檔案:")
    print(f"  - output/voting_topics_*.csv (Excel 表格)")
    print(f"  - output/voting_report_*.md (Markdown 報告)")
    print(f"  - voting_articles.json (詳細資料)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
