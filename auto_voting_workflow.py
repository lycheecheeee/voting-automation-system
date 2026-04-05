"""
自動化新聞抓取 + AI 生成投票議題 + NVIDIA 圖片生成
完整的一鍵自動化流程 - 修復版
"""
import sys
import os
from datetime import datetime

# 添加路徑
sys.path.append(os.path.dirname(__file__))

from news_fetcher import NewsFetcher
try:
    from ai_topic_generator import AITopicGeneratorFixed as AITopicGenerator
    print("✅ 使用修復版 AI 議題生成器")
except ImportError:
    try:
        from ai_topic_generator import AITopicGenerator
        print("⚠️  使用原版 AI 議題生成器")
    except ImportError:
        print("❌ 無法導入 AI 議題生成器")
        AITopicGenerator = None

try:
    from nvidia_image_generator import generate_all_images_nvidia
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False
    print("⚠️  NVIDIA 圖像生成器不可用")

import json

class AutoVotingWorkflow:
    """自動化投票議題生成工作流（修復版）"""
    
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        if AITopicGenerator:
            self.topic_generator = AITopicGenerator()
        else:
            self.topic_generator = None
        self.generated_topics = []
        self.generated_images = []
    
    def run_full_workflow(self, 
                         keywords: list = None,
                         max_news: int = 10,
                         max_topics: int = 5,
                         use_nvidia: bool = True,
                         save_results: bool = True):
        """
        執行完整工作流程
        
        參數:
            keywords: 搜索關鍵詞列表
            max_news: 最多抓取的新聞數量
            max_topics: 最多生成的議題數量
            use_nvidia: 是否使用 NVIDIA API 生成圖片
            save_results: 是否保存結果到文件
        """
        
        print("\n" + "="*70)
        print("🚀 自動化投票議題生成系統（修復版）")
        print("="*70)
        
        start_time = datetime.now()
        
        try:
            # 步驟 1: 抓取新聞
            print("\n【步驟 1/4】📰 抓取最新新聞")
            print("-" * 70)
            
            if keywords:
                news_articles = self.news_fetcher.fetch_from_keywords(
                    keywords, 
                    max_articles=max_news
                )
            else:
                news_articles = self.news_fetcher.fetch_multiple_sources(
                    ['google_news_cn'],
                    max_per_source=max_news
                )
            
            if not news_articles:
                print("⚠️  未能抓取到新聞，將使用備用方案生成議題")
                news_articles = []
            else:
                print(f"✅ 成功抓取 {len(news_articles)} 篇新聞")
            
            # 保存新聞
            news_file = None
            if save_results and news_articles:
                news_file = self.news_fetcher.save_to_file(news_articles)
            
            # 步驟 2: AI 生成議題
            print("\n【步驟 2/4】🤖 AI 分析並生成投票議題")
            print("-" * 70)
            
            if self.topic_generator:
                topics = self.topic_generator.generate_topics_from_news(
                    news_articles,
                    max_topics=max_topics
                )
            else:
                print("❌ AI 議題生成器不可用")
                topics = []
            
            if not topics:
                print("❌ 未能生成議題")
                return False
            
            self.generated_topics = topics
            print(f"✅ 成功生成 {len(topics)} 個投票議題")
            
            # 顯示議題預覽
            print("\n📋 生成的議題:")
            for i, topic in enumerate(topics, 1):
                print(f"  {i}. {topic.get('title', '未知')}")
                print(f"     {topic.get('question', '')[:60]}...")
            
            # 保存議題
            topics_file = None
            if save_results:
                topics_file = self.topic_generator.save_topics_to_file(topics)
            
            # 步驟 3: 生成圖片
            print("\n【步驟 3/4】🎨 生成投票圖片")
            print("-" * 70)
            
            images = []
            
            if use_nvidia and NVIDIA_AVAILABLE:
                print("使用 NVIDIA Stable Diffusion 3 生成圖片...")
                try:
                    images = generate_all_images_nvidia(topics, "output_images")
                except Exception as e:
                    print(f"⚠️  NVIDIA 生成失敗: {e}")
                    print("切換到本地生成器...")
                    from image_generator import generate_all_images
                    images = generate_all_images(topics, "output_images")
            else:
                print("使用本地 PIL 生成器...")
                try:
                    from image_generator import generate_all_images
                    images = generate_all_images(topics, "output_images")
                except Exception as e:
                    print(f"⚠️  本地生成失敗: {e}")
                    images = []
            
            self.generated_images = images
            print(f"✅ 成功生成 {len(images)} 張圖片")
            
            # 步驟 4: 生成報告
            print("\n【步驟 4/4】📊 生成總結報告")
            print("-" * 70)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': duration,
                'news_count': len(news_articles),
                'topics_count': len(topics),
                'images_count': len(images),
                'keywords_used': keywords or ['自動'],
                'news_file': news_file if save_results else None,
                'topics_file': topics_file if save_results else None,
                'images_dir': 'output_images',
                'topics': [
                    {
                        'id': t.get('id'),
                        'title': t.get('title'),
                        'question': t.get('question'),
                        'category': t.get('category'),
                        'controversy': t.get('controversy'),
                        'hotness': t.get('hotness')
                    }
                    for t in topics
                ]
            }
            
            # 打印報告
            print(f"\n⏱️  總耗時: {duration:.1f} 秒")
            print(f"📰 抓取新聞: {len(news_articles)} 篇")
            print(f"📝 生成議題: {len(topics)} 個")
            print(f"🖼️  生成圖片: {len(images)} 張")
            
            if save_results:
                report_file = f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                print(f"💾 報告已保存: {report_file}")
            
            print("\n" + "="*70)
            print("✅ 自動化流程完成！")
            print("="*70)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 流程執行失敗: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函數"""
    
    print("\n" + "="*70)
    print("🚀 自動化投票議題生成系統（修復版）")
    print("="*70)
    print("\n這個系統將自動：")
    print("  ✅ 抓取最新新聞")
    print("  ✅ AI 分析並生成投票議題（含備用方案）")
    print("  ✅ 使用 NVIDIA API 生成高質量圖片")
    print("  ✅ 一鍵完成整個流程")
    print("="*70)
    
    # 創建工作流實例
    workflow = AutoVotingWorkflowFixed()
    
    # 詢問用戶輸入
    print("\n請選擇關鍵詞（用逗號分隔，直接回車使用默認）:")
    user_input = input("關鍵詞: ").strip()
    
    if user_input:
        keywords = [k.strip() for k in user_input.split(',')]
    else:
        keywords = ['中美', '特朗普', '科技', '經濟']
    
    print(f"\n使用的關鍵詞: {', '.join(keywords)}")
    
    # 詢問生成數量
    max_topics_input = input("\n要生成多少個議題？(默認 5): ").strip()
    max_topics = int(max_topics_input) if max_topics_input.isdigit() else 5
    
    # 詢問是否使用 NVIDIA
    use_nvidia_input = input("使用 NVIDIA AI 生成圖片？(y/n, 默認 y): ").strip().lower()
    use_nvidia = use_nvidia_input != 'n'
    
    # 執行工作流
    success = workflow.run_full_workflow(
        keywords=keywords,
        max_news=10,
        max_topics=max_topics,
        use_nvidia=use_nvidia,
        save_results=True
    )
    
    if success:
        print("\n🎉 所有步驟完成！")
        print(f"\n下一步:")
        print(f"  1. 重啟 Flask 伺服器以加載新議題")
        print(f"  2. 訪問 http://localhost:5000 查看結果")
        print(f"  3. 訪問 http://localhost:5000/nvidia-gen 查看圖片")
    else:
        print("\n❌ 流程失敗，請檢查錯誤信息")
    
    return success


if __name__ == "__main__":
    main()
