import re
from typing import List
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

class TextCleaner:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text: str) -> str:
        # Odstrani HTML oznake
        text = re.sub(r'<[^>]+>', '', text)
        
        # Odstrani posebne znake
        text = re.sub(r'[^\w\s]', '', text)
        
        # Normalizacija presledkov
        text = ' '.join(text.split())
        
        return text.lower()
    
    def split_into_sentences(self, text: str) -> List[str]:
        return sent_tokenize(text)
    
    def remove_stopwords(self, text: str) -> str:
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words) 