# yourapp/services/news_service.py
import requests

API_KEY = 'bd5063ffeffd4995981797c7cec091f0'
BASE_URL = 'https://newsapi.org/v2/everything'

def get_news(topic):
    params = {
        'apiKey': API_KEY,
        'qInTitle': topic,  # Search in the title for more relevant results
        'language': 'en',
        'sortBy': 'relevancy',  # You can also use 'publishedAt' for latest news
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
        return news_data['articles'][:5]  # Return the top 5 articles
    else:
        return []
