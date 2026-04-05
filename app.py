from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS
from datetime import datetime
import json
import csv
import os
from io import StringIO, BytesIO
from image_generator import generate_all_images
try:
    from nvidia_image_generator import generate_all_images_nvidia
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False

# 導入自動化模組
try:
    from news_fetcher import NewsFetcher
    from ai_topic_generator import AITopicGenerator
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False

import threading

app = Flask(__name__)
CORS(app)  # 啟用 CORS 支持

# Google Drive 設定
GOOGLE_DRIVE_FOLDER_ID = "1iTngyUVgE7suUZ9ChA1QZhyVr6bGK5VH"

# 示範投票數據
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
        "reason": "中美貿易戰持續升溫，影響全球經濟。",
        "editor_statement": "本週中美關係再成網絡熱話。在全球政治格局轉變下，中美和解的可能性成為各界關注焦點。",
        "fb_feed": "新題出爐🗳️\n\n你認為中美應否尋求和解？\n\n投票話俾我地知！\n\n#中美關係",
        "fb_image_text": "你點睇？中美應否尋求和解？",
        "banner": "你點睇？中美關係",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n你認為中美應否尋求和解？",
        "app_title": "【你點睇？】中美關係",
        "app_headline": "你認為中美應否尋求和解？投票現已開放！"
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
        "reason": "特朗普作為前美國總統再次涉足政治。",
        "editor_statement": "特朗普重返政治舞台，引起全球矚目。其貿易保護主義政策、對華態度等，將深遠影響亞太局勢。",
        "fb_feed": "新題出爐🗳️\n\n特朗普重返政治舞台，你有無睇好？\n\n投票話俾我地知！\n\n#特朗普",
        "fb_image_text": "你點睇？特朗普重返政治舞台",
        "banner": "你點睇？特朗普回歸",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n特朗普重返政治舞台，你有無睇好？",
        "app_title": "【你點睇？】特朗普回歸",
        "app_headline": "特朗普重返政治舞台，你有無睇好？投票現已開放！"
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
        "editor_statement": "烏克蘭局勢持續演變，西方國家的援助政策引起激烈辯論。",
        "fb_feed": "新題出爐🗳️\n\n西方應否繼續支持烏克蘭？\n\n投票話俾我地知！\n\n#烏克蘭",
        "fb_image_text": "你點睇？西方應否支持烏克蘭",
        "banner": "你點睇？烏克蘭局勢",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n西方應否繼續支持烏克蘭？",
        "app_title": "【你點睇？】烏克蘭局勢",
        "app_headline": "西方應否繼續支持烏克蘭？投票現已開放！"
    },
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 4,
        "title": "科技競賽升級",
        "question": "你認為科技國族主義係咪必然趨勢？",
        "category": "中美關係",
        "options": ["係必然趨勢", "唔係必然", "因情況而異", "無意見"],
        "controversy": 72,
        "hotness": 82,
        "reason": "中美科技戰升級，芯片、AI等領域成為競爭焦點。",
        "editor_statement": "科技競賽成為中美競爭的新戰場。國族主義色彩日濃。",
        "fb_feed": "新題出爐🗳️\n\n你認為科技國族主義係咪必然趨勢？\n\n投票話俾我地知！\n\n#科技競賽",
        "fb_image_text": "你點睇？科技國族主義趨勢",
        "banner": "你點睇？科技競賽",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n你認為科技國族主義係咪必然趨勢？",
        "app_title": "【你點睇？】科技競賽",
        "app_headline": "科技國族主義是必然趨勢嗎？投票現已開放！"
    },
    {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "id": 5,
        "title": "亞太地緣政治",
        "question": "亞太局勢緊張，香港應點樣應對？",
        "category": "國際政治",
        "options": ["加強防守", "尋求平衡", "遠離競爭", "無意見"],
        "controversy": 80,
        "hotness": 78,
        "reason": "台灣問題升溫，南海局勢緊張。",
        "editor_statement": "亞太地區已成為全球最具戰略意義的地帶。",
        "fb_feed": "新題出爐🗳️\n\n亞太局勢緊張，香港應點樣應對？\n\n投票話俾我地知！\n\n#香港前景",
        "fb_image_text": "你點睇？香港應點樣應對亞太局勢",
        "banner": "你點睇？香港出路",
        "footer": "投票已截止，多謝參與！",
        "group_message": "Hi all,\n新題已出，謝謝\n亞太局勢緊張，香港應點樣應對？",
        "app_title": "【你點睇？】亞太局勢",
        "app_headline": "亞太局勢緊張，香港應點樣應對？投票現已開放！"
    }
]

# 全局狀態
upload_status = {
    'in_progress': False,
    'status': '就緒',
    'timestamp': None,
    'files': []
}

# 自動化流程狀態
automation_status = {
    'running': False,
    'progress': 0,
    'message': '',
    'result': None
}

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/nvidia-gen')
def nvidia_gen():
    """NVIDIA 圖像生成頁面"""
    return render_template('nvidia_gen.html')

@app.route('/auto-generate')
def auto_generate_page():
    """自動化生成頁面"""
    return render_template('auto_generate.html')

