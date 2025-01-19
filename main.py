import yaml
import os
from src.data_collection.news_api_client import NewsAPIClient
from src.data_collection.news_scraper import FinancialNewsScraper
from src.preprocessing.text_cleaner import TextCleaner
from src.summarization.summarizer import NewsSummarizer
from dotenv import load_dotenv
import logging
from src.sentiment.analyzer import FinancialSentimentAnalyzer
from src.visualization.dashboard import SentimentDashboard
from src.interface.gradio_app import FinancialNewsGUI
from src.evaluation.evaluator import FinancialNewsEvaluator

def load_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    # Naloži okolijske spremenljivke in konfiguracijo
    load_dotenv()
    config = load_config()
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Inicializacija komponent
    news_api = NewsAPIClient(os.getenv('NEWS_API_KEY'))
    scraper = FinancialNewsScraper()
    cleaner = TextCleaner()
    summarizer = NewsSummarizer(config['summarization']['model_name'])
    
    # Inicializacija novih komponent
    sentiment_analyzer = FinancialSentimentAnalyzer(
        config['sentiment_analysis']['model_name']
    )
    dashboard = SentimentDashboard(
        config['visualization']['grafana']['host'],
        config['visualization']['grafana']['port']
    )
    
    # Inicializacija evaluatorja
    evaluator = FinancialNewsEvaluator()
    
    try:
        # Pridobi novice iz API-ja
        articles = news_api.fetch_financial_news(
            sources=config['data_collection']['news_api']['sources'],
            language=config['data_collection']['news_api']['language']
        )
        
        all_results = []
        for article in articles:
            # Čiščenje besedila
            cleaned_text = cleaner.clean_text(article.content)
            
            # Generiranje povzetka
            summary = summarizer.summarize(
                cleaned_text,
                max_length=config['summarization']['max_length'],
                min_length=config['summarization']['min_length']
            )
            
            # Analiza sentimenta
            sentiment_result = sentiment_analyzer.analyze_sentiment(summary)
            
            if sentiment_result:
                logger.info(f"Članek: {article.title}")
                logger.info(f"Povzetek: {summary}")
                logger.info(f"Sentiment: {sentiment_result.sentiment} "
                          f"(zaupanje: {sentiment_result.confidence:.2f})\n")
                
                all_results.append({
                    'title': article.title,
                    'summary': summary,
                    'sentiment': sentiment_result.sentiment,
                    'confidence': sentiment_result.confidence,
                    'timestamp': article.published_at
                })
        
        # Pripravi podatke za evalvacijo
        original_texts = [article.content for article in articles]
        generated_summaries = []
        predicted_sentiments = []
        confidence_scores = []
        
        for article in articles:
            cleaned_text = cleaner.clean_text(article.content)
            summary = summarizer.summarize(cleaned_text)
            sentiment_result = sentiment_analyzer.analyze_sentiment(summary)
            
            generated_summaries.append(summary)
            if sentiment_result:
                predicted_sentiments.append(sentiment_result.sentiment)
                confidence_scores.append(sentiment_result.confidence)
            
            # Analiza sentimenta
            sentiment_result = sentiment_analyzer.analyze_sentiment(summary)
            
            if sentiment_result:
                logger.info(f"Članek: {article.title}")
                logger.info(f"Povzetek: {summary}")
                logger.info(f"Sentiment: {sentiment_result.sentiment} "
                          f"(zaupanje: {sentiment_result.confidence:.2f})\n")
                
                all_results.append({
                    'title': article.title,
                    'summary': summary,
                    'sentiment': sentiment_result.sentiment,
                    'confidence': sentiment_result.confidence,
                    'timestamp': article.published_at
                })
        
        # Izvedi evalvacijo
        summary_eval = evaluator.evaluate_summaries(
            original_texts,
            generated_summaries
        )
        
        # Za demonstracijo uporabimo nekaj označenih podatkov
        # V praksi bi morali imeti ročno označene podatke
        demo_true_sentiments = ["positive"] * 3 + ["negative"] * 2 + ["neutral"] * 2
        sentiment_eval = evaluator.evaluate_sentiment(
            demo_true_sentiments[:len(predicted_sentiments)],
            predicted_sentiments,
            confidence_scores
        )
        
        # Generiraj poročilo
        evaluation_report = evaluator.generate_evaluation_report(
            summary_eval,
            sentiment_eval
        )
        
        # Vizualiziraj rezultate
        evaluator.visualize_results(
            summary_eval,
            sentiment_eval,
            output_path="evaluation_results"
        )
        
        logger.info("Evalvacijsko poročilo:\n" + evaluation_report)
        
        # Ustvari dashboard
        dashboard_id = dashboard.create_sentiment_dashboard(
            config['visualization']['grafana']['dashboard_title']
        )
        
        if dashboard_id:
            logger.info(f"Dashboard ustvarjen z ID: {dashboard_id}")
        
        # Zaženi Gradio vmesnik
        gui = FinancialNewsGUI(config)
        gui.launch_interface()
        
    except Exception as e:
        logger.error(f"Napaka v glavni skripti: {str(e)}")

if __name__ == "__main__":
    main() 