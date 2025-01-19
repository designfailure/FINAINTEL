from rouge_score import rouge_scorer
from typing import Dict, List
import numpy as np

class SummaryEvaluator:
    def __init__(self):
        self.scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    def evaluate_summary(self, reference: str, generated: str) -> Dict[str, float]:
        scores = self.scorer.score(reference, generated)
        
        return {
            'rouge1_f1': scores['rouge1'].fmeasure,
            'rouge2_f1': scores['rouge2'].fmeasure,
            'rougeL_f1': scores['rougeL'].fmeasure
        }

    def calculate_average_scores(self, all_scores: List[Dict[str, float]]) -> Dict[str, float]:
        avg_scores = {}
        for metric in ['rouge1_f1', 'rouge2_f1', 'rougeL_f1']:
            scores = [score[metric] for score in all_scores]
            avg_scores[metric] = np.mean(scores)
        return avg_scores

