"""
新聞抓取模組
支持多種新聞來源：Google News RSS、自定義 RSS 源
"""
import feedparser
import requests
from datetime import datetime, timedelta
import json
from typing import List, Dict

class NewsFetcher:
    """新聞抓取器"""
    
    def __init__(self):
        # 熱門新聞 RSS 源
        self.rss_sources = {
            'bbc_chinese': 'http://feeds.bbci.co.uk/news/world/asia/china/rss.xml',
            'reuters_world': 'https://www.reutersagency.com/feed/?best-topics=news-all&post_type=best',
            'google_news_cn': 'https://news.google.com/rss/search?q=中美+OR+特朗普+OR+科技+when:7d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant',
        }
        
        # 用戶代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_from_rss(self, source_key: str = 'google_news_cn', max_articles: int = 10) -> List[Dict]:
        """從 RSS 源抓取新聞"""
        
        if source_key not in self.rss_sources:
            raise ValueError(f"未知的新聞源: {source_key}")
        
        url = self.rss_sources[source_key]
        articles = []
        
        try:
            print(f"📰 正在從 {source_key} 抓取新聞...")
            
            # 解析 RSS
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:max_articles]:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': source_key,
                    'timestamp': datetime.now().isoformat()
                }
                
                # 清理 HTML 標籤
                article['summary'] = self._clean_html(article['summary'])
                
                articles.append(article)
            
            print(f"✅ 成功抓取 {len(articles)} 篇新聞")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取新聞失敗: {e}")
            return []
    
    def fetch_from_keywords(self, keywords: List[str], max_articles: int = 10) -> List[Dict]:
        """根據關鍵詞從 Google News 抓取"""
        
        query = '+OR+'.join(keywords)
        url = f"https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        
        articles = []
        
        try:
            print(f"🔍 搜索關鍵詞: {', '.join(keywords)}")
            
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:max_articles]:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': 'google_news_keywords',
                    'keywords': keywords,
                    'timestamp': datetime.now().isoformat()
                }
                
                article['summary'] = self._clean_html(article['summary'])
                articles.append(article)
            
            print(f"✅ 找到 {len(articles)} 篇相關新聞")
            return articles
            
        except Exception as e:
            print(f"❌ 搜索失敗: {e}")
            return []
    
    def fetch_multiple_sources(self, sources: List[str] = None, max_per_source: int = 5) -> List[Dict]:
        """從多個來源抓取新聞"""
        
        if sources is None:
            sources = list(self.rss_sources.keys())
        
        all_articles = []
        
        for source in sources:
            try:
                articles = self.fetch_from_rss(source, max_per_source)
                all_articles.extend(articles)
            except Exception as e:
                print(f"⚠️  {source} 抓取失敗: {e}")
        
        # 去重（基於標題）
        seen_titles = set()
        unique_articles = []
        
        for article in all_articles:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_articles.append(article)
        
        print(f"📊 共獲取 {len(unique_articles)} 篇唯一新聞")
        return unique_articles
    
    def _clean_html(self, text: str) -> str:
        """清理 HTML 標籤"""
        import re
        
        # 移除 HTML 標籤
        clean = re.sub('<[^<]+?>', '', text)
        
        # 移除多餘空格
        clean = ' '.join(clean.split())
        
        return clean.strip()
    
    def save_to_file(self, articles: List[Dict], filename: str = None):
        """保存新聞到文件"""
        
        if filename is None:
            filename = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        print(f"💾 新聞已保存到: {filename}")
        return filename


if __name__ == "__main__":
    # 測試代碼
    fetcher = NewsFetcher()
    
    print("="*60)
    print("測試新聞抓取功能")
    print("="*60)
    
    # 測試 1: 從 Google News 抓取
    print("\n【測試 1】從 Google News 抓取熱門新聞")
    articles = fetcher.fetch_from_rss('google_news_cn', max_articles=5)
    
    if articles:
        print(f"\n前 3 篇新聞:")
        for i, article in enumerate(articles[:3], 1):
            print(f"{i}. {article['title']}")
            print(f"   {article['summary'][:100]}...")
            print()
    
    # 測試 2: 根據關鍵詞搜索
    print("\n【測試 2】根據關鍵詞搜索")
    articles = fetcher.fetch_from_keywords(['中美', '特朗普'], max_articles=5)
    
    if articles:
        print(f"\n找到 {len(articles)} 篇相關新聞")
        for i, article in enumerate(articles[:3], 1):
            print(f"{i}. {article['title']}")
            print()
    
    # 測試 3: 多來源抓取
    print("\n【測試 3】多來源抓取")
    articles = fetcher.fetch_multiple_sources(['google_news_cn'], max_per_source=3)
    
    if articles:
        print(f"\n共獲取 {len(articles)} 篇新聞")
        fetcher.save_to_file(articles)
