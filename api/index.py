from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
import random
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Cấu hình danh sách các báo
SOURCES = {
    "VNExpress": {
        "url": "https://vnexpress.net",
        "item": "article.item-news",
        "title": "h3.title-news a",
        "img": "div.thumb-art img"
    },
    "Tuổi Trẻ": {
        "url": "https://tuoitre.vn",
        "item": "div.box-category-item",
        "title": "h3.box-category-title-main a",
        "img": "a.box-category-link-with-avatar img"
    },
    "Thanh Niên": {
        "url": "https://thanhnien.vn",
        "item": "div.category-item",
        "title": "h2.category-item__title a",
        "img": "a.category-item__thumb img"
    },
    "Dân Trí": {
        "url": "https://dantri.com.vn",
        "item": "article.article-item",
        "title": "h3.article-title a",
        "img": "div.article-thumb img"
    },
    "VietnamNet": {
        "url": "https://vietnamnet.vn",
        "item": "div.horizontal-post",
        "title": "h3.vnn-title a",
        "img": "div.picture img"
    },
    "Znews": {
        "url": "https://znews.vn",
        "item": "article.article-item",
        "title": "p.article-title a",
        "img": "p.article-thumbnail img"
    }
}

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

def scrape_site(name, config):
    articles = []
    try:
        response = requests.get(config['url'], headers=get_headers(), timeout=7)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        items = soup.select(config['item'])[:12] # Lấy 12 bài mỗi trang
        
        for item in items:
            title_tag = item.select_one(config['title'])
            img_tag = item.select_one(config['img'])
            
            if title_tag and title_tag.get('href'):
                title = title_tag.get_text(strip=True)
                link = title_tag['href']
                if not link.startswith('http'):
                    link = config['url'].rstrip('/') + '/' + link.lstrip('/')
                
                # Xử lý lấy ảnh (ưu tiên data-src của lazyload)
                img_url = "https://via.placeholder.com/300x180?text=No+Image"
                if img_tag:
                    img_url = img_tag.get('data-src') or img_tag.get('src') or img_url
                
                articles.append({"title": title, "link": link, "img": img_url})
    except Exception as e:
        print(f"Lỗi khi cào {name}: {e}")
    return name, articles

@app.route('/')
def home():
    # Sử dụng ThreadPoolExecutor để cào 6 trang song song cho nhanh
    final_data = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(lambda x: scrape_site(x[0], x[1]), SOURCES.items())
        for name, articles in results:
            final_data[name] = articles

    return render_template_string(HTML_TEMPLATE, data=final_data)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Hub - Tin Tức Tổng Hợp</title>
    <style>
        :root { --bg: #0f0f0f; --card-bg: #1e1e1e; --text: #efefef; --accent: #ff3e3e; }
        body { background-color: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }
        h1 { text-align: center; color: var(--accent); letter-spacing: 2px; }
        
        .row { margin-bottom: 40px; }
        .row-header { display: flex; align-items: center; margin-bottom: 15px; padding-left: 10px; }
        .row-header h2 { margin: 0; font-size: 1.4rem; border-left: 4px solid var(--accent); padding-left: 12px; }
        
        /* Thanh cuộn ngang */
        .scroll-wrapper { 
            display: flex; overflow-x: auto; gap: 15px; padding: 10px;
            scroll-behavior: smooth; scrollbar-width: none; 
        }
        .scroll-wrapper::-webkit-scrollbar { display: none; }

        .card { 
            flex: 0 0 280px; background: var(--card-bg); border-radius: 12px; 
            transition: all 0.3s ease; text-decoration: none; color: inherit;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5); display: flex; flex-direction: column;
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(255,62,62,0.2); }
        
        .card img { width: 100%; height: 160px; object-fit: cover; border-top-left-radius: 12px; border-top-right-radius: 12px; }
        .card-info { padding: 12px; font-size: 0.95rem; font-weight: 500; line-height: 1.4; flex-grow: 1; }
    </style>
</head>
<body>
    <h1>NEWS HUB</h1>
    
    {% for source, articles in data.items() %}
    <div class="row">
        <div class="row-header"><h2>{{ source }}</h2></div>
        <div class="scroll-wrapper">
            {% for art in articles %}
            <a href="{{ art.link }}" target="_blank" class="card">
                <img src="{{ art.img }}" loading="lazy">
                <div class="card-info">{{ art.title }}</div>
            </a>
            {% endfor %}
        </div>
    </div>
    {% endfor %}

    <script>
        // Thêm tính năng dùng con lăn chuột để cuộn ngang
        const scrollContainers = document.querySelectorAll('.scroll-wrapper');
        scrollContainers.forEach(container => {
            container.addEventListener('wheel', (evt) => {
                evt.preventDefault();
                container.scrollLeft += evt.deltaY;
            });
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
