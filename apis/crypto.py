import requests
from flask import Blueprint, jsonify

crypto_bp = Blueprint('crypto_news', __name__)

NEWSDATA_API_KEY = 'pub_f1b94a0af239455b9d6b8c8197720de0'
GNEWS_API_KEY = 'c22aa4e5b3154001c857762ecd73d7ff'
NEWSAPI_KEY = 'abcdaac9869847b9aeea09a320ae6c61'
MEDIASTACK_KEY = '4e4537e9a8cbcde4a88979ed2ffc691f'

LANGUAGE = "en"

def filter_articles(articles):
    keywords = ["crypto", "bitcoin", "ethereum", "blockchain", "web3", "defi", "nft"]
    filtered = []
    for article in articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        if not article.get("author"):
            article["author"] = article.get("source_id", "Unknown Source")
        if any(kw in title or kw in description for kw in keywords):
            filtered.append(article)
    return filtered[:10]

@crypto_bp.route('/news')
def get_crypto_news():
    try:
        url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q=crypto&language={LANGUAGE}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("results", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "newsdata.io", "articles": filtered})
    except Exception as e:
        print("NewsData (Crypto) failed:", e)

    try:
        url = f"https://gnews.io/api/v4/search?q=cryptocurrency&token={GNEWS_API_KEY}&lang={LANGUAGE}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("articles", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "gnews", "articles": filtered})
    except Exception as e:
        print("GNews (Crypto) failed:", e)

    try:
        url = f"https://newsapi.org/v2/everything?q=crypto&language={LANGUAGE}&apiKey={NEWSAPI_KEY}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("articles", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "newsapi", "articles": filtered})
    except Exception as e:
        print("NewsAPI (Crypto) failed:", e)

    try:
        url = f"http://api.mediastack.com/v1/news?access_key={MEDIASTACK_KEY}&keywords=crypto&languages={LANGUAGE}"
        r = requests.get(url)
        data = r.json()
        articles = data.get("data", [])
        filtered = filter_articles(articles)
        if filtered:
            return jsonify({"source": "mediastack", "articles": filtered})
    except Exception as e:
        print("Mediastack (Crypto) failed:", e)

    return jsonify({"error": "All sources failed for Crypto"}), 500
