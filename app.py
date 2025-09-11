from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime, timedelta
import random
import requests
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Initialize VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()

def get_real_stock_data(symbol):
    """Fetch real stock data from Yahoo Finance API with Indian stock support"""
    try:
        # List of Indian stocks that need .NS suffix
        indian_stocks = [
            'TCS', 'INFY', 'WIPRO', 'HCLTECH', 'TECHM', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 
            'AXISBANK', 'SBIN', 'RELIANCE', 'HINDUNILVR', 'ITC', 'BHARTIARTL', 'MARUTI', 
            'SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB', 'BIOCON', 'ONGC', 'IOC', 'BPCL', 
            'ADANIGREEN', 'TATAPOWER', 'ZOMATO', 'PAYTM', 'POLICYBZR', 'NAZARA'
        ]
        
        # Add .NS suffix for Indian stocks
        yahoo_symbol = f"{symbol}.NS" if symbol in indian_stocks else symbol
        
        # Using Yahoo Finance API with specific parameters for 30 days of data
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?interval=1d&range=30d"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            if "timestamp" in result and "indicators" in result:
                timestamps = result["timestamp"]
                quotes = result["indicators"]["quote"][0]
                
                # Get all available data points (up to 30 days)
                chart_data = []
                current_price = 0
                previous_price = 0
                
                # Process all available timestamps
                for i, timestamp in enumerate(timestamps):
                    if (i < len(quotes["close"]) and 
                        quotes["close"][i] is not None and 
                        quotes["close"][i] > 0):
                        
                        price = float(quotes["close"][i])
                        volume = int(quotes["volume"][i]) if quotes["volume"][i] is not None else 0
                        
                        chart_data.append({
                            "date": timestamp * 1000,  # Convert to milliseconds
                            "price": round(price, 2),  # Ensure 2 decimal places
                            "volume": volume
                        })
                
                # Get current and previous prices from the last two valid data points
                if len(chart_data) >= 2:
                    current_price = chart_data[-1]["price"]
                    previous_price = chart_data[-2]["price"]
                elif len(chart_data) == 1:
                    current_price = chart_data[0]["price"]
                    previous_price = current_price
                else:
                    # Fallback if no data
                    current_price = 0
                    previous_price = 0
                
                # Calculate price change
                if previous_price == 0:
                    previous_price = current_price
                price_change = current_price - previous_price
                price_change_percent = (price_change / previous_price) * 100 if previous_price != 0 else 0
                
                return {
                    "chart_data": chart_data,
                    "current_price": round(current_price, 2),
                    "price_change": round(price_change, 2),
                    "price_change_percent": round(price_change_percent, 2),
                    "data_timestamp": datetime.now().isoformat(),
                    "data_source": "Yahoo Finance (Real-time)"
                }
        else:
            # Fallback to simulated data if API fails
            return get_simulated_stock_data(symbol)
            
    except Exception as e:
        print(f"Error fetching real stock data: {e}")
        # Fallback to simulated data
        return get_simulated_stock_data(symbol)

def get_simulated_stock_data(symbol):
    """Generate simulated stock data as fallback"""
    base_price = random.uniform(50, 300)
    chart_data = []
    current_price = base_price
    
    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        timestamp = int(date.timestamp() * 1000)
        
        # Random walk for price
        change = random.uniform(-0.05, 0.05)
        current_price = current_price * (1 + change)
        
        chart_data.append({
            "date": timestamp,
            "price": round(current_price, 2),
            "volume": random.randint(1000000, 10000000)
        })
    
    # Calculate price change
    previous_price = chart_data[-2]["price"] if len(chart_data) > 1 else current_price
    price_change = current_price - previous_price
    price_change_percent = (price_change / previous_price) * 100 if previous_price != 0 else 0
    
    return {
        "chart_data": chart_data,
        "current_price": round(current_price, 2),
        "price_change": round(price_change, 2),
        "price_change_percent": round(price_change_percent, 2),
        "data_timestamp": datetime.now().isoformat(),
        "data_source": "Simulated Data (Fallback)"
    }

