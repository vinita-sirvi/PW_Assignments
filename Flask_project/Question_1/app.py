from flask import Flask, render_template, request
from scrapers.youtube_scraper import scrape_youtube
from scrapers.amazon_scraper import scrape_amazon

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/youtube')
def youtube_results():
    query = request.args.get('query', '')
    videos = scrape_youtube(query)
    return render_template('youtube_results.html', videos=videos, query=query)

@app.route('/amazon')
def amazon_results():
    query = request.args.get('query', '')
    products = scrape_amazon(query)
    return render_template('amazon_results.html', products=products, query=query)

if __name__ == '__main__':
    app.run(debug=True)