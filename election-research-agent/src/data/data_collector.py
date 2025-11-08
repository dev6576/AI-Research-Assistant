from typing import Dict, List, Any
import logging
import requests
from datetime import datetime, timedelta
import tweepy
from newspaper import Article, ArticleException
import os
from dotenv import load_dotenv

class DataCollector:
    """Agent responsible for collecting data from various sources."""
    
    def __init__(self):
        """Initialize the data collector with necessary API clients."""
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self._setup_apis()
        
    def _setup_apis(self):
        """Set up API clients for various data sources."""
        try:
            # Twitter API setup
            auth = tweepy.OAuthHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET')
            )
            auth.set_access_token(
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.twitter_client = tweepy.API(auth)
            
            # News API setup
            self.news_api_key = os.getenv('NEWS_API_KEY')
            
        except Exception as e:
            self.logger.error(f"Error setting up APIs: {str(e)}")
            raise
    
    def collect(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect data from all configured sources based on election parameters.
        
        Args:
            params (Dict[str, Any]): Structured election parameters including:
                - election_type: type of election
                - country: country where the election is held
                - region: specific region/state if applicable
                - date: election date or timeframe
                - candidates: list of candidates
                - keywords: relevant keywords
                - hashtags: relevant hashtags
        
        Returns:
            Dict[str, Any]: Collected data from various sources
        """
        try:
            news_data = self._collect_news(params)
            social_data = self._collect_social_media(params)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'parameters': params,
                'news': news_data,
                'social': social_data
            }
            
        except Exception as e:
            self.logger.error(f"Error collecting data: {str(e)}")
            raise
    
    def _collect_news(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Collect news articles from various sources based on election parameters.
        
        Args:
            params (Dict[str, Any]): Structured election parameters
        
        Returns:
            List[Dict[str, Any]]: Collection of news articles
        """
        try:
            # Build search query from parameters
            search_terms = []
            
            # Add election type and location
            if params.get('election_type'):
                search_terms.append(params['election_type'])
            if params.get('country'):
                search_terms.append(params['country'])
            if params.get('region'):
                search_terms.append(params['region'])
            
            # Add candidates
            candidates = params.get('candidates', [])
            if candidates:
                search_terms.extend([f'"{c}"' for c in candidates])
            
            # Add keywords
            search_terms.extend(params.get('keywords', []))
            
            # Combine into search query
            query = ' AND '.join(search_terms)
            
            # Use News API to get election-related articles
            base_url = "https://newsapi.org/v2/everything"
            api_params = {
                'q': query,
                'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.news_api_key
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            # Process and clean articles
            processed_articles = []
            for article in articles:
                try:
                    # Use newspaper3k to extract clean text
                    article_obj = Article(article['url'])
                    article_obj.download()
                    article_obj.parse()
                    
                    processed_articles.append({
                        'url': article['url'],
                        'title': article['title'],
                        'text': article_obj.text,
                        'published_at': article['publishedAt'],
                        'source': article['source']['name']
                    })
                except ArticleException as ae:
                    self.logger.warning(f"Error processing article {article['url']}: {str(ae)}")
                    continue
                
            return processed_articles
            
        except Exception as e:
            self.logger.error(f"Error collecting news data: {str(e)}")
            raise
    
    def _collect_social_media(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect social media data from various platforms based on parameters.
        
        Args:
            params (Dict[str, Any]): Structured election parameters
            
        Returns:
            Dict[str, Any]: Collection of social media data
        """
        try:
            # Collect Twitter data
            twitter_data = self._collect_twitter(params)
            
            # Add other social media platforms here
            
            return {
                'twitter': twitter_data,
                'parameters': params  # Include parameters for context
            }
            
        except Exception as e:
            self.logger.error(f"Error collecting social media data: {str(e)}")
            raise
    
    def _collect_twitter(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Collect election-related tweets based on parameters.
        
        Args:
            params (Dict[str, Any]): Structured election parameters
            
        Returns:
            List[Dict[str, Any]]: Collection of relevant tweets
        """
        try:
            # Build search query from parameters
            search_terms = []
            
            # Add election type and location
            if params.get('election_type'):
                search_terms.append(params['election_type'])
            if params.get('country'):
                search_terms.append(params['country'])
            if params.get('region'):
                search_terms.append(params['region'])
            
            # Add candidates
            candidates = params.get('candidates', [])
            if candidates:
                search_terms.extend([f'"{c}"' for c in candidates])
            
            # Add hashtags
            hashtags = params.get('hashtags', [])
            if hashtags:
                search_terms.extend(hashtags)
            
            # Combine into search query
            query = ' '.join(search_terms) + ' -filter:retweets'
            tweets = []
            
            # Collect tweets from the past week
            for tweet in tweepy.Cursor(
                self.twitter_client.search_tweets,
                q=query,
                tweet_mode="extended",
                lang="en"
            ).items(1000):  # Limit to 1000 tweets for MVP
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.full_text,
                    'created_at': tweet.created_at,
                    'user': tweet.user.screen_name,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count
                })
            
            return tweets
            
            # Collect tweets from the past week
            for tweet in tweepy.Cursor(
                self.twitter_client.search_tweets,
                q=search_query,
                tweet_mode="extended",
                lang="en"
            ).items(1000):  # Limit to 1000 tweets for MVP
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.full_text,
                    'created_at': tweet.created_at,
                    'user': tweet.user.screen_name,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count
                })
            
            return tweets
            
        except Exception as e:
            self.logger.error(f"Error collecting Twitter data: {str(e)}")
            raise