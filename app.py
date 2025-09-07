from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Stock Sentiment Analysis API is running',
        'timestamp': datetime.now().isoformat(),
        'port': os.environ.get('PORT', 'not set')
    })

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
    
    # Sample stock data
    stocks = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "JNJ", "name": "Johnson & Johnson"}
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

@app.route('/api/analyze_sentiment', methods=['POST'])
def analyze_sentiment_endpoint():
    """API endpoint for sentiment analysis"""
    data = request.get_json()
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    try:
        # Sample news data
        company_names = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation', 
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'META': 'Meta Platforms Inc.',
            'NVDA': 'NVIDIA Corporation',
            'JPM': 'JPMorgan Chase & Co.',
            'V': 'Visa Inc.',
            'JNJ': 'Johnson & Johnson'
        }
        
        company_name = company_names.get(symbol, f"{symbol} Corporation")
        
        # Generate sample news with positive sentiment
        news_items = [
            {
                'title': f"{company_name} Shows Strong Performance in Latest Quarter",
                'summary': f"{company_name} has demonstrated excellent growth with positive market sentiment. Investors are optimistic about future prospects.",
                'link': f"https://finance.yahoo.com/quote/{symbol}",
                'publisher': 'Market News',
                'published': int(datetime.now().timestamp()),
                'sentiment': 'Positive',
                'confidence': 0.8
            },
            {
                'title': f"{company_name} Strategic Initiatives Drive Market Confidence",
                'summary': f"Recent strategic moves by {company_name} have generated positive investor sentiment and strong market performance.",
                'link': f"https://finance.yahoo.com/quote/{symbol}",
                'publisher': 'Financial Review',
                'published': int(datetime.now().timestamp()) - 3600,
                'sentiment': 'Positive',
                'confidence': 0.7
            },
            {
                'title': f"{company_name} Market Analysis Shows Bullish Trends",
                'summary': f"Technical analysis indicates strong upward momentum for {company_name} with positive outlook from analysts.",
                'link': f"https://finance.yahoo.com/quote/{symbol}",
                'publisher': 'Technical Analysis',
                'published': int(datetime.now().timestamp()) - 7200,
                'sentiment': 'Positive',
                'confidence': 0.75
            }
        ]
        
        return jsonify({
            'symbol': symbol,
            'news_count': len(news_items),
            'overall_sentiment': 'Positive',
            'confidence': 0.75,
            'news_items': news_items
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