from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from typing import List, Dict
import logging

class FinancialSummarizer:
    def __init__(self, model_name: str = "t5-base"):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        self.logger = logging.getLogger(__name__)

    def generate_summary(self, text: str, max_length: int = 150) -> str:
        try:
            # Prepare input text
            input_text = f"summarize: {text}"
            
            # Tokenize input
            inputs = self.tokenizer.encode(
                input_text, 
                return_tensors="pt", 
                max_length=1024, 
                truncation=True
            ).to(self.device)
            
            # Generate summary
            summary_ids = self.model.generate(
                inputs,
                max_length=max_length,
                min_length=40,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
            
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return ""

