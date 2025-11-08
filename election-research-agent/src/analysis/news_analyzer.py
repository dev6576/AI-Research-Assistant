from typing import Dict, List, Any
import logging
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from newspaper import Article
import numpy as np

class NewsAnalyzer:
    """Agent responsible for analyzing news articles and extracting relevant election information."""
    
    def __init__(self):
        """Initialize the news analyzer with necessary components."""
        self.logger = logging.getLogger(__name__)
        self.llm = ChatOpenAI(temperature=0)
        
    def analyze(self, news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze news articles for election-related information.
        
        Args:
            news_data (List[Dict[str, Any]]): List of news articles with their metadata
            
        Returns:
            Dict[str, Any]: Analysis results including sentiment, topics, and key findings
        """
        try:
            analyzed_articles = []
            
            for article in news_data:
                analysis = self._analyze_single_article(article)
                analyzed_articles.append(analysis)
            
            return self._aggregate_analysis(analyzed_articles)
            
        except Exception as e:
            self.logger.error(f"Error analyzing news data: {str(e)}")
            raise
    
    def _analyze_single_article(self, article: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze a single news article using LLM.
        
        Args:
            article (Dict[str, str]): Article data including URL and content
            
        Returns:
            Dict[str, Any]: Analysis of the single article
        """
        try:
            # Parse article using newspaper3k
            parsed_article = Article(article['url'])
            parsed_article.download()
            parsed_article.parse()
            parsed_article.nlp()
            
            # Use LLM for detailed analysis
            messages = [
                SystemMessage(content="You are an expert political analyst. Analyze this news article for election-related information."),
                HumanMessage(content=f"Title: {parsed_article.title}\n\nContent: {parsed_article.text}")
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                'url': article['url'],
                'title': parsed_article.title,
                'summary': parsed_article.summary,
                'keywords': parsed_article.keywords,
                'llm_analysis': response.content,
                'publication_date': parsed_article.publish_date,
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing article {article.get('url', 'unknown')}: {str(e)}")
            return {'error': str(e), 'url': article.get('url', 'unknown')}
    
    def _aggregate_analysis(self, analyzed_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate the analysis of multiple articles.
        
        Args:
            analyzed_articles (List[Dict[str, Any]]): List of analyzed articles
            
        Returns:
            Dict[str, Any]: Aggregated analysis results
        """
        try:
            # Combine all LLM analyses for a meta-analysis
            combined_analysis = "\n\n".join([a['llm_analysis'] for a in analyzed_articles if 'llm_analysis' in a])
            
            messages = [
                SystemMessage(content="You are an expert political analyst. Provide a meta-analysis of these news analyses."),
                HumanMessage(content=combined_analysis)
            ]
            
            meta_analysis = self.llm.invoke(messages)
            
            return {
                'meta_analysis': meta_analysis.content,
                'article_count': len(analyzed_articles),
                'individual_analyses': analyzed_articles
            }
            
        except Exception as e:
            self.logger.error(f"Error in aggregating analysis: {str(e)}")
            raise