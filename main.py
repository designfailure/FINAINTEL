import logging
from src.collectors.web_scraper import FinancialWebScraper
from src.collectors.news_api import NewsAPICollector
from src.processors.cleaner import TextCleaner
from src.analyzers.summarizer import FinancialSummarizer
from src.analyzers.sentiment import FinancialSentimentAnalyzer
from src.analyzers.evaluator import SummaryEvaluator
import json
from datetime import datetime

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize components
    scraper = FinancialWebScraper()
    news_api = NewsAPICollector(api_key="YOUR_API_KEY")
    cleaner = TextCleaner()
    summarizer = FinancialSummarizer()
    sentiment_analyzer = FinancialSentimentAnalyzer()
    evaluator = SummaryEvaluator()

    # Collect news
    logger.info("Collecting news articles...")
    articles = news_api.get_financial_news(days=1)

    results = []
    for article in articles:
        # Clean text
        cleaned_text = cleaner.clean_text(article['content'])
        
        # Generate summary
        summary = summarizer.generate_summary(cleaned_text)
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze_sentiment(summary)
        
        # Evaluate summary
        evaluation = evaluator.evaluate_summary(article['content'], summary)
        
        results.append({
            'title': article['title'],
            'original_text': article['content'],
            'summary': summary,
            'source': article['url'],
            'sentiment': sentiment,
            'evaluation': evaluation
        })

    # Calculate average scores
    avg_scores = evaluator.calculate_average_scores([r['evaluation'] for r in results])
    logger.info(f"Average evaluation scores: {avg_scores}")

    # Save results to JSON for visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"data/processed/results_{timestamp}.json", "w") as f:
        json.dump(results, f)

    logger.info(f"Results saved to data/processed/results_{timestamp}.json")

if __name__ == "__main__":
    main()

