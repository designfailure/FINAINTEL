# FINAINTEL

https://colab.research.google.com/drive/1JBd68_4MjbweeKoi9MXojqOASq_pZT_w?usp=sharing



"Financial AI and News Intelligence" -  financial news summarization and sentiment analysis pipeline

The workflow overview focuses on summarizing financial news articles through a structured approach involving data collection, preprocessing, summarization, and output storage. The phase pipeline also involves analyzing the sentiment of the summarized articles.

![Financial NEWS summarization   sentiment ](https://github.com/user-attachments/assets/c7fdb800-0806-436a-a0da-3c24537c160a)

![image](https://github.com/user-attachments/assets/823a40a6-0d1e-47cd-863a-229650cc6b7f)


Data Collection involves gathering financial news articles through two primary methods. The first method is Web Scraping, utilizing libraries such as BeautifulSoup and Scrapy to extract articles from reputable financial news sources like Bloomberg, Reuters, and Financial Times. The second method is API Integration, where tools like NewsAPI are employed to programmatically fetch articles, ensuring a steady stream of relevant content.

![data colection 01](https://github.com/user-attachments/assets/1f33e23e-bc19-435d-b9e0-b405ed9265d3)


Following data collection, the Data Preprocessing stage is crucial. This includes Text Cleaning, which removes special characters, HTML tags, and stop words to enhance the quality of the text. Next, Text Normalization converts all text to lowercase and applies stemming to reduce words to their base forms. The text is then split into manageable pieces through Tokenization, allowing for easier analysis. Additionally, Metadata Extraction captures essential information such as publication date, source, and relevant tags.

![data colection 02](https://github.com/user-attachments/assets/bca29489-5d90-4fec-8c3c-fc2ceed583c6)


The core of this phase is the Summarization process. Here, model selection is pivotal; pre-trained models like T5 and BERT are utilized to generate concise summaries that reflect the main points and essential details of the original articles. The final output consists of these summaries stored in a structured format such as JSON or CSV.

Additional preprocessing ensures that these summaries are clean and tokenized for effective analysis. The heart of this phase is the Sentiment Analysis, which involves selecting an appropriate model like FinBERT for sentiment classification. Each summary is classified as positive, negative, or neutral based on its content. Furthermore, the analysis distinguishes between varying degrees of sentiment, such as strongly positive or mildly negative.

![sentiment analyzer](https://github.com/user-attachments/assets/f4d02fe3-6c2e-47d5-8863-94a656f2dbc8)


The output from this phase includes Sentiment Scores, which are stored in a structured format for further use.
Finally, an Evaluation step assesses the performance of both the summarization and sentiment analysis models using metrics like ROUGE and F-1 scores. Visualization tools such as Grafana are employed to present results and performance metrics clearly.
![image](https://github.com/user-attachments/assets/811c5e00-a389-4b8e-bb84-a627355167b6)


This comprehensive workflow effectively combines data collection, processing, summarization, sentiment analysis, and evaluation to provide valuable insights into financial news trends and sentiments.

https://finance-narrator.lovable.app/
![image](https://github.com/user-attachments/assets/6eab0a80-fc96-4f51-ac37-292f94b34a55)


https://finance-gist-ai.lovable.app/
![image](https://github.com/user-attachments/assets/ba3845c6-a70a-4b1e-80db-fa7b10042747)



For fine-tuning it could be used the “financial summarization” dataset from HuggingFace, https://huggingface.co/datasets/Lightscale/financial-advise-summarization or using the https://www.kaggle.com/datasets/sbhatti/financial-sentiment-analysis data is intended for advancing financial sentiment analysis research. It's two datasets (FiQA, Financial PhraseBank) combined into one easy-to-use CSV file. It provides financial sentences with sentiment labels.

#SOCIAL LISTENING#

Integrating social listening tools and libraries into the financial news summarization and sentiment analysis pipeline can significantly enhance the overall system by providing a more comprehensive view of public sentiment and perception around financial news. Here’s how embedded social listening tools and libraries can enhance the pipeline.
https://www.meltwater.com/en/suite/social-listening-analytics

https://mentionmind.com/

https://github.com/obsei/obsei 



# Intelligent GenAI-Driven Financial News Summarization and Sentiment Analysis

## Project Objective

An intelligent application that uses Generative AI to summarize financial news articles from various sources and analyze the sentiment expressed in these articles and their summaries. The goal is to provide concise, accurate, and informative summaries along with sentiment classifications (positive, negative, or neutral) to aid financial analysis and decision-making.

## Project Phases

This project is structured in two essential phases:

**Phase 1: Financial News Summarization**

*   **Objective:** To build a system capable of summarizing financial news content from web pages and news APIs.
*   **Data Sources:**
    *   Web Scraping: Bloomberg, Reuters, Financial Times, Finance.si
    *   News APIs: NewsAPI
*   **Tools & Libraries:**
    *   Web Scraping: `beautifulsoup4`, `requests`
    *   News API: `newsapi-python`
    *   Text Preprocessing: `nltk` (stopwords, tokenization), `re`
    *   Summarization Model: `transformers` (Hugging Face `pipeline`, e.g., `facebook/bart-large-cnn`)
*   **Expected Outcomes:**
    *   Accurate summaries reflecting main points and details of original articles.
    *   Summaries in clear, fluent language, understandable for non-experts.
    *   Concise summaries preserving overall meaning and context.
    *   Focus on financially relevant information (company performance, market trends, etc.).
    *   Reflection of the original article's tone in the summary.

**Phase 2: Sentiment Analysis**

*   **Objective:** To enhance the summarization pipeline with sentiment analysis capabilities, classifying the sentiment of both original articles and their summaries.
*   **Sentiment Classification:** Positive, Negative, or Neutral.
*   **Tools & Libraries:**
    *   Sentiment Analysis Model: `transformers` (Hugging Face, e.g., FinBERT from `ProsusAI/finbert`)
    *   Data Handling & Preparation: `pandas`, `numpy`
    *   Text Cleaning: `re`, `nltk`
    *   Tokenization: `nltk`
*   **Expected Outcomes:**
    *   Reliable sentiment classification of text.
    *   Distinction between degrees of sentiment.
    *   Correct interpretation of ambiguous financial language.
    *   Sentiment analysis for both original articles and generated summaries.

## Evaluation Metrics

*   **Summarization Quality:** ROUGE scores
*   **Sentiment Analysis Accuracy:** F-1 score

## Future Enhancements (Mentioned in Project Description)

*   Data Visualization: Grafana integration for advanced dashboards.
*   Email Notifications: Sending summaries and sentiment analysis results via email.
*   Social Listening: Integration with social media data using tools like Meltwater, MentionMind, Obsei.
*   
