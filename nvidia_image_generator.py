"""
NVIDIA Stable Diffusion 3 圖像生成器
用於生成投票議題圖片
"""
import requests
import os
from datetime import datetime
import json

# NVIDIA API 配置
NVIDIA_API_KEY = "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"
NVIDIA_API_URL = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"

def generate_prompt_from_article(article):
    """根據投票議題生成英文提示詞"""
    
    # 提取關鍵信息
    title = article.get('title', '')
    question = article.get('question', '')
    category = article.get('category', '')
    
    # 構建專業的新聞風格提示詞
    prompt = f"""Professional news infographic style, clean modern design:
    
Main topic: {title}
Question: {question}
Category: {category}

Visual elements:
- Bold typography with traditional Chinese characters
- Red and white color scheme (economic news style)
- Professional layout with clear hierarchy
- Modern minimalist design
- High contrast for readability
- Economic/financial news aesthetic
- Clean geometric shapes
- Professional voting poll design

Style: Editorial design, news media, professional infographic
Quality: High resolution, sharp text, clean lines
Composition: Balanced layout with space for text overlay
"""
    
    return prompt.strip()

def generate_negative_prompt():
    """生成負面提示詞以避免不良結果"""
    return """blurry, low quality, distorted text, unreadable, messy, 
cluttered, amateur, poor lighting, watermark, signature, 
ugly, deformed, noisy, pixelated, low resolution"""

def call_nvidia_api(prompt, negative_prompt=None, steps=30, guidance_scale=7.5):
    """調用 NVIDIA Stable Diffusion 3 API"""
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # NVIDIA NIM API 正確格式
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt if negative_prompt else generate_negative_prompt(),
        "cfg_scale": guidance_scale,
        "steps": steps,
        "aspect_ratio": "1:1",
        "seed": None
    }
    
    print(f"📤 正在調用 NVIDIA API...")
    print(f"   提示詞長度: {len(prompt)} 字符")
    
    try:
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        # 檢查回應格式 - NVIDIA API 返回 "image" 字段
        if 'image' in result:
            # Base64 編碼的圖片
            import base64
            image_data = result['image']
            
            # 如果是 base64 格式
            if isinstance(image_data, str):
                # 移除可能的 data:image/png;base64, 前綴
                if image_data.startswith('data:'):
                    image_data = image_data.split(',')[1]
                
                try:
                    image_bytes = base64.b64decode(image_data)
                    return image_bytes
                except Exception as e:
                    print(f"❌ 解碼 base64 失敗: {e}")
                    return None
            else:
                print(f"⚠️ 未知的圖片格式: {type(image_data)}")
                return None
        elif 'images' in result and len(result['images']) > 0:
            # 備用格式：images 數組
            import base64
            image_data = result['images'][0]
            
            if isinstance(image_data, str):
                if image_data.startswith('data:'):
                    image_data = image_data.split(',')[1]
                
                try:
                    image_bytes = base64.b64decode(image_data)
                    return image_bytes
                except Exception as e:
                    print(f"❌ 解碼 base64 失敗: {e}")
                    return None
        else:
            print(f"⚠️ API 回應中沒有找到圖片數據")
            print(f"   回應內容: {json.dumps(result, indent=2)[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ API 請求超時（120秒）")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API 請求失敗: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   狀態碼: {e.response.status_code}")
            print(f"   回應內容: {e.response.text[:500]}")
        return None
    except Exception as e:
        print(f"❌ 處理 API 回應時出錯: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_image(image_bytes, output_path):
    """保存圖片到文件"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"✓ 圖片已保存: {output_path}")
        return True
    except Exception as e:
        print(f"❌ 保存圖片失敗: {e}")
        return False

def generate_voting_image_nvidia(article, output_dir="output_images"):
    """使用 NVIDIA API 為單個議題生成圖片"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成文件名
    filename = f"{output_dir}/voting_{article['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    print(f"\n🎨 開始生成圖片 #{article['id']}: {article.get('title', '未知')}")
    
    # 生成提示詞
    prompt = generate_prompt_from_article(article)
    negative_prompt = generate_negative_prompt()
    
    print(f"📝 提示詞預覽: {prompt[:100]}...")
    
    # 調用 NVIDIA API
    image_bytes = call_nvidia_api(prompt, negative_prompt)
    
    if image_bytes:
        # 保存圖片
        if save_image(image_bytes, filename):
            print(f"✅ 成功生成圖片: {filename}")
            return filename
        else:
            print(f"❌ 保存圖片失敗")
            return None
    else:
        print(f"❌ NVIDIA API 返回空結果")
        return None

def generate_all_images_nvidia(articles, output_dir="output_images"):
    """為所有議題使用 NVIDIA API 生成圖片"""
    images = []
    total = len(articles)
    
    print(f"\n{'='*60}")
    print(f"🚀 開始使用 NVIDIA Stable Diffusion 3 生成 {total} 張圖片")
    print(f"{'='*60}\n")
    
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}/{total}] ", end="")
        try:
            img_path = generate_voting_image_nvidia(article, output_dir)
            if img_path:
                images.append(img_path)
            else:
                print(f"⚠️ 跳過議題 #{article['id']}")
        except Exception as e:
            print(f"❌ 生成圖片失敗 (#{article['id']}): {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"✅ 完成！成功生成 {len(images)}/{total} 張圖片")
    print(f"📁 保存位置: {output_dir}/")
    print(f"{'='*60}\n")
    
    return images

if __name__ == "__main__":
    # 測試代碼
    test_article = {
        "id": 1,
        "title": "中美關係",
        "question": "你認為中美應否尋求和解？",
        "category": "國際政治"
    }
    
    print("測試 NVIDIA Stable Diffusion 3 圖像生成...")
    result = generate_voting_image_nvidia(test_article, "test_output")
    
    if result:
        print(f"\n✅ 測試成功！圖片已保存到: {result}")
    else:
        print("\n❌ 測試失敗")
