import requests
from bs4 import BeautifulSoup
import json
import random
from concurrent.futures import ThreadPoolExecutor

# Cập nhật Selectors mới nhất cho 3 báo bị lỗi
SOURCES = {
    "VNExpress": {
        "url": "https://vnexpress.net", 
        "item": "article.item-news", 
        "title": "h3.title-news a", 
        "img": "picture img"
    },
    "Tuổi Trẻ": {
        "url": "https://tuoitre.vn", 
        "item": "div.box-category-item", # Cập nhật lại class container
        "title": "h3.box-category-title-main a", 
        "img": "img.box-category-avatar-img"
    },
    "Thanh Niên": {
        "url": "https://thanhnien.vn", 
        "item": ".category-item", # Selector đơn giản hóa cho Thanh Niên
        "title": "h2.category-item__title a", 
        "img": ".category-item__thumb img"
    },
    "Dân Trí": {
        "url": "https://dantri.com.vn", 
        "item": "article.article-item", 
        "title": "h3.article-title a", 
        "img": "img"
    },
    "VietnamNet": {
        "url": "https://vietnamnet.vn", 
        "item": ".vnn-news-item, .horizontal-post", # Thêm class item mới
        "title": ".vnn-title a, .vnn-news-title a", 
        "img": "img"
    },
    "Znews": {
        "url": "https://znews.vn", 
        "item": "article.article-item", 
        "title": ".article-title a", 
        "img": "img"
    }
}

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

def scrape_site(name, config):
    articles = []
    try:
        # Sử dụng session để giữ cookies (giúp vượt qua một số kiểm tra đơn giản)
        session = requests.Session()
        res = session.get(config['url'], headers=get_headers(), timeout=15)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.content, 'html.parser')
        items = soup.select(config['item'])
        
        for item in items[:10]:
            t = item.select_one(config['title'])
            if not t: continue
            
            title = t.get_text(strip=True)
            link = t.get('href', '')
            if link and not link.startswith('http'):
                link = config['url'].rstrip('/') + '/' + link.lstrip('/')
            
            img_tag = item.select_one(config['img'])
            img = "https://via.placeholder.com/300x200?text=No+Image"
            if img_tag:
                # Ưu tiên các attribute lazy-load phổ biến
                img = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-original') or img
            
            if title and link:
                articles.append({"title": title, "link": link, "img": img})
        
        print(f"✅ {name}: Lấy được {len(articles)} bài.")
    except Exception as e:
        print(f"❌ {name}: Lỗi -> {str(e)}")
        
    return name, articles

if __name__ == "__main__":
    final_data = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = ex.map(lambda p: scrape_site(p[0], p[1]), SOURCES.items())
        for name, arts in results:
            final_data[name] = arts
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