@app.route('/api/auto-generate', methods=['POST'])
def api_auto_generate():
    """API: 自動化生成投票議題"""
    
    if not AUTOMATION_AVAILABLE:
        return jsonify({
            'success': False,
            'error': '自動化模組未安裝'
        }), 500
    
    try:
        data = request.json or {}
        
        keywords = data.get('keywords', ['中美', '特朗普', '科技'])
        max_news = data.get('max_news', 10)
        max_topics = data.get('max_topics', 5)
        use_nvidia = data.get('use_nvidia', True)
        
        # 在後台線程中執行
        def run_automation():
            global automation_status, SAMPLE_ARTICLES
            
            automation_status['running'] = True
            automation_status['progress'] = 0
            automation_status['message'] = '開始執行...'
            
            try:
                from auto_voting_workflow import AutoVotingWorkflow
                
                workflow = AutoVotingWorkflow()
                
                # 步驟 1: 抓取新聞
                automation_status['progress'] = 10
                automation_status['message'] = '正在抓取新聞...'
                
                news_fetcher = NewsFetcher()
                news_articles = news_fetcher.fetch_from_keywords(keywords, max_articles=max_news)
                
                if not news_articles:
                    raise Exception("未能抓取到新聞")
                
                # 步驟 2: AI 生成議題
                automation_status['progress'] = 40
                automation_status['message'] = 'AI 分析中...'
                
                topic_generator = AITopicGenerator()
                topics = topic_generator.generate_topics_from_news(news_articles, max_topics=max_topics)
                
                if not topics:
                    raise Exception("未能生成議題")
                
                # 步驟 3: 生成圖片
                automation_status['progress'] = 70
                automation_status['message'] = '生成圖片中...'
                
                if use_nvidia and NVIDIA_AVAILABLE:
                    images = generate_all_images_nvidia(topics, "output_images")
                else:
                    images = generate_all_images(topics, "output_images")
                
                # 步驟 4: 更新全局變量
                automation_status['progress'] = 90
                automation_status['message'] = '更新系統...'
                
                # 為議題添加 ID 和日期
                for i, topic in enumerate(topics, 1):
                    topic['id'] = i
                    topic['date'] = datetime.now().strftime('%Y-%m-%d')
                
                # 更新 SAMPLE_ARTICLES
                SAMPLE_ARTICLES = topics
                
                automation_status['progress'] = 100
                automation_status['message'] = '完成！'
                automation_status['result'] = {
                    'news_count': len(news_articles),
                    'topics_count': len(topics),
                    'images_count': len(images),
                    'topics': topics
                }
                
            except Exception as e:
                automation_status['message'] = f'錯誤: {str(e)}'
                automation_status['result'] = None
            finally:
                automation_status['running'] = False
        
        # 啟動後台線程
        thread = threading.Thread(target=run_automation)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': '自動化流程已啟動'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/automation-status')
def get_automation_status():
    """獲取自動化流程狀態"""
    return jsonify(automation_status)