def get_real_news_from_yahoo(symbol, company_name):
    """Fetch real news from Yahoo Finance API with stock-specific filtering"""
    try:
        # Yahoo Finance news API endpoint - search for specific stock
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}&quotesCount=1&newsCount=15"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        news_items = []
        if "news" in data and data["news"]:
            # Filter news to ensure it's related to the specific stock
            filtered_news = []
            for news in data["news"]:
                title = news.get("title", "").lower()
                summary = news.get("summary", "").lower()
                
                # Check if news is related to the stock symbol or company name
                is_relevant = (
                    symbol.lower() in title or 
                    symbol.lower() in summary or
                    company_name.lower().split()[0] in title or  # First word of company name
                    any(word in title for word in company_name.lower().split()[:2])  # First two words
                )
                
                if is_relevant:
                    filtered_news.append(news)
            
            # Take up to 8 relevant news items
            for news in filtered_news[:8]:
                # Extract news content
                title = news.get("title", "")
                summary = news.get("summary", "")
                link = news.get("link", f"https://finance.yahoo.com/quote/{symbol}")
                publisher = news.get("publisher", "Yahoo Finance")
                published = news.get("providerPublishTime", int(datetime.now().timestamp()))
                
                # Perform ML sentiment analysis on the news content
                sentiment_result = analyze_sentiment_ml(title + " " + summary)
                
                news_items.append({
                    'title': title,
                    'summary': summary,
                    'link': link,
                    'publisher': publisher,
                    'published': published,
                    'sentiment': sentiment_result['sentiment'],
                    'confidence': sentiment_result['confidence']
                })
        
        # If we don't have enough relevant news, try alternative method
        if len(news_items) < 3:
            print(f"Not enough relevant news found for {symbol}, trying alternative method...")
            return get_alternative_news(symbol, company_name)
        
        return news_items
        
    except Exception as e:
        print(f"Error fetching real news from Yahoo Finance: {e}")
        # Fallback to alternative news source
        return get_alternative_news(symbol, company_name)

def get_alternative_news(symbol, company_name):
    """Alternative news scraping method with multiple Indian news sources"""
    try:
        news_items = []
        
        # List of Indian news sources to try
        indian_news_sources = [
            {
                'name': 'Yahoo Finance India',
                'url': f"https://finance.yahoo.com/quote/{symbol}.NS/news",
                'selector': 'h3.Mb\\(5px\\)'
            },
            {
                'name': 'Economic Times',
                'url': f"https://economictimes.indiatimes.com/markets/stocks/news",
                'selector': '.eachStory h3 a'
            },
            {
                'name': 'Business Standard',
                'url': f"https://www.business-standard.com/markets",
                'selector': '.story-heading a'
            }
        ]
        
        # Try Yahoo Finance first (most reliable)
        try:
            url = f"https://finance.yahoo.com/quote/{symbol}.NS/news"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for news articles in the page
            news_elements = soup.find_all('h3', class_='Mb(5px)')
            
            for i, element in enumerate(news_elements[:6]):  # Limit to 6 items
                title = element.get_text().strip()
                if title and (symbol.lower() in title.lower() or company_name.lower().split()[0] in title.lower()):
                    # Find the link
                    link_element = element.find('a')
                    link = link_element.get('href') if link_element else f"https://finance.yahoo.com/quote/{symbol}.NS"
                    
                    # Perform ML sentiment analysis
                    sentiment_result = analyze_sentiment_ml(title)
                    
                    news_items.append({
                        'title': title,
                        'summary': f"Latest news about {company_name} from Yahoo Finance",
                        'link': link,
                        'publisher': 'Yahoo Finance',
                        'published': int(datetime.now().timestamp()) - (i * 3600),
                        'sentiment': sentiment_result['sentiment'],
                        'confidence': sentiment_result['confidence']
                    })
        except Exception as e:
            print(f"Error scraping Yahoo Finance: {e}")
        
        # If we don't have enough news, try to get some generic Indian market news
        if len(news_items) < 3:
            try:
                # Try to get general Indian market news
                generic_news = [
                    {
                        'title': f"{company_name} Stock Analysis - Indian Market Update",
                        'summary': f"Latest market analysis for {company_name} in the Indian stock market.",
                        'link': f"https://finance.yahoo.com/quote/{symbol}.NS",
                        'publisher': 'Market Analysis',
                        'published': int(datetime.now().timestamp()),
                        'sentiment': 'Neutral',
                        'confidence': 0.6
                    },
                    {
                        'title': f"{company_name} - NSE Trading Update",
                        'summary': f"Trading update for {company_name} on the National Stock Exchange.",
                        'link': f"https://finance.yahoo.com/quote/{symbol}.NS",
                        'publisher': 'NSE Update',
                        'published': int(datetime.now().timestamp()) - 3600,
                        'sentiment': 'Neutral',
                        'confidence': 0.6
                    },
                    {
                        'title': f"Indian Market: {company_name} Performance Review",
                        'summary': f"Performance review of {company_name} in the Indian equity market.",
                        'link': f"https://finance.yahoo.com/quote/{symbol}.NS",
                        'publisher': 'Market Review',
                        'published': int(datetime.now().timestamp()) - 7200,
                        'sentiment': 'Neutral',
                        'confidence': 0.6
                    }
                ]
                
                # Add generic news if we don't have enough specific news
                for news in generic_news[:3-len(news_items)]:
                    news_items.append(news)
                    
            except Exception as e:
                print(f"Error adding generic news: {e}")
        
        return news_items
        
    except Exception as e:
        print(f"Error with alternative news scraping: {e}")
        return []

