from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from typing import List
import logging

class NewsSummarizer:
    def __init__(self, model_name: str = 't5-base'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        self.logger = logging.getLogger(__name__)
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 40) -> str:
        try:
            # Pripravi vhodni tekst
            input_text = f"summarize: {text}"
            
            # Tokenizacija
            inputs = self.tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            ).to(self.device)
            
            # Generiranje povzetka
            summary_ids = self.model.generate(
                inputs,
                max_length=max_length,
                min_length=min_length,
                do_sample=True,
                num_beams=4,
                temperature=0.7
            )
            
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
            
        except Exception as e:
            self.logger.error(f"Napaka pri povzemanju: {str(e)}")
            return "" 