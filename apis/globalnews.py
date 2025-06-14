import requests
from flask import Blueprint, jsonify

global_bp = Blueprint('global_news', __name__)

# ✅ API Keys
NEWSDATA_API_KEY = 'pub_f1b94a0af239455b9d6b8c8197720de0'
GNEWS_API_KEY = 'c22aa4e5b3154001c857762ecd73d7ff'
NEWSAPI_KEY = 'abcdaac9869847b9aeea09a320ae6c61'
MEDIASTACK_KEY = '4e4537e9a8cbcde4a88979ed2ffc691f'

LANGUAGE = "en"
COUNTRIES = ["ae", "sa", "au", "nz", "br", "ar", "cl", "co", "qa", "ng", "za", "eg", "ke", "gh"]

def filter_articles(articles):
    keywords = ["finance", "business", "economy", "market", "stock", "investment"]
    filtered = []
    for article in articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        if any(kw in title or kw in description for kw in keywords):
            filtered.append(article)
    return filtered[:10]

@global_bp.route('/', methods=['GET'])
def global_root():
    return jsonify({"message": "Use /api/global/news to get the latest Global finance news."})

@global_bp.route('/news', methods=['GET'])
def get_global_news():
    for country in COUNTRIES:
        try:
            url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&country={country}&category=business&language={LANGUAGE}"
            r = requests.get(url)
            data = r.json()
            articles = data.get("results", [])
            filtered = filter_articles(articles)
            if filtered:
                return jsonify({"source": "newsdata.io", "country": country, "articles": filtered})
        except Exception as e:
            print(f"NewsData for {country} failed:", e)

        try:
            url = f"https://gnews.io/api/v4/search?q={country}+business&token={GNEWS_API_KEY}&lang={LANGUAGE}"
            r = requests.get(url)
            data = r.json()
            articles = data.get("articles", [])
            filtered = filter_articles(articles)
            if filtered:
                return jsonify({"source": "gnews", "country": country, "articles": filtered})
        except Exception as e:
            print(f"GNews for {country} failed:", e)

        try:
            url = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={NEWSAPI_KEY}"
            r = requests.get(url)
            data = r.json()
            articles = data.get("articles", [])
            filtered = filter_articles(articles)
            if filtered:
                return jsonify({"source": "newsapi", "country": country, "articles": filtered})
        except Exception as e:
            print(f"NewsAPI for {country} failed:", e)

        try:
            url = f"http://api.mediastack.com/v1/news?access_key={MEDIASTACK_KEY}&countries={country}&categories=business&languages={LANGUAGE}"
            r = requests.get(url)
            data = r.json()
            articles = data.get("data", [])
            filtered = filter_articles(articles)
            if filtered:
                return jsonify({"source": "mediastack", "country": country, "articles": filtered})
        except Exception as e:
            print(f"Mediastack for {country} failed:", e)

    return jsonify({"error": "All global sources failed"}), 500
