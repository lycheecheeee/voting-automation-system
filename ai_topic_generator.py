"""
AI 投票議題生成器 - 修復版
支持多種 AI API，包含完善的錯誤處理和備用方案
"""
import requests
import json
from datetime import datetime
from typing import List, Dict

class AITopicGeneratorFixed:
    """AI 投票議題生成器（修復版）"""
    
    def __init__(self, api_key: str = None, api_url: str = None):
        # API 配置
        self.api_key = api_key or "sk-dmxapi-test-key"
        self.api_url = api_url or "https://api.dmxapi.com/v1/chat/completions"
        
        # API 可用性狀態
        self.api_available = False
        
        print("🔧 初始化 AI 議題生成器...")
        print(f"   API URL: {self.api_url}")
        print(f"   API Key: {self.api_key[:20]}..." if len(self.api_key) > 20 else f"   API Key: {self.api_key}")
    
    def generate_topics_from_news(self, news_articles: List[Dict], max_topics: int = 5) -> List[Dict]:
        """從新聞生成投票議題"""
        
        print(f"\n🤖 正在分析 {len(news_articles)} 篇新聞...")
        
        if not news_articles:
            print("⚠️  沒有新聞數據，使用備用方案")
            return self._generate_fallback_topics(max_topics)
        
        try:
            # 嘗試使用 AI API
            print("📡 嘗試調用 AI API...")
            topics = self._try_generate_with_ai(news_articles, max_topics)
            
            if topics:
                print(f"✅ AI 成功生成 {len(topics)} 個議題")
                return topics
            else:
                print("⚠️  AI 生成失敗，使用備用方案")
                return self._generate_fallback_topics(max_topics)
                
        except Exception as e:
            print(f"❌ AI 生成異常: {e}")
            print("🔄 切換到備用方案...")
            return self._generate_fallback_topics(max_topics)
    
    def _try_generate_with_ai(self, news_articles: List[Dict], max_topics: int) -> List[Dict]:
        """嘗試使用 AI API 生成"""
        
        # 準備新聞內容
        news_context = self._prepare_news_context(news_articles)
        
        # 構建提示詞
        system_prompt = """你是一位專業的新聞編輯。根據新聞生成投票議題，返回 JSON 數組。
每個議題包含：title, question, category, options(4個), controversy(0-100), hotness(0-100), reason"""
        
        user_prompt = f"""根據以下新聞生成 {max_topics} 個繁體中文投票議題：

{news_context}

只返回 JSON 數組，不要其他文字。"""
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "moonshot-v1-8k",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 3000
            }
            
            print("📤 發送請求到 AI API...")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"⚠️  API 返回錯誤: {response.status_code}")
                print(f"   回應: {response.text[:200]}")
                return []
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print("📥 收到 AI 回應")
            
            # 解析 JSON
            topics = self._parse_json_response(content)
            
            if topics:
                # 添加元數據
                for i, topic in enumerate(topics, 1):
                    topic['id'] = i
                    topic['date'] = datetime.now().strftime('%Y-%m-%d')
                
                return topics[:max_topics]
            else:
                return []
                
        except requests.exceptions.Timeout:
            print("⏱️  API 請求超時")
            return []
        except requests.exceptions.ConnectionError:
            print("🌐 網絡連接失敗")
            return []
        except Exception as e:
            print(f"❌ API 調用失敗: {e}")
            return []
    
    def _generate_fallback_topics(self, max_topics: int) -> List[Dict]:
        """備用方案：生成示範議題"""
        
        print("\n📝 使用備用方案生成示範議題...")
        
        fallback_topics = [
            {
                "id": 1,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "title": "中美貿易關係",
                "question": "你認為中美貿易關係未來會如何發展？",
                "category": "中美關係",
                "options": ["持續改善", "保持現狀", "進一步惡化", "難以預測"],
                "controversy": 78,
                "hotness": 85,
                "reason": "中美貿易戰持續影響全球經濟格局。",
                "editor_statement": "中美貿易關係是當前國際關注的焦點。雙方在多個領域存在分歧，但也有合作空間。",
                "fb_feed": "新題出爐🗳️\n\n你認為中美貿易關係未來會如何發展？\n\n投票話俾我地知！\n\n#中美貿易",
                "fb_image_text": "你點睇？中美貿易關係未來",
                "banner": "你點睇？中美貿易",
                "footer": "投票已截止，多謝參與！",
                "group_message": "Hi all,\n新題已出，謝謝\n你認為中美貿易關係未來會如何發展？",
                "app_title": "【你點睇？】中美貿易",
                "app_headline": "中美貿易關係未來會如何發展？投票現已開放！"
            },
            {
                "id": 2,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "title": "人工智能監管",
                "question": "政府應否加強對 AI 技術的監管？",
                "category": "科技競賽",
                "options": ["應該加強", "適度監管", "不需監管", "無意見"],
                "controversy": 82,
                "hotness": 90,
                "reason": "AI 技術快速發展引發監管討論。",
                "editor_statement": "人工智能技術日新月異，帶來便利的同時也引發隱私、安全等擔憂。",
                "fb_feed": "新題出爐🗳️\n\n政府應否加強對 AI 技術的監管？\n\n投票話俾我地知！\n\n#AI監管",
                "fb_image_text": "你點睇？AI 技術監管",
                "banner": "你點睇？AI 監管",
                "footer": "投票已截止，多謝參與！",
                "group_message": "Hi all,\n新題已出，謝謝\n政府應否加強對 AI 技術的監管？",
                "app_title": "【你點睇？】AI 監管",
                "app_headline": "政府應否加強對 AI 技術的監管？投票現已開放！"
            },
            {
                "id": 3,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "title": "氣候變化行動",
                "question": "個人應否為減緩氣候變化做出更多努力？",
                "category": "社會",
                "options": ["應該多做", "已經足夠", "主要靠政府", "無意見"],
                "controversy": 65,
                "hotness": 72,
                "reason": "氣候變化問題日益嚴峻。",
                "editor_statement": "全球氣候變化帶來極端天氣頻發，個人行動與政府政策同樣重要。",
                "fb_feed": "新題出爐🗳️\n\n個人應否為減緩氣候變化做出更多努力？\n\n投票話俾我地知！\n\n#氣候變化",
                "fb_image_text": "你點睇？氣候變化行動",
                "banner": "你點睇？氣候行動",
                "footer": "投票已截止，多謝參與！",
                "group_message": "Hi all,\n新題已出，謝謝\n個人應否為減緩氣候變化做出更多努力？",
                "app_title": "【你點睇？】氣候行動",
                "app_headline": "個人應否為減緩氣候變化做出更多努力？投票現已開放！"
            },
            {
                "id": 4,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "title": "遠程工作趨勢",
                "question": "疫情後遠程工作會成為常態嗎？",
                "category": "經濟",
                "options": ["會成為常態", "部分行業", "不會普及", "無意見"],
                "controversy": 70,
                "hotness": 80,
                "reason": "疫情改變了工作方式。",
                "editor_statement": "遠程工作在疫情期間迅速普及，但長期來看是否可持續仍有爭議。",
                "fb_feed": "新題出爐🗳️\n\n疫情後遠程工作會成為常態嗎？\n\n投票話俾我地知！\n\n#遠程工作",
                "fb_image_text": "你點睇？遠程工作趨勢",
                "banner": "你點睇？遠程工作",
                "footer": "投票已截止，多謝參與！",
                "group_message": "Hi all,\n新題已出，謝謝\n疫情後遠程工作會成為常態嗎？",
                "app_title": "【你點睇？】遠程工作",
                "app_headline": "疫情後遠程工作會成為常態嗎？投票現已開放！"
            },
            {
                "id": 5,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "title": "社交媒體影響",
                "question": "社交媒體對青少年影響利大於弊嗎？",
                "category": "社會",
                "options": ["利大於弊", "弊大於利", "利弊相當", "無意見"],
                "controversy": 88,
                "hotness": 92,
                "reason": "社交媒體普及率持續上升。",
                "editor_statement": "社交媒體已成為青少年生活的重要部分，其影響引發廣泛討論。",
                "fb_feed": "新題出爐🗳️\n\n社交媒體對青少年影響利大於弊嗎？\n\n投票話俾我地知！\n\n#社交媒體",
                "fb_image_text": "你點睇？社交媒體影響",
                "banner": "你點睇？社交媒體",
                "footer": "投票已截止，多謝參與！",
                "group_message": "Hi all,\n新題已出，謝謝\n社交媒體對青少年影響利大於弊嗎？",
                "app_title": "【你點睇？】社交媒體",
                "app_headline": "社交媒體對青少年影響利大於弊嗎？投票現已開放！"
            }
        ]
        
        # 返回請求數量的議題
        result = fallback_topics[:max_topics]
        
        print(f"✅ 備用方案生成 {len(result)} 個議題")
        
        return result
    
    def _prepare_news_context(self, articles: List[Dict]) -> str:
        """準備新聞上下文"""
        
        context_parts = []
        
        for i, article in enumerate(articles[:10], 1):
            title = article.get('title', '')
            summary = article.get('summary', '')[:200]
            
            context_parts.append(f"{i}. {title}\n   {summary}")
        
        return "\n\n".join(context_parts)
    
    def _parse_json_response(self, response_text: str) -> List[Dict]:
        """解析 JSON 回應"""
        
        try:
            # 嘗試直接解析
            topics = json.loads(response_text)
            
            if isinstance(topics, list):
                return topics
            elif isinstance(topics, dict):
                return [topics]
            else:
                return []
                
        except json.JSONDecodeError:
            # 嘗試提取 JSON
            import re
            
            # 查找 JSON 數組
            json_match = re.search(r'\[\s*\{.*\}\s*\]', response_text, re.DOTALL)
            
            if json_match:
                try:
                    topics = json.loads(json_match.group())
                    return topics if isinstance(topics, list) else [topics]
                except:
                    pass
            
            print("⚠️  無法解析 JSON")
            return []
    
    def save_topics_to_file(self, topics: List[Dict], filename: str = None):
        """保存議題到文件"""
        
        if filename is None:
            filename = f"voting_topics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
        
        print(f"💾 議題已保存到: {filename}")
        return filename


if __name__ == "__main__":
    # 測試代碼
    from news_fetcher import NewsFetcher
    
    print("="*60)
    print("測試 AI 議題生成器（修復版）")
    print("="*60)
    
    # 步驟 1: 抓取新聞
    print("\n【步驟 1】抓取新聞")
    fetcher = NewsFetcher()
    articles = fetcher.fetch_from_rss('google_news_cn', max_articles=3)
    
    if not articles:
        print("⚠️  未能抓取新聞，使用空列表測試備用方案")
        articles = []
    
    # 步驟 2: 生成議題
    print("\n【步驟 2】AI 生成投票議題")
    generator = AITopicGeneratorFixed()
    topics = generator.generate_topics_from_news(articles, max_topics=3)
    
    if topics:
        print(f"\n✅ 生成了 {len(topics)} 個議題:")
        for i, topic in enumerate(topics, 1):
            print(f"\n{i}. {topic.get('title', '未知')}")
            print(f"   問題: {topic.get('question', '')}")
            print(f"   爭議度: {topic.get('controversy', 0)}")
            print(f"   熱度: {topic.get('hotness', 0)}")
        
        # 保存
        generator.save_topics_to_file(topics)
    else:
        print("❌ 未能生成議題")
