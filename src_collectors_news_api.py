import requests
from typing import List, Dict
import os
from datetime import datetime, timedelta

class NewsAPICollector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"

    def get_financial_news(self, 
                         keywords: List[str] = ["finance", "stock market", "economy"],
                         days: int = 1) -> List[Dict]:
        endpoint = f"{self.base_url}/everything"
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        params = {
            'q': ' OR '.join(keywords),
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'language': 'en',
            'sortBy': 'relevancy',
            'apiKey': self.api_key
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        return response.json().get('articles', [])

