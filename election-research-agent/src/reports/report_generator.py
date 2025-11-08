from typing import Dict, Any
import logging
from datetime import datetime
import json
import os
from pathlib import Path

class ReportGenerator:
    """Agent responsible for generating comprehensive election analysis reports."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.logger = logging.getLogger(__name__)
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)
    
    def generate(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive report from the analysis results.
        
        Args:
            analysis_results (Dict[str, Any]): Results from the analysis pipeline
            
        Returns:
            str: Path to the generated report file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.report_dir / f"election_analysis_{timestamp}.md"
            
            report_content = self._create_report_content(analysis_results)
            
            # Save the report
            report_path.write_text(report_content)
            
            # Save raw data for reference
            raw_data_path = self.report_dir / f"raw_data_{timestamp}.json"
            raw_data_path.write_text(json.dumps(analysis_results, indent=2))
            
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _create_report_content(self, analysis_results: Dict[str, Any]) -> str:
        """
        Create the content for the report in Markdown format.
        
        Args:
            analysis_results (Dict[str, Any]): Results from the analysis pipeline
            
        Returns:
            str: Formatted report content
        """
        try:
            predictions = analysis_results.get('predictions', {})
            news_analysis = analysis_results.get('news_analysis', {})
            social_analysis = analysis_results.get('social_analysis', {})
            
            report = [
                "# Election Analysis Report",
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                
                "## Executive Summary",
                self._generate_executive_summary(predictions),
                
                "## News Analysis",
                self._format_news_analysis(news_analysis),
                
                "## Social Media Analysis",
                self._format_social_analysis(social_analysis),
                
                "## Predictions",
                self._format_predictions(predictions),
                
                "## Methodology",
                self._generate_methodology_section()
            ]
            
            return "\n\n".join(report)
            
        except Exception as e:
            self.logger.error(f"Error creating report content: {str(e)}")
            raise
    
    def _generate_executive_summary(self, predictions: Dict[str, Any]) -> str:
        """Generate the executive summary section."""
        try:
            confidence = predictions.get('confidence', 0)
            prediction_results = predictions.get('predictions', {})
            
            summary = [
                "Based on our comprehensive analysis of news and social media data,",
                f"we predict the following election outcomes with {confidence:.1%} confidence:"
            ]
            
            for candidate, probability in prediction_results.items():
                summary.append(f"- {candidate}: {probability:.1%}")
            
            return "\n".join(summary)
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {str(e)}")
            return "Error generating executive summary"
    
    def _format_news_analysis(self, news_analysis: Dict[str, Any]) -> str:
        """Format the news analysis section."""
        try:
            return f"""### Overview
- Number of articles analyzed: {news_analysis.get('article_count', 0)}

### Key Findings
{news_analysis.get('meta_analysis', 'No analysis available')}"""
            
        except Exception as e:
            self.logger.error(f"Error formatting news analysis: {str(e)}")
            return "Error formatting news analysis"
    
    def _format_social_analysis(self, social_analysis: Dict[str, Any]) -> str:
        """Format the social media analysis section."""
        try:
            twitter = social_analysis.get('twitter_analysis', {})
            
            return f"""### Twitter Analysis
- Number of tweets analyzed: {twitter.get('tweet_count', 0)}
- Overall sentiment: {social_analysis.get('overall_sentiment', 0):.2f}

### Key Findings
{twitter.get('sentiment_analysis', 'No analysis available')}"""
            
        except Exception as e:
            self.logger.error(f"Error formatting social analysis: {str(e)}")
            return "Error formatting social analysis"
    
    def _format_predictions(self, predictions: Dict[str, Any]) -> str:
        """Format the predictions section."""
        try:
            results = predictions.get('predictions', {})
            confidence = predictions.get('confidence', 0)
            
            prediction_lines = [
                f"### Prediction Confidence: {confidence:.1%}",
                "",
                "### Predicted Outcomes"
            ]
            
            for candidate, probability in results.items():
                prediction_lines.append(f"- {candidate}: {probability:.1%}")
            
            return "\n".join(prediction_lines)
            
        except Exception as e:
            self.logger.error(f"Error formatting predictions: {str(e)}")
            return "Error formatting predictions"
    
    def _generate_methodology_section(self) -> str:
        """Generate the methodology section."""
        return """Our analysis combines multiple data sources and advanced AI techniques:

1. **Data Collection**
   - News articles from major publications
   - Social media posts and engagement metrics
   
2. **Analysis Techniques**
   - Natural Language Processing for content analysis
   - Sentiment Analysis
   - Topic Modeling
   
3. **Prediction Model**
   - Machine Learning-based prediction
   - Confidence scoring based on data quality and coverage"""