import requests
from bs4 import BeautifulSoup
import json
import random
from concurrent.futures import ThreadPoolExecutor

SOURCES = {
    "VNExpress": {"url": "https://vnexpress.net", "item": "article.item-news", "title": "h3.title-news a", "img": "div.thumb-art img"},
    "Tuổi Trẻ": {"url": "https://tuoitre.vn", "item": "div.box-category-item", "title": "h3.box-category-title-main a", "img": "a.box-category-link-with-avatar img"},
    "Thanh Niên": {"url": "https://thanhnien.vn", "item": "div.category-item", "title": "h2.category-item__title a", "img": "a.category-item__thumb img"},
    "Dân Trí": {"url": "https://dantri.com.vn", "item": "article.article-item", "title": "h3.article-title a", "img": "div.article-thumb img"},
    "VietnamNet": {"url": "https://vietnamnet.vn", "item": "div.horizontal-post", "title": "h3.vnn-title a", "img": "div.picture img"},
    "Znews": {"url": "https://znews.vn", "item": "article.article-item", "title": "p.article-title a", "img": "p.article-thumbnail img"}
}

def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Referer": "https://www.google.com/"}

def scrape_site(name, config):
    articles = []
    try:
        res = requests.get(config['url'], headers=get_headers(), timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        items = soup.select(config['item'])[:12]
        for item in items:
            t = item.select_one(config['title'])
            i = item.select_one(config['img'])
            if t:
                link = t['href'] if t['href'].startswith('http') else config['url'] + t['href']
                img = i.get('data-src') or i.get('src') if i else ""
                articles.append({"title": t.get_text(strip=True), "link": link, "img": img})
    except: pass
    return name, articles

if __name__ == "__main__":
    final_data = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = ex.map(lambda p: scrape_site(p[0], p[1]), SOURCES.items())
        for name, arts in results: final_data[name] = arts
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
