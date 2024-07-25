from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def scrape_youtube():
    url = "https://www.youtube.com/feed/trending"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    videos = soup.find_all('div', {'class': 'ytd-video-renderer'})
    
    trending_videos = []
    for video in videos[:10]:  # Get top 10 trending videos
        title = video.find('yt-formatted-string', {'id': 'video-title'}).text
        views = video.find('yt-formatted-string', {'id': 'metadata-line'}).find_all('span')[0].text
        trending_videos.append({'title': title, 'views': views})
    
    return trending_videos

def scrape_amazon():
    url = "https://www.amazon.com/best-sellers"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'class': 'zg-item-immersion'})
    
    best_sellers = []
    for item in items[:10]:  # Get top 10 best sellers
        title = item.find('div', {'class': 'p13n-sc-truncate'}).text.strip()
        price = item.find('span', {'class': 'p13n-sc-price'}).text
        best_sellers.append({'title': title, 'price': price})
    
    return best_sellers

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/youtube')
def youtube_trending():
    videos = scrape_youtube()
    return render_template('youtube.html', videos=videos)

@app.route('/amazon')
def amazon_bestsellers():
    products = scrape_amazon()
    return render_template('amazon.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)