def analyze_sentiment_ml(text):
    """Perform sentiment analysis using VADER"""
    try:
        # Clean the text but preserve important financial terms
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = ' '.join(text.split())
        
        if not text.strip():
            return {'sentiment': 'Neutral', 'confidence': 0.5}
        
        # VADER sentiment analysis
        vader_scores = vader_analyzer.polarity_scores(text)
        vader_compound = vader_scores['compound']
        vader_positive = vader_scores['pos']
        vader_negative = vader_scores['neg']
        vader_neutral = vader_scores['neu']
        
        # Enhanced sentiment analysis with financial context
        financial_positive_words = ['profit', 'growth', 'revenue', 'gain', 'rise', 'increase', 'strong', 'beat', 'exceed', 'surge', 'rally', 'bullish', 'upgrade', 'positive', 'success', 'breakthrough', 'record', 'high', 'boost', 'improve', 'expansion', 'partnership', 'deal', 'acquisition', 'investment']
        financial_negative_words = ['loss', 'decline', 'fall', 'drop', 'crash', 'plunge', 'slump', 'weak', 'poor', 'disappoint', 'miss', 'cut', 'reduce', 'layoff', 'crisis', 'concern', 'risk', 'threat', 'challenge', 'problem', 'issue', 'trouble', 'struggle', 'pressure', 'volatility', 'uncertainty', 'bearish', 'pessimistic', 'downgrade', 'warning', 'caution']
        
        # Count financial sentiment words
        pos_count = sum(1 for word in financial_positive_words if word in text)
        neg_count = sum(1 for word in financial_negative_words if word in text)
        
        # Adjust sentiment based on financial context
        financial_bias = (pos_count - neg_count) * 0.1
        
        # Combine VADER analysis with financial context
        combined_score = vader_compound + financial_bias
        
        # Determine sentiment based on combined score
        if combined_score >= 0.2:
            sentiment = 'Positive'
            confidence = min(0.95, 0.6 + abs(combined_score) * 0.4)
        elif combined_score <= -0.2:
            sentiment = 'Negative'
            confidence = min(0.95, 0.6 + abs(combined_score) * 0.4)
        else:
            sentiment = 'Neutral'
            confidence = 0.5 + (0.2 - abs(combined_score)) * 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 2)
        }
        
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {'sentiment': 'Neutral', 'confidence': 0.5}

