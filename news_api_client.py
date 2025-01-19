from typing import List, Dict
import newsapi
from pydantic import BaseModel
import logging

class NewsArticle(BaseModel):
    title: str
    content: str
    url: str
    source: str
    published_at: str

class NewsAPIClient:
    def __init__(self, api_key: str):
        self.client = newsapi.NewsApiClient(api_key=api_key)
        self.logger = logging.getLogger(__name__)
    
    def fetch_financial_news(self, sources: List[str], language: str = 'en') -> List[NewsArticle]:
        try:
            response = self.client.get_everything(
                sources=','.join(sources),
                language=language,
                sort_by='publishedAt'
            )
            
            articles = []
            for article in response['articles']:
                articles.append(
                    NewsArticle(
                        title=article['title'],
                        content=article['content'],
                        url=article['url'],
                        source=article['source']['name'],
                        published_at=article['publishedAt']
                    )
                )
            return articles
            
        except Exception as e:
            self.logger.error(f"Napaka pri pridobivanju novic: {str(e)}")
            return [] 