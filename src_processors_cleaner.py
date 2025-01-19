import re
from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

class TextCleaner:
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^\w\s.]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def split_into_sentences(self, text: str) -> List[str]:
        return sent_tokenize(text)

    def remove_stopwords(self, text: str) -> str:
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered_words)

