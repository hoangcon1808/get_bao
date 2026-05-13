import requests
from bs4 import BeautifulSoup
import json
import random
from concurrent.futures import ThreadPoolExecutor

# Cấu hình nguồn (Lưu ý: Nếu một báo không có bài, bạn có thể cần cập nhật lại class CSS ở đây)
SOURCES = {
    "VNExpress": {"url": "https://vnexpress.net", "item": "article.item-news", "title": "h3.title-news a", "img": "picture img, div.thumb-art img"},
    "Tuổi Trẻ": {"url": "https://tuoitre.vn", "item": "div.box-category-item", "title": "h3.box-category-title-main a", "img": "img.box-category-avatar-img, a.box-category-link-with-avatar img"},
    "Thanh Niên": {"url": "https://thanhnien.vn", "item": "div.category-item", "title": "h2.category-item__title a", "img": "a.category-item__thumb img"},
    "Dân Trí": {"url": "https://dantri.com.vn", "item": "article.article-item", "title": "h3.article-title a", "img": "div.article-thumb img"},
    "VietnamNet": {"url": "https://vietnamnet.vn", "item": "div.horizontal-post, div.vnn-news-item", "title": "h3.vnn-title a, h3.vnn-news-title a", "img": "picture img, div.picture img"},
    "Znews": {"url": "https://znews.vn", "item": "article.article-item", "title": "p.article-title a, header.article-title a", "img": "p.article-thumbnail img, header.article-thumbnail img"}
}

def get_headers():
    # Bộ headers giả lập giống người dùng thật nhất có thể
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }

def scrape_site(name, config):
    articles = []
    try:
        # Tăng timeout lên 15s phòng trường hợp server GitHub chậm
        res = requests.get(config['url'], headers=get_headers(), timeout=15)
        res.raise_for_status() # Sẽ ném ra lỗi nếu bị báo chặn (ví dụ lỗi 403, 404)
        
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # Hỗ trợ tìm kiếm theo nhiều class (phân cách bằng dấu phẩy)
        items = soup.select(config['item'])
        
        if not items:
            print(f"⚠️ [{name}] Không tìm thấy bài viết nào! (Có thể báo đã đổi giao diện web)")
            
        for item in items[:12]:
            t = item.select_one(config['title'])
            if not t:
                continue # Nếu không có tiêu đề, bỏ qua bài này
                
            title_text = t.get_text(strip=True)
            link = t.get('href', '')
            if link and not link.startswith('http'):
                link = config['url'].rstrip('/') + '/' + link.lstrip('/')
            
            i = item.select_one(config['img'])
            img_url = "https://via.placeholder.com/250x140?text=No+Image" # Ảnh mặc định
            if i:
                img_url = i.get('data-src') or i.get('src') or img_url
                
            if title_text and link:
                articles.append({"title": title_text, "link": link, "img": img_url})
                
        print(f"✅ [{name}] Đã lấy thành công {len(articles)} bài.")
        
    except requests.exceptions.HTTPError as err:
        print(f"❌ [{name}] Bị lỗi mạng hoặc bị chặn: {err}")
    except Exception as e:
        print(f"❌ [{name}] Lỗi không xác định: {e}")
        
    return name, articles

if __name__ == "__main__":
    final_data = {}
    print("Bắt đầu tiến trình cào dữ liệu...")
    
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = ex.map(lambda p: scrape_site(p[0], p[1]), SOURCES.items())
        for name, arts in results: 
            final_data[name] = arts
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print("Hoàn tất lưu file data.json!")
