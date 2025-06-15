from flask import Blueprint, jsonify
import requests

top_bp = Blueprint('top', __name__)

@top_bp.route('/news')
def get_top_news():
    top_articles = []
    endpoints = [
        ("India", "https://newsdata.io/api/1/news?apikey=YOUR_API_KEY&q=finance%20stock%20market&country=in&language=en"),
        ("US", "https://newsdata.io/api/1/news?apikey=YOUR_API_KEY&q=finance%20stock%20market&country=us&language=en"),
        ("Asia", "https://newsdata.io/api/1/news?apikey=YOUR_API_KEY&q=asia%20finance&language=en"),
        ("Europe", "https://newsdata.io/api/1/news?apikey=YOUR_API_KEY&q=europe%20finance&language=en"),
        ("Crypto", "https://newsdata.io/api/1/news?apikey=YOUR_API_KEY&q=crypto&category=business&language=en")
    ]

    for region, url in endpoints:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            articles = data.get('results', [])[:2]
            top_articles.extend(articles)
        except Exception as e:
            print(f"Error fetching {region} news: {e}")

    top_articles.sort(key=lambda x: x.get('pubDate', ''), reverse=True)
    return jsonify({"status": "ok", "articles": top_articles})
