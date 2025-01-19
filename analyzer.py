from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np
from typing import Dict, List, Tuple
import logging
from pydantic import BaseModel

class SentimentResult(BaseModel):
    text: str
    sentiment: str
    confidence: float
    scores: Dict[str, float]

class FinancialSentimentAnalyzer:
    def __init__(self, model_name: str = "ProsusAI/finbert"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.logger = logging.getLogger(__name__)
        self.labels = ["positive", "negative", "neutral"]
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        try:
            # Tokenizacija
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Napoved
            with torch.no_grad():
                outputs = self.model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=1)
                scores = scores[0].cpu().numpy()
            
            # Določitev sentimenta
            sentiment_idx = np.argmax(scores)
            sentiment = self.labels[sentiment_idx]
            confidence = float(scores[sentiment_idx])
            
            # Pripravi rezultat
            result = SentimentResult(
                text=text,
                sentiment=sentiment,
                confidence=confidence,
                scores={label: float(score) for label, score in zip(self.labels, scores)}
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Napaka pri analizi sentimenta: {str(e)}")
            return None
    
    def analyze_batch(self, texts: List[str], batch_size: int = 16) -> List[SentimentResult]:
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_results = [self.analyze_sentiment(text) for text in batch]
            results.extend([r for r in batch_results if r is not None])
        return results 