@app.route('/api/generate', methods=['POST'])
def generate_articles():
    """生成投票議題 + 圖片 + 上傳 Drive"""
    try:
        # 檢查是否使用 NVIDIA API
        use_nvidia = request.json.get('use_nvidia', False) if request.is_json else False
        
        # 生成圖片
        print("\n生成投票圖片...")
        if use_nvidia and NVIDIA_AVAILABLE:
            print("🎨 使用 NVIDIA Stable Diffusion 3 生成圖片")
            images = generate_all_images_nvidia(SAMPLE_ARTICLES, "output_images")
        else:
            print("🎨 使用本地 PIL 生成圖片")
            images = generate_all_images(SAMPLE_ARTICLES, "output_images")
        
        # 生成 CSV
        csv_path = generate_csv()
        
        # 生成 JSON
        json_path = generate_json()
        
        # 後台上傳到 Google Drive
        threading.Thread(
            target=upload_to_drive_async,
            args=(csv_path, json_path, "output_images")
        ).start()
        
        return jsonify({
            'success': True,
            'message': '投票議題已生成，正在上傳到 Google Drive...',
            'articles': SAMPLE_ARTICLES,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'images_count': len(images),
            'generator': 'nvidia' if (use_nvidia and NVIDIA_AVAILABLE) else 'local'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/articles')
def get_articles():
    """獲取所有投票議題"""
    return jsonify({
        'success': True,
        'articles': SAMPLE_ARTICLES,
        'total': len(SAMPLE_ARTICLES)
    })

@app.route('/api/article/<int:article_id>')
def get_article(article_id):
    """獲取單個投票議題"""
    article = next((a for a in SAMPLE_ARTICLES if a['id'] == article_id), None)
    if article:
        # 檢查是否有對應圖片
        image_path = f"output_images/voting_{article_id}_{datetime.now().strftime('%Y%m%d')}.png"
        if os.path.exists(image_path):
            article['image_url'] = f"/api/image/{article_id}"
        
        return jsonify({'success': True, 'article': article})
    return jsonify({'success': False, 'error': 'Article not found'}), 404

@app.route('/api/image/<int:article_id>')
def get_image(article_id):
    """取得投票圖片"""
    image_path = f"output_images/voting_{article_id}_{datetime.now().strftime('%Y%m%d')}.png"
    
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    
    # 如果今天還沒生成，嘗試找最近的
    import glob
    matching_files = glob.glob(f"output_images/voting_{article_id}_*.png")
    if matching_files:
        return send_file(matching_files[-1], mimetype='image/png')
    
    return jsonify({'error': 'Image not found'}), 404

@app.route('/api/export/csv')
def export_csv():
    """匯出 CSV"""
    csv_path = generate_csv()
    return send_file(csv_path, mimetype='text/csv', as_attachment=True, 
                     download_name=f'voting_topics_{datetime.now().strftime("%Y%m%d")}.csv')

@app.route('/api/export/json')
def export_json():
    """匯出 JSON"""
    json_path = generate_json()
    return send_file(json_path, mimetype='application/json', as_attachment=True,
                     download_name=f'voting_articles_{datetime.now().strftime("%Y%m%d")}.json')

@app.route('/api/stats')
def get_stats():
    """獲取統計資訊"""
    return jsonify({
        'total_articles': len(SAMPLE_ARTICLES),
        'avg_controversy': round(sum(a['controversy'] for a in SAMPLE_ARTICLES) / len(SAMPLE_ARTICLES), 1),
        'avg_hotness': round(sum(a['hotness'] for a in SAMPLE_ARTICLES) / len(SAMPLE_ARTICLES), 1),
        'categories': list(set(a['category'] for a in SAMPLE_ARTICLES))
    })

@app.route('/api/upload-status')
def get_upload_status():
    """獲取上傳狀態"""
    return jsonify(upload_status)

@app.route('/health')
def health():
    """健康檢查"""
    return jsonify({
        'status': 'ok', 
        'timestamp': datetime.now().isoformat(),
        'nvidia_available': NVIDIA_AVAILABLE,
        'automation_available': AUTOMATION_AVAILABLE
    })

# 輔助函數

def generate_csv():
    """生成 CSV"""
    csv_path = f"output/voting_topics_{datetime.now().strftime('%Y%m%d')}.csv"
    
    os.makedirs("output", exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['題號', '日期', '主題', '精簡背景連問法', '建議選項', '爭議度', '網上熱度',
                     '版主聲明', 'FB feed文字', 'FB圖片文字', 'Banner文稿', 'Article footer文字',
                     'Message to Voting group', 'App push Title', 'App push Headline']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for article in SAMPLE_ARTICLES:
            writer.writerow({
                '題號': article['id'],
                '日期': article['date'],
                '主題': article['title'],
                '精簡背景連問法': article['question'],
                '建議選項': ' / '.join(article['options']),
                '爭議度': article['controversy'],
                '網上熱度': article['hotness'],
                '版主聲明': article['editor_statement'],
                'FB feed文字': article['fb_feed'],
                'FB圖片文字': article['fb_image_text'],
                'Banner文稿': article['banner'],
                'Article footer文字': article['footer'],
                'Message to Voting group': article['group_message'],
                'App push Title': article['app_title'],
                'App push Headline': article['app_headline']
            })
    
    return csv_path

def generate_json():
    """生成 JSON"""
    json_path = f"output/voting_articles_{datetime.now().strftime('%Y%m%d')}.json"
    
    os.makedirs("output", exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_ARTICLES, f, ensure_ascii=False, indent=2)
    
    return json_path

def upload_to_drive_async(csv_path, json_path, images_dir):
    """後台上傳到 Google Drive"""
    global upload_status
    
    upload_status['in_progress'] = True
    upload_status['status'] = '正在連接 Google Drive...'
    upload_status['timestamp'] = datetime.now().isoformat()
    
    try:
        from google_drive_uploader import GoogleDriveUploader
        
        uploader = GoogleDriveUploader()
        upload_status['status'] = '正在上傳檔案...'
        
        # 建立本週資料夾
        week_folder_name = f"投票_{datetime.now().strftime('%Y%m%d')}"
        week_folder_id = uploader.create_folder(week_folder_name, GOOGLE_DRIVE_FOLDER_ID)
        
        uploaded_files = []
        
        # 上傳 CSV
        if os.path.exists(csv_path):
            result = uploader.upload_file(csv_path, week_folder_id)
            if result:
                uploaded_files.append(result)
        
        # 上傳 JSON
        if os.path.exists(json_path):
            result = uploader.upload_file(json_path, week_folder_id)
            if result:
                uploaded_files.append(result)
        
        # 上傳圖片
        if os.path.isdir(images_dir):
            upload_status['status'] = '正在上傳圖片...'
            for file_name in os.listdir(images_dir):
                if file_name.endswith('.png'):
                    file_path = os.path.join(images_dir, file_name)
                    result = uploader.upload_file(file_path, week_folder_id)
                    if result:
                        uploaded_files.append(result)
        
        upload_status['status'] = '✓ 上傳完成'
        upload_status['files'] = uploaded_files
        
    except Exception as e:
        upload_status['status'] = f'✗ 上傳失敗: {str(e)}'
    finally:
        upload_status['in_progress'] = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