def generate_summarized_insights(news_items, symbol, company_name):
    """Generate summarized insights from news items using extractive summarization"""
    try:
        # Combine all news content for summarization
        all_text = ""
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0, "Volatile": 0}
        
        for item in news_items:
            all_text += f"{item['title']}. {item['summary']}. "
            sentiment_counts[item['sentiment']] = sentiment_counts.get(item['sentiment'], 0) + 1
        
        # Simple extractive summarization - extract key sentences
        sentences = all_text.split('. ')
        key_sentences = []
        
        # Keywords to look for in important sentences
        important_keywords = [
            'revenue', 'growth', 'earnings', 'profit', 'loss', 'acquisition', 'merger',
            'partnership', 'expansion', 'investment', 'dividend', 'stock', 'market',
            'analyst', 'forecast', 'outlook', 'guidance', 'quarterly', 'annual',
            'breakthrough', 'innovation', 'technology', 'product', 'service'
        ]
        
        # Score sentences based on keyword presence and length
        scored_sentences = []
        for sentence in sentences:
            if len(sentence.strip()) > 20:  # Minimum length
                score = 0
                sentence_lower = sentence.lower()
                
                # Score based on important keywords
                for keyword in important_keywords:
                    if keyword in sentence_lower:
                        score += 2
                
                # Score based on company name mention
                if company_name.lower() in sentence_lower or symbol.lower() in sentence_lower:
                    score += 1
                
                # Score based on sentiment words
                positive_words = ['strong', 'growth', 'increase', 'positive', 'success', 'excellent', 'robust']
                negative_words = ['decline', 'decrease', 'negative', 'concern', 'challenge', 'issue', 'problem']
                
                for word in positive_words:
                    if word in sentence_lower:
                        score += 1
                for word in negative_words:
                    if word in sentence_lower:
                        score += 1
                
                if score > 0:
                    scored_sentences.append((sentence.strip(), score))
        
        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in scored_sentences[:3]]  # Top 3 sentences
        
        # Generate insights based on sentiment analysis
        total_news = len(news_items)
        positive_ratio = sentiment_counts["Positive"] / total_news if total_news > 0 else 0
        negative_ratio = sentiment_counts["Negative"] / total_news if total_news > 0 else 0
        
        # Create summary insights
        insights = {
            "key_points": top_sentences,
            "sentiment_summary": {
                "positive_news": sentiment_counts["Positive"],
                "negative_news": sentiment_counts["Negative"],
                "neutral_news": sentiment_counts["Neutral"],
                "volatile_news": sentiment_counts.get("Volatile", 0)
            },
            "market_outlook": generate_market_outlook(positive_ratio, negative_ratio, symbol),
            "risk_factors": generate_risk_factors(news_items, negative_ratio),
            "opportunities": generate_opportunities(news_items, positive_ratio)
        }
        
        return insights
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return {
            "key_points": ["Analysis in progress..."],
            "sentiment_summary": {"positive_news": 0, "negative_news": 0, "neutral_news": 0, "volatile_news": 0},
            "market_outlook": "Neutral outlook based on current market conditions.",
            "risk_factors": ["Market volatility", "Economic uncertainty"],
            "opportunities": ["Potential growth areas", "Market expansion"]
        }

def generate_market_outlook(positive_ratio, negative_ratio, symbol):
    """Generate market outlook based on sentiment ratios"""
    if positive_ratio > 0.6:
        return f"Bullish outlook for {symbol} with strong positive sentiment from recent news coverage."
    elif negative_ratio > 0.6:
        return f"Bearish outlook for {symbol} with significant negative sentiment in recent news."
    elif positive_ratio > negative_ratio:
        return f"Cautiously optimistic outlook for {symbol} with mixed but slightly positive sentiment."
    elif negative_ratio > positive_ratio:
        return f"Cautious outlook for {symbol} with mixed but slightly negative sentiment."
    else:
        return f"Neutral outlook for {symbol} with balanced sentiment across recent news coverage."

def generate_risk_factors(news_items, negative_ratio):
    """Generate risk factors based on news analysis"""
    risk_factors = []
    
    if negative_ratio > 0.3:
        risk_factors.append("High negative sentiment in recent news")
    
    # Look for specific risk-related keywords in news
    risk_keywords = ['regulatory', 'competition', 'challenge', 'concern', 'issue', 'problem', 'decline']
    for item in news_items:
        for keyword in risk_keywords:
            if keyword.lower() in item['title'].lower() or keyword.lower() in item['summary'].lower():
                if f"Regulatory concerns" not in risk_factors and 'regulatory' in keyword:
                    risk_factors.append("Regulatory concerns")
                elif f"Competitive pressure" not in risk_factors and 'competition' in keyword:
                    risk_factors.append("Competitive pressure")
                elif f"Market challenges" not in risk_factors and 'challenge' in keyword:
                    risk_factors.append("Market challenges")
    
    if not risk_factors:
        risk_factors = ["Market volatility", "Economic uncertainty"]
    
    return risk_factors[:3]  # Limit to 3 risk factors

def generate_opportunities(news_items, positive_ratio):
    """Generate opportunities based on news analysis"""
    opportunities = []
    
    if positive_ratio > 0.3:
        opportunities.append("Strong positive momentum in recent news")
    
    # Look for specific opportunity-related keywords in news
    opportunity_keywords = ['growth', 'expansion', 'partnership', 'innovation', 'breakthrough', 'acquisition']
    for item in news_items:
        for keyword in opportunity_keywords:
            if keyword.lower() in item['title'].lower() or keyword.lower() in item['summary'].lower():
                if f"Growth opportunities" not in opportunities and 'growth' in keyword:
                    opportunities.append("Growth opportunities")
                elif f"Strategic partnerships" not in opportunities and 'partnership' in keyword:
                    opportunities.append("Strategic partnerships")
                elif f"Market expansion" not in opportunities and 'expansion' in keyword:
                    opportunities.append("Market expansion")
    
    if not opportunities:
        opportunities = ["Market recovery potential", "Innovation opportunities"]
    
    return opportunities[:3]  # Limit to 3 opportunities

