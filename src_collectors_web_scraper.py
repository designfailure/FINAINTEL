from bs4 import BeautifulSoup
import requests
import logging
from typing import Dict, List, Optional

class FinancialWebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.logger = logging.getLogger(__name__)

    def fetch_article(self, url: str) -> Optional[Dict]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'title': self._extract_title(soup),
                'content': self._extract_content(soup),
                'date': self._extract_date(soup),
                'source': url
            }
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('h1') or soup.find('title')
        return title.text.strip() if title else ""

    def _extract_content(self, soup: BeautifulSoup) -> str:
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Find main article content (customize selectors based on website structure)
        article = soup.find('article') or soup.find('main')
        if article:
            return ' '.join([p.text.strip() for p in article.find_all('p')])
        return ""

    def _extract_date(self, soup: BeautifulSoup) -> str:
        date = soup.find('time') or soup.find(class_='date')
        return date.text.strip() if date else ""

