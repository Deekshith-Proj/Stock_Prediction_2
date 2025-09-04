import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class FinBERTAnalyzer:
    def __init__(self):
        self.model_name = "ProsusAI/finbert"
        self.tokenizer = None
        self.model = None
        self._model_loaded = False
    
    def _load_model(self):
        """Load the FinBERT model and tokenizer"""
        if self._model_loaded:
            return
            
        try:
            logger.info("Loading FinBERT model...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self._model_loaded = True
            logger.info("FinBERT model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading FinBERT model: {e}")
            raise
    
    def extract_stock_tickers(self, text: str) -> List[str]:
        """Extract stock tickers from text using regex pattern $TICKER"""
        pattern = r'\$([A-Z]{1,5})'
        tickers = re.findall(pattern, text.upper())
        return list(set(tickers))  # Remove duplicates
    
    def clean_text(self, text: str) -> str:
        """Clean text by removing emojis, links, and extra whitespace"""
        # Remove emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        
        # Remove URLs
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        text = url_pattern.sub('', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text using FinBERT
        Returns: (sentiment_label, confidence_score)
        """
        try:
            # Load model if not already loaded
            self._load_model()
            
            # Clean the text
            cleaned_text = self.clean_text(text)
            
            if len(cleaned_text.strip()) < 3:
                return "neutral", 0.0
            
            # Tokenize and predict
            inputs = self.tokenizer(cleaned_text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get the predicted class and confidence
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = predictions[0][predicted_class].item()
            
            # Map to sentiment labels (FinBERT: 0=positive, 1=negative, 2=neutral)
            sentiment_map = {0: "positive", 1: "negative", 2: "neutral"}
            sentiment_label = sentiment_map[predicted_class]
            
            # Convert confidence to sentiment score (-1 to 1)
            if sentiment_label == "positive":
                sentiment_score = confidence
            elif sentiment_label == "negative":
                sentiment_score = -confidence
            else:  # neutral
                sentiment_score = 0.0
            
            return sentiment_label, sentiment_score
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return "neutral", 0.0
    
    def process_text(self, text: str) -> List[Dict[str, any]]:
        """
        Process text to extract stock mentions and analyze sentiment
        Returns: List of dicts with ticker, sentiment, and score
        """
        results = []
        
        # Extract stock tickers
        tickers = self.extract_stock_tickers(text)
        
        if not tickers:
            return results
        
        # Analyze sentiment for the entire text
        sentiment_label, sentiment_score = self.analyze_sentiment(text)
        
        # Create result for each ticker found
        for ticker in tickers:
            results.append({
                "ticker": ticker,
                "text": text,
                "sentiment": sentiment_label,
                "sentiment_score": sentiment_score
            })
        
        return results

# Note: Create analyzer instances as needed to avoid loading the model at import time
