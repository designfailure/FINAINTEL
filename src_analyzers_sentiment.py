from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, List

class FinancialSentimentAnalyzer:
    def __init__(self, model_name: str = "ProsusAI/finbert"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)
        self.labels = ['negative', 'neutral', 'positive']

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        outputs = self.model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        sentiment_scores = {label: float(prob) for label, prob in zip(self.labels, probabilities[0])}
        sentiment_label = max(sentiment_scores, key=sentiment_scores.get)
        
        return {
            'label': sentiment_label,
            'scores': sentiment_scores
        }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        return [self.analyze_sentiment(text) for text in texts]