def generate_stock_sentiment_data(symbol, chart_data):
    """Generate realistic sentiment data based on stock symbol and price movement"""
    
    # Simplified sentiment profiles
    sentiment_profiles = {
        'AAPL': {'base_sentiment': 0.3, 'volatility': 0.4},
        'MSFT': {'base_sentiment': 0.4, 'volatility': 0.3},
        'GOOGL': {'base_sentiment': 0.2, 'volatility': 0.5},
        'AMZN': {'base_sentiment': 0.1, 'volatility': 0.6},
        'TSLA': {'base_sentiment': -0.1, 'volatility': 0.8},
        'META': {'base_sentiment': 0.0, 'volatility': 0.7},
        'NVDA': {'base_sentiment': 0.5, 'volatility': 0.4},
        'JPM': {'base_sentiment': 0.2, 'volatility': 0.3},
        'V': {'base_sentiment': 0.3, 'volatility': 0.2},
        'JNJ': {'base_sentiment': 0.1, 'volatility': 0.2}
    }
    
    profile = sentiment_profiles.get(symbol, {'base_sentiment': 0.0, 'volatility': 0.4})
    sentiment_data = []
    
    for i, price_point in enumerate(chart_data):
        base_sentiment = profile['base_sentiment']
        volatility = profile['volatility']
        random_factor = random.uniform(-volatility, volatility)
        
        # Add price movement correlation
        if i > 0:
            price_change = (price_point['price'] - chart_data[i-1]['price']) / chart_data[i-1]['price']
            price_sentiment_correlation = price_change * 0.5
        else:
            price_sentiment_correlation = 0
        
        final_sentiment = base_sentiment + random_factor + price_sentiment_correlation
        final_sentiment = max(-1.0, min(1.0, final_sentiment))
        
        sentiment_data.append({
            'date': price_point['date'],
            'sentiment': round(final_sentiment, 2)
        })
    
    return sentiment_data

def get_stock_news_items(symbol, company_name):
    """Get real news items for a stock using Yahoo Finance API"""
    return get_real_news_from_yahoo(symbol, company_name)

def extract_keywords_from_news(news_items):
    """Extract keywords from real news content for word cloud"""
    try:
        # Combine all news content
        all_text = ""
        for item in news_items:
            all_text += " " + item.get('title', '') + " " + item.get('summary', '')
        
        # Clean and tokenize text
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            if word not in ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'man', 'oil', 'sit', 'try', 'use', 'she', 'put', 'end', 'why', 'let', 'say', 'ask', 'run', 'own', 'set', 'too', 'any', 'may', 'say', 'she', 'use', 'her', 'many', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'much', 'over', 'such', 'take', 'than', 'them', 'well', 'were']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and take top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Create keyword objects with sentiment
        keywords = []
        sentiment_keywords = {
            'positive': ['growth', 'profit', 'revenue', 'success', 'strong', 'increase', 'gain', 'rise', 'boost', 'improve', 'excellent', 'outstanding', 'record', 'breakthrough', 'innovation', 'expansion', 'partnership', 'deal', 'acquisition', 'investment', 'upgrade', 'beat', 'exceed', 'surge', 'rally', 'bullish', 'optimistic', 'confidence', 'momentum', 'leadership', 'dominance'],
            'negative': ['loss', 'decline', 'fall', 'drop', 'crash', 'plunge', 'slump', 'weak', 'poor', 'disappoint', 'miss', 'cut', 'reduce', 'layoff', 'crisis', 'concern', 'risk', 'threat', 'challenge', 'problem', 'issue', 'trouble', 'struggle', 'pressure', 'volatility', 'uncertainty', 'bearish', 'pessimistic', 'downgrade', 'warning', 'caution'],
            'neutral': ['market', 'company', 'stock', 'share', 'price', 'earnings', 'quarter', 'year', 'report', 'analyst', 'forecast', 'expectation', 'guidance', 'outlook', 'trend', 'sector', 'industry', 'business', 'financial', 'result', 'performance', 'data', 'news', 'update', 'announcement', 'statement', 'conference', 'call', 'meeting', 'agreement']
        }
        
        for word, freq in sorted_words[:15]:  # Top 15 keywords
            sentiment = 'neutral'
            for sent_type, words_list in sentiment_keywords.items():
                if word in words_list:
                    sentiment = sent_type
                    break
            
            keywords.append({
                'text': word,
                'weight': min(20, freq * 2),  # Scale weight
                'sentiment': sentiment
            })
        
        return keywords
        
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        # Return default keywords if extraction fails
        return [
            {'text': 'market', 'weight': 15, 'sentiment': 'neutral'},
            {'text': 'growth', 'weight': 12, 'sentiment': 'positive'},
            {'text': 'revenue', 'weight': 10, 'sentiment': 'positive'},
            {'text': 'earnings', 'weight': 8, 'sentiment': 'neutral'},
            {'text': 'analysts', 'weight': 6, 'sentiment': 'neutral'}
        ]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'stock-sentiment-analysis'
    }), 200

