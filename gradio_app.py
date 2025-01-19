import gradio as gr
import validators
from typing import List, Dict, Tuple
from src.data_collection.news_scraper import FinancialNewsScraper
from src.preprocessing.text_cleaner import TextCleaner
from src.summarization.summarizer import NewsSummarizer
from src.sentiment.analyzer import FinancialSentimentAnalyzer
import logging

class FinancialNewsGUI:
    def __init__(self, config: Dict):
        self.scraper = FinancialNewsScraper()
        self.cleaner = TextCleaner()
        self.summarizer = NewsSummarizer(config['summarization']['model_name'])
        self.sentiment_analyzer = FinancialSentimentAnalyzer(
            config['sentiment_analysis']['model_name']
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_url(self, url: str) -> bool:
        return validators.url(url) is True
    
    def process_article(self, url: str, keywords: str) -> Tuple[str, str, str, float]:
        try:
            # Preveri URL
            if not self.validate_url(url):
                return "Napaka", "Neveljaven URL", "neutral", 0.0
            
            # Razdeli ključne besede
            keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
            
            # Pridobi članek
            articles = self.scraper.scrape_url(url)
            if not articles:
                return "Napaka", "Ni najdenih člankov", "neutral", 0.0
            
            # Filtriraj po ključnih besedah
            filtered_articles = []
            for article in articles:
                if any(kw.lower() in article.content.lower() for kw in keywords_list):
                    filtered_articles.append(article)
            
            if not filtered_articles:
                return "Napaka", "Ni člankov z izbranimi ključnimi besedami", "neutral", 0.0
            
            # Vzemi prvi ujemajoči članek
            article = filtered_articles[0]
            
            # Očisti in povzemi besedilo
            cleaned_text = self.cleaner.clean_text(article.content)
            summary = self.summarizer.summarize(cleaned_text)
            
            # Analiziraj sentiment
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(summary)
            
            return (
                article.title,
                summary,
                sentiment_result.sentiment,
                sentiment_result.confidence
            )
            
        except Exception as e:
            self.logger.error(f"Napaka pri procesiranju članka: {str(e)}")
            return "Napaka", str(e), "neutral", 0.0
    
    def launch_interface(self):
        with gr.Blocks(title="Analizator finančnih novic") as interface:
            gr.Markdown("# Analizator finančnih novic")
            
            with gr.Row():
                url_input = gr.Textbox(
                    label="URL članka",
                    placeholder="Vnesite URL finančnega članka..."
                )
                keywords_input = gr.Textbox(
                    label="Ključne besede",
                    placeholder="Vnesite ključne besede, ločene z vejico..."
                )
            
            analyze_btn = gr.Button("Analiziraj")
            
            with gr.Row():
                title_output = gr.Textbox(label="Naslov")
                summary_output = gr.Textbox(label="Povzetek")
                sentiment_output = gr.Label(label="Sentiment")
            
            analyze_btn.click(
                fn=self.process_article,
                inputs=[url_input, keywords_input],
                outputs=[title_output, summary_output, sentiment_output]
            )
        
        # Zaženi vmesnik
        interface.launch(share=True) 