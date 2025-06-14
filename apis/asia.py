import requests
from flask import Blueprint, jsonify

asia_bp = Blueprint('asia_news', __name__)

NEWSDATA_API_KEY = 'pub_f1b94a0af239455b9d6b8c8197720de0'
GNEWS_API_KEY = 'c22aa4e5b3154001c857762ecd73d7ff'
NEWSAPI_KEY = 'abcdaac9869847b9aeea09a320ae6c61'
MEDIASTACK_KEY = '4e4537e9a8cbcde4a88979ed2ffc691f'

LANGUAGE = "en"

def filter_articles(articles):
    keywords = ["asia", "india", "china", "japan", "korea", "stock", "business", "economy", "finance", "market"]
    filtered = []
    for article in articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        if any(kw in title or kw in description for kw in keywords):
            filtered.append(article)
    return filtered[:10]

@asia_bp.route('/news')
def get_asia_news():
    try:
        url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&country=in,jp,cn,sg,kr&category=business&language={LANGUAGE}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("results", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "newsdata.io", "articles": filtered})
    except Exception as e:
        print("NewsData (Asia) failed:", e)

    try:
        url = f"https://gnews.io/api/v4/search?q=asia+business&token={GNEWS_API_KEY}&lang={LANGUAGE}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("articles", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "gnews", "articles": filtered})
    except Exception as e:
        print("GNews (Asia) failed:", e)

    try:
        url = f"https://newsapi.org/v2/everything?q=asia+business&language={LANGUAGE}&apiKey={NEWSAPI_KEY}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("articles", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "newsapi", "articles": filtered})
    except Exception as e:
        print("NewsAPI (Asia) failed:", e)

    try:
        url = f"http://api.mediastack.com/v1/news?access_key={MEDIASTACK_KEY}&keywords=asia,business&languages={LANGUAGE}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("data", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "mediastack", "articles": filtered})
    except Exception as e:
        print("Mediastack (Asia) failed:", e)

    return jsonify({"error": "All sources failed for Asia"}), 500