@app.route('/ping')
def ping():
    return jsonify({'pong': True, 'timestamp': datetime.now().isoformat()})

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/search_stocks')
def search_stocks():
    """API endpoint for stock search"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    # Expanded stock data including Indian stocks
    stocks = [
        # US Stocks
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "JNJ", "name": "Johnson & Johnson"},
        {"symbol": "NFLX", "name": "Netflix Inc."},
        {"symbol": "UBER", "name": "Uber Technologies Inc."},
        {"symbol": "SHOP", "name": "Shopify Inc."},
        {"symbol": "ZM", "name": "Zoom Video Communications Inc."},
        {"symbol": "PLTR", "name": "Palantir Technologies Inc."},
        {"symbol": "MA", "name": "Mastercard Inc."},
        {"symbol": "PYPL", "name": "PayPal Holdings Inc."},
        {"symbol": "WMT", "name": "Walmart Inc."},
        {"symbol": "DIS", "name": "Walt Disney Company"},
        {"symbol": "NKE", "name": "Nike Inc."},
        {"symbol": "XOM", "name": "Exxon Mobil Corporation"},
        {"symbol": "BA", "name": "Boeing Company"},
        {"symbol": "CAT", "name": "Caterpillar Inc."},
        
        # Indian Stocks
        {"symbol": "TCS", "name": "Tata Consultancy Services Ltd."},
        {"symbol": "INFY", "name": "Infosys Ltd."},
        {"symbol": "WIPRO", "name": "Wipro Ltd."},
        {"symbol": "HCLTECH", "name": "HCL Technologies Ltd."},
        {"symbol": "TECHM", "name": "Tech Mahindra Ltd."},
        {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd."},
        {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd."},
        {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank Ltd."},
        {"symbol": "AXISBANK", "name": "Axis Bank Ltd."},
        {"symbol": "SBIN", "name": "State Bank of India"},
        {"symbol": "RELIANCE", "name": "Reliance Industries Ltd."},
        {"symbol": "HINDUNILVR", "name": "Hindustan Unilever Ltd."},
        {"symbol": "ITC", "name": "ITC Ltd."},
        {"symbol": "BHARTIARTL", "name": "Bharti Airtel Ltd."},
        {"symbol": "MARUTI", "name": "Maruti Suzuki India Ltd."},
        {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical Industries Ltd."},
        {"symbol": "DRREDDY", "name": "Dr. Reddy's Laboratories Ltd."},
        {"symbol": "CIPLA", "name": "Cipla Ltd."},
        {"symbol": "DIVISLAB", "name": "Divi's Laboratories Ltd."},
        {"symbol": "BIOCON", "name": "Biocon Ltd."},
        {"symbol": "ONGC", "name": "Oil and Natural Gas Corporation Ltd."},
        {"symbol": "IOC", "name": "Indian Oil Corporation Ltd."},
        {"symbol": "BPCL", "name": "Bharat Petroleum Corporation Ltd."},
        {"symbol": "ADANIGREEN", "name": "Adani Green Energy Ltd."},
        {"symbol": "TATAPOWER", "name": "Tata Power Company Ltd."},
        {"symbol": "ZOMATO", "name": "Zomato Ltd."},
        {"symbol": "PAYTM", "name": "One97 Communications Ltd."},
        {"symbol": "POLICYBZR", "name": "PB Fintech Ltd."},
        {"symbol": "NAZARA", "name": "Nazara Technologies Ltd."}
    ]
    
    results = []
    for stock in stocks:
        if (query in stock['symbol'].lower() or 
            query in stock['name'].lower()):
            results.append({
                'symbol': stock['symbol'],
                'name': stock['name'],
                'display': f"{stock['symbol']} - {stock['name']}"
            })
    
    return jsonify(results[:20])

@app.route('/api/get_default_markets')
def get_default_markets():
    """API endpoint to get default market data (Dow Jones, S&P 500 for US; Sensex, Nifty for India)"""
    try:
        # Get market location from query parameter (default to US)
        market_location = request.args.get('location', 'US')
        
        if market_location == 'IN':
            # Indian markets
            markets = [
                {'symbol': '^NSEI', 'name': 'Nifty 50', 'display_name': 'Nifty 50'},
                {'symbol': '^BSESN', 'name': 'S&P BSE Sensex', 'display_name': 'Sensex'}
            ]
        else:
            # US markets
            markets = [
                {'symbol': '^DJI', 'name': 'Dow Jones Industrial Average', 'display_name': 'Dow Jones'},
                {'symbol': '^GSPC', 'name': 'S&P 500', 'display_name': 'S&P 500'}
            ]
        
        market_data = []
        for market in markets:
            try:
                # Get real stock data for the market index
                stock_data = get_real_stock_data(market['symbol'])
                
                market_info = {
                    'symbol': market['symbol'],
                    'name': market['name'],
                    'display_name': market['display_name'],
                    'current_price': stock_data['current_price'],
                    'price_change': stock_data['price_change'],
                    'price_change_percent': stock_data['price_change_percent'],
                    'chart_data': stock_data['chart_data'][-7:],  # Last 7 days for default display
                    'currency': '₹' if market_location == 'IN' else '$',
                    'is_indian_market': market_location == 'IN'
                }
                market_data.append(market_info)
            except Exception as e:
                print(f"Error fetching data for {market['symbol']}: {e}")
                # Add fallback data
                market_info = {
                    'symbol': market['symbol'],
                    'name': market['name'],
                    'display_name': market['display_name'],
                    'current_price': 0,
                    'price_change': 0,
                    'price_change_percent': 0,
                    'chart_data': [],
                    'currency': '₹' if market_location == 'IN' else '$',
                    'is_indian_market': market_location == 'IN'
                }
                market_data.append(market_info)
        
        return jsonify({
            'markets': market_data,
            'location': market_location,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_sentiment', methods=['POST'])
def analyze_sentiment_endpoint():
    """API endpoint for sentiment analysis with real news and ML analysis"""
    data = request.get_json()
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    try:
        # Expanded company names including Indian stocks
        company_names = {
            # US Stocks
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation', 
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'META': 'Meta Platforms Inc.',
            'NVDA': 'NVIDIA Corporation',
            'JPM': 'JPMorgan Chase & Co.',
            'V': 'Visa Inc.',
            'JNJ': 'Johnson & Johnson',
            'NFLX': 'Netflix Inc.',
            'UBER': 'Uber Technologies Inc.',
            'SHOP': 'Shopify Inc.',
            'ZM': 'Zoom Video Communications Inc.',
            'PLTR': 'Palantir Technologies Inc.',
            'MA': 'Mastercard Inc.',
            'PYPL': 'PayPal Holdings Inc.',
            'WMT': 'Walmart Inc.',
            'DIS': 'Walt Disney Company',
            'NKE': 'Nike Inc.',
            'XOM': 'Exxon Mobil Corporation',
            'BA': 'Boeing Company',
            'CAT': 'Caterpillar Inc.',
            
            # Indian Stocks
            'TCS': 'Tata Consultancy Services Ltd.',
            'INFY': 'Infosys Ltd.',
            'WIPRO': 'Wipro Ltd.',
            'HCLTECH': 'HCL Technologies Ltd.',
            'TECHM': 'Tech Mahindra Ltd.',
            'HDFCBANK': 'HDFC Bank Ltd.',
            'ICICIBANK': 'ICICI Bank Ltd.',
            'KOTAKBANK': 'Kotak Mahindra Bank Ltd.',
            'AXISBANK': 'Axis Bank Ltd.',
            'SBIN': 'State Bank of India',
            'RELIANCE': 'Reliance Industries Ltd.',
            'HINDUNILVR': 'Hindustan Unilever Ltd.',
            'ITC': 'ITC Ltd.',
            'BHARTIARTL': 'Bharti Airtel Ltd.',
            'MARUTI': 'Maruti Suzuki India Ltd.',
            'SUNPHARMA': 'Sun Pharmaceutical Industries Ltd.',
            'DRREDDY': 'Dr. Reddy\'s Laboratories Ltd.',
            'CIPLA': 'Cipla Ltd.',
            'DIVISLAB': 'Divi\'s Laboratories Ltd.',
            'BIOCON': 'Biocon Ltd.',
            'ONGC': 'Oil and Natural Gas Corporation Ltd.',
            'IOC': 'Indian Oil Corporation Ltd.',
            'BPCL': 'Bharat Petroleum Corporation Ltd.',
            'ADANIGREEN': 'Adani Green Energy Ltd.',
            'TATAPOWER': 'Tata Power Company Ltd.',
            'ZOMATO': 'Zomato Ltd.',
            'PAYTM': 'One97 Communications Ltd.',
            'POLICYBZR': 'PB Fintech Ltd.',
            'NAZARA': 'Nazara Technologies Ltd.'
        }
        
        company_name = company_names.get(symbol, f"{symbol} Corporation")
        
        # Get real news items using ML sentiment analysis
        news_items = get_stock_news_items(symbol, company_name)
        
        # Calculate overall sentiment based on real ML analysis
        if not news_items:
            overall_sentiment = 'Neutral'
            confidence = 0.5
        else:
            # Calculate weighted sentiment based on ML confidence scores
            total_weighted_score = 0
            total_weight = 0
            
            for item in news_items:
                sentiment = item['sentiment']
                item_confidence = item['confidence']
                
                # Convert sentiment to numeric score
                if sentiment == 'Positive':
                    score = 1
                elif sentiment == 'Negative':
                    score = -1
                else:  # Neutral
                    score = 0
                
                # Weight by confidence
                total_weighted_score += score * item_confidence
                total_weight += item_confidence
            
            if total_weight > 0:
                avg_weighted_score = total_weighted_score / total_weight
                avg_confidence = total_weight / len(news_items)
                
                # Determine overall sentiment based on weighted score
                if avg_weighted_score >= 0.3:
                    overall_sentiment = 'Positive'
                    confidence = min(0.95, avg_confidence + 0.1)
                elif avg_weighted_score <= -0.3:
                    overall_sentiment = 'Negative'
                    confidence = min(0.95, avg_confidence + 0.1)
                else:
                    overall_sentiment = 'Neutral'
                    confidence = avg_confidence
            else:
                overall_sentiment = 'Neutral'
                confidence = 0.5
        
        # Get real stock data with Indian stock support
        stock_data = get_real_stock_data(symbol)
        chart_data = stock_data["chart_data"]
        current_price = stock_data["current_price"]
        price_change = stock_data["price_change"]
        price_change_percent = stock_data["price_change_percent"]
        data_timestamp = stock_data.get("data_timestamp", datetime.now().isoformat())
        data_source = stock_data.get("data_source", "Yahoo Finance (Real-time)")
        
        # Determine currency and Indian stock status
        indian_stocks = [
            'TCS', 'INFY', 'WIPRO', 'HCLTECH', 'TECHM', 'HDFCBANK', 'ICICIBANK', 'KOTAKBANK', 
            'AXISBANK', 'SBIN', 'RELIANCE', 'HINDUNILVR', 'ITC', 'BHARTIARTL', 'MARUTI', 
            'SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB', 'BIOCON', 'ONGC', 'IOC', 'BPCL', 
            'ADANIGREEN', 'TATAPOWER', 'ZOMATO', 'PAYTM', 'POLICYBZR', 'NAZARA'
        ]
        
        currency = "₹" if symbol in indian_stocks else "$"
        is_indian_stock = symbol in indian_stocks
        
        # Generate realistic sentiment data based on stock symbol
        sentiment_data = generate_stock_sentiment_data(symbol, chart_data)
        
        # Generate summarized insights from real news items
        insights = generate_summarized_insights(news_items, symbol, company_name)
        
        # Generate keyword cloud data from real news content
        keywords = extract_keywords_from_news(news_items)
        
        return jsonify({
            'symbol': symbol,
            'company_name': company_name,
            'news_count': len(news_items),
            'overall_sentiment': overall_sentiment,
            'confidence': round(confidence, 2),
            'news_items': news_items,
            'chart_data': chart_data,
            'sentiment_data': sentiment_data,
            'keywords': keywords,
            'current_price': current_price,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
            'currency': currency,
            'is_indian_stock': is_indian_stock,
            'insights': insights,
            'data_timestamp': data_timestamp,
            'data_source': data_source
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable, default to 8080 (GCP standard)
    port = int(os.environ.get('PORT', 8080))
    
    print("Starting Stock Sentiment Analysis App")
    print(f"Running on port: {port}")
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)