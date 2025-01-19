from bs4 import BeautifulSoup
import requests
from typing import List, Dict
import logging
from pydantic import BaseModel
from urllib.parse import urlparse

class ScrapedArticle(BaseModel):
    title: str
    content: str
    url: str
    source: str

class FinancialNewsScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_bloomberg(self, url: str) -> List[ScrapedArticle]:
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            for article in soup.find_all('article'):
                title = article.find('h3').text.strip()
                content = article.find('p').text.strip()
                article_url = article.find('a')['href']
                
                articles.append(
                    ScrapedArticle(
                        title=title,
                        content=content,
                        url=article_url,
                        source='Bloomberg'
                    )
                )
            return articles
            
        except Exception as e:
            self.logger.error(f"Napaka pri strganju Bloomberg strani: {str(e)}")
            return [] 

    def scrape_url(self, url: str) -> List[ScrapedArticle]:
        """Scrape any financial news URL."""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Poskusi najti glavni članek
            article_content = ""
            
            # Poskusi različne pogoste selektorje za vsebino članka
            content_selectors = [
                'article',
                '.article-content',
                '.article-body',
                '#article-body',
                '.story-content'
            ]
            
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    # Odstrani nepotrebne elemente
                    for tag in content.find_all(['script', 'style']):
                        tag.decompose()
                    article_content = content.get_text(strip=True)
                    break
            
            if not article_content:
                # Če ne najdemo specifičnega selektorja, vzemi vse odstavke
                paragraphs = soup.find_all('p')
                article_content = ' '.join(p.get_text(strip=True) for p in paragraphs)
            
            # Poskusi najti naslov
            title = ""
            title_selectors = ['h1', '.article-title', '.headline']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            if not title:
                title = soup.title.string if soup.title else "Neznan naslov"
            
            return [ScrapedArticle(
                title=title,
                content=article_content,
                url=url,
                source=urlparse(url).netloc
            )]
            
        except Exception as e:
            self.logger.error(f"Napaka pri strganju URL-ja {url}: {str(e)}")
            return [] 