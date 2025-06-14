# 📄 us.py
import requests
from flask import Blueprint, jsonify

us_bp = Blueprint('us_news', __name__)

# 🔑 API Keys
NEWSDATA_API_KEY = 'pub_f1b94a0af239455b9d6b8c8197720de0'
GNEWS_API_KEY = 'c22aa4e5b3154001c857762ecd73d7ff'
NEWSAPI_KEY = 'abcdaac9869847b9aeea09a320ae6c61'
MEDIASTACK_KEY = '4e4537e9a8cbcde4a88979ed2ffc691f'

LANGUAGE = "en"

def filter_articles(articles):
    keywords = ["finance", "business", "economy", "market", "stock", "investment"]
    filtered = []
    for article in articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        if any(kw in title or kw in description for kw in keywords):
            filtered.append(article)
    return filtered[:10]

@us_bp.route('/news')
def get_us_news():
    # ✅ NewsData.io
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&country=us&category=business&language={LANGUAGE}"
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("results", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "newsdata.io", "articles": filtered})
    except Exception as e:
        print("NewsData (US) failed:", e)

    # ✅ GNews
    url = f"https://gnews.io/api/v4/search?q=usa+business&token={GNEWS_API_KEY}&lang={LANGUAGE}&country=us"
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("articles", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "gnews", "articles": filtered})
    except Exception as e:
        print("GNews (US) failed:", e)

    # ✅ NewsAPI
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={NEWSAPI_KEY}"
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("articles", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "newsapi", "articles": filtered})
    except Exception as e:
        print("NewsAPI (US) failed:", e)

    # ✅ Mediastack
    url = f"http://api.mediastack.com/v1/news?access_key={MEDIASTACK_KEY}&countries=us&categories=business&languages={LANGUAGE}"
    try:
        r = requests.get(url)
        data = r.json()
        articles = data.get("data", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "mediastack", "articles": filtered})
    except Exception as e:
        print("Mediastack (US) failed:", e)

    return jsonify({"error": "All sources failed for US"}), 500
