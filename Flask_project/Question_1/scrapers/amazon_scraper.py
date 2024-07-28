import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_amazon(query, max_results=10):
    url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.amazon.com/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        for item in soup.select('div[data-component-type="s-search-result"]'):
            title_elem = item.select_one('h2 a span')
            price_elem = item.select_one('.a-price-whole')
            image_elem = item.select_one('img.s-image')
            
            if title_elem and price_elem and image_elem:
                product = {
                    'title': title_elem.text.strip(),
                    'price': price_elem.text.strip(),
                    'image': image_elem['src']
                }
                products.append(product)
                
                if len(products) >= max_results:
                    break
        
        if not products:
            print("No products found. The page structure might have changed.")
        
        return products
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return []

# Example usage
results = scrape_amazon("laptop", max_results=5)
for product in results:
    print(f"Title: {product['title']}")
    print(f"Price: ${product['price']}")
    print(f"Image URL: {product['image']}")
    print("---")