from typing import List, Dict, Any
from datetime import datetime
import json
import logging
from .analysis.news_analyzer import NewsAnalyzer
from .analysis.social_media_analyzer import SocialMediaAnalyzer
from .data.data_collector import DataCollector
from .models.prediction_model import PredictionModel
from .models.local_llm import LocalLLMHandler
from .reports.report_generator import ReportGenerator

class ElectionResearchSystem:
    """Main class orchestrating the election research agent system."""
    
    def __init__(self):
        """Initialize the election research system with its component agents."""
        self.data_collector = DataCollector()
        self.news_analyzer = NewsAnalyzer()
        self.social_media_analyzer = SocialMediaAnalyzer()
        self.prediction_model = PredictionModel()
        self.report_generator = ReportGenerator()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize local LLM handler
        self.llm_handler = LocalLLMHandler()
    
    def parse_election_query(self, query: str) -> Dict[str, Any]:
        """
        Parse a natural language query about an election into structured parameters.
        
        Args:
            query (str): Natural language query about an election
            
        Returns:
            Dict[str, Any]: Structured parameters including election type, location, date, candidates
        """
        try:
            self.logger.info(f"Parsing query: {query}")
            parameters = self.llm_handler.parse_election_query(query)
            self.logger.info(f"Extracted parameters: {parameters}")
            return parameters
            
        except Exception as e:
            self.logger.error(f"Error parsing query: {str(e)}")
            raise
    
    def run_analysis(self, query: str) -> Dict[str, Any]:
        """
        Execute the full analysis pipeline based on a natural language query.
        
        Args:
            query (str): Natural language query about an election
            
        Returns:
            Dict[str, Any]: Analysis results including predictions and confidence scores
        """
        try:
            # Parse the natural language query
            election_params = self.parse_election_query(query)
            
            # Collect data from various sources with the extracted parameters
            self.logger.info("Starting data collection...")
            raw_data = self.data_collector.collect(election_params)
            
            # Analyze news content using local LLM
            self.logger.info("Analyzing news content...")
            news_data = raw_data['news']
            news_analysis = {
                'articles': news_data,
                'analysis': self.llm_handler.analyze_content(
                    '\n'.join(article['text'] for article in news_data),
                    'news article'
                )
            }
            
            # Analyze social media using local LLM
            self.logger.info("Analyzing social media content...")
            social_data = raw_data['social']['twitter']
            social_analysis = {
                'tweets': social_data,
                'analysis': self.llm_handler.analyze_content(
                    '\n'.join(tweet['text'] for tweet in social_data),
                    'social media'
                )
            }
            
            # Generate predictions using local LLM
            self.logger.info("Generating predictions...")
            predictions = self.llm_handler.generate_prediction([
                news_analysis['analysis'],
                social_analysis['analysis']
            ])
            
            return {
                'timestamp': datetime.now().isoformat(),
                'query_parameters': election_params,
                'news_analysis': news_analysis,
                'social_analysis': social_analysis,
                'predictions': predictions
            }
            
        except Exception as e:
            self.logger.error(f"Error in analysis pipeline: {str(e)}")
            raise
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive report from the analysis results.
        
        Args:
            analysis_results (Dict[str, Any]): Results from run_analysis()
            
        Returns:
            str: Path to the generated report file
        """
        try:
            self.logger.info("Generating analysis report...")
            report_path = self.report_generator.generate(analysis_results)
            self.logger.info(f"Report generated successfully at: {report_path}")
            return report_path
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    system = ElectionResearchSystem()
    
    # Example natural language query
    query = "What are the predictions for the 2024 US Presidential election between Joe Biden and Donald Trump?"
    
    # Run analysis based on the query
    results = system.run_analysis(query)
    report_path = system.generate_report(results)
    print(f"Analysis complete. Report available at: {report_path}")