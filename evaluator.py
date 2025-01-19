from rouge_score import rouge_scorer
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class FinancialNewsEvaluator:
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.logger = logging.getLogger(__name__)
        
    def evaluate_summaries(self, original_texts: List[str], generated_summaries: List[str]) -> Dict:
        """Evalvacija povzetkov z ROUGE metrikami."""
        try:
            rouge_scores = {
                'rouge1': [],
                'rouge2': [],
                'rougeL': []
            }
            
            for original, summary in zip(original_texts, generated_summaries):
                scores = self.rouge_scorer.score(original, summary)
                for metric in rouge_scores.keys():
                    rouge_scores[metric].append(scores[metric].fmeasure)
            
            # Izračunaj povprečja
            avg_scores = {
                metric: np.mean(scores) 
                for metric, scores in rouge_scores.items()
            }
            
            return {
                'detailed_scores': rouge_scores,
                'average_scores': avg_scores
            }
            
        except Exception as e:
            self.logger.error(f"Napaka pri evalvaciji povzetkov: {str(e)}")
            return {}
    
    def evaluate_sentiment(self, true_sentiments: List[str], 
                         predicted_sentiments: List[str],
                         confidence_scores: List[float]) -> Dict:
        """Evalvacija analize sentimenta."""
        try:
            # Izračunaj klasifikacijske metrike
            report = classification_report(
                true_sentiments,
                predicted_sentiments,
                output_dict=True
            )
            
            # Izračunaj matriko zmede
            conf_matrix = confusion_matrix(
                true_sentiments,
                predicted_sentiments
            )
            
            # Analiza zaupanja v napovedi
            confidence_analysis = {
                'mean_confidence': np.mean(confidence_scores),
                'std_confidence': np.std(confidence_scores),
                'min_confidence': np.min(confidence_scores),
                'max_confidence': np.max(confidence_scores)
            }
            
            return {
                'classification_report': report,
                'confusion_matrix': conf_matrix,
                'confidence_analysis': confidence_analysis
            }
            
        except Exception as e:
            self.logger.error(f"Napaka pri evalvaciji sentimenta: {str(e)}")
            return {}
    
    def visualize_results(self, summary_scores: Dict, sentiment_results: Dict,
                         output_path: str = "evaluation_results"):
        """Vizualizacija rezultatov evalvacije."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Vizualizacija ROUGE rezultatov
            plt.figure(figsize=(10, 6))
            avg_scores = summary_scores['average_scores']
            plt.bar(avg_scores.keys(), avg_scores.values())
            plt.title('Povprečne ROUGE ocene')
            plt.ylabel('F1 ocena')
            plt.savefig(f"{output_path}/rouge_scores_{timestamp}.png")
            plt.close()
            
            # Vizualizacija matrike zmede
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                sentiment_results['confusion_matrix'],
                annot=True,
                fmt='d',
                cmap='Blues'
            )
            plt.title('Matrika zmede za analizo sentimenta')
            plt.savefig(f"{output_path}/confusion_matrix_{timestamp}.png")
            plt.close()
            
            # Shrani podrobno poročilo
            report = pd.DataFrame(sentiment_results['classification_report']).transpose()
            report.to_csv(f"{output_path}/classification_report_{timestamp}.csv")
            
        except Exception as e:
            self.logger.error(f"Napaka pri vizualizaciji rezultatov: {str(e)}")
    
    def generate_evaluation_report(self, 
                                 summary_evaluation: Dict,
                                 sentiment_evaluation: Dict) -> str:
        """Generiranje poročila o evalvaciji."""
        try:
            report = []
            report.append("# Poročilo o evalvaciji")
            report.append("\n## Evalvacija povzetkov")
            
            # ROUGE rezultati
            report.append("\nPovprečne ROUGE ocene:")
            for metric, score in summary_evaluation['average_scores'].items():
                report.append(f"- {metric}: {score:.4f}")
            
            # Rezultati sentimenta
            report.append("\n## Evalvacija sentimenta")
            clf_report = sentiment_evaluation['classification_report']
            
            report.append("\nNatančnost po razredih:")
            for label in ['positive', 'negative', 'neutral']:
                if label in clf_report:
                    precision = clf_report[label]['precision']
                    recall = clf_report[label]['recall']
                    f1 = clf_report[label]['f1-score']
                    report.append(f"- {label}:")
                    report.append(f"  - Precision: {precision:.4f}")
                    report.append(f"  - Recall: {recall:.4f}")
                    report.append(f"  - F1: {f1:.4f}")
            
            # Analiza zaupanja
            conf_analysis = sentiment_evaluation['confidence_analysis']
            report.append("\nAnaliza zaupanja v napovedi:")
            report.append(f"- Povprečno zaupanje: {conf_analysis['mean_confidence']:.4f}")
            report.append(f"- Standardni odklon: {conf_analysis['std_confidence']:.4f}")
            report.append(f"- Min zaupanje: {conf_analysis['min_confidence']:.4f}")
            report.append(f"- Max zaupanje: {conf_analysis['max_confidence']:.4f}")
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"Napaka pri generiranju poročila: {str(e)}")
            return "Napaka pri generiranju poročila" 