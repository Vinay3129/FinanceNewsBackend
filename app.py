from flask import Flask
from flask_cors import CORS
from apis.india import india_bp
from apis.us import us_bp
from apis.asia import asia_bp
from apis.europe import europe_bp
from apis.crypto import crypto_bp
from apis.globalnews import global_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(india_bp, url_prefix='/api/india')
app.register_blueprint(us_bp, url_prefix='/api/us')
app.register_blueprint(asia_bp, url_prefix='/api/asia')
app.register_blueprint(europe_bp, url_prefix='/api/europe')
app.register_blueprint(crypto_bp, url_prefix='/api/crypto')
app.register_blueprint(global_bp, url_prefix='/api/global')

@app.route('/')
def home():
    return {'message': 'Finance News API is running 🎯'}

from flask import render_template

@app.route('/india-news')
def serve_india_html():
    return render_template("india.html")

if __name__ == '__main__':
    app.run(debug=True)
