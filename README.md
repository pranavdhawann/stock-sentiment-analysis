# Stock Sentiment Analyzer

A real-time stock news sentiment analysis application built with Flask and AI-powered sentiment analysis models.

## 🚀 Features

- **Real-time Sentiment Analysis**: Analyze sentiment of stock news using VADER and keyword-based analysis
- **Smart Search**: Search by ticker symbol or company name with autocomplete
- **Visual Sentiment Meter**: Interactive meter showing sentiment scores with animated needle
- **Quick Stocks**: Quick access to popular stocks (AAPL, MSFT, GOOGL, etc.)
- **Responsive Design**: Beautiful, mobile-friendly interface

## ⚠️ Limitations & Considerations

### **Data Limitations**
- **Rate Limiting**: yfinance API has rate limits that may affect data fetching
- **News Coverage**: Limited to news available through yfinance API
- **Real-time Constraints**: News updates depend on external API availability

### **Analysis Limitations**
- **Sentiment Accuracy**: Sentiment analysis is based on text patterns and may not capture market nuances
- **Language Dependency**: Optimized for English language content

## 📊 Sentiment Analysis Models

- **VADER Sentiment**: Rule-based sentiment analysis optimized for social media and financial content
- **Keyword Analysis**: Fallback sentiment analysis using financial keywords
- **Full Content Analysis**: Analyzes title, summary, and full article content for maximum accuracy

## 📰 News Sources

- **Primary Source**: yfinance API (Yahoo Finance data provider)
- **Coverage**: Major stock exchanges and financial markets
- **Update Frequency**: Real-time updates with rate limiting protection
- **Data Quality**: Comprehensive analysis of news headlines and full content

## 🎯 Demo

Try the live application: [Demo Link](https://your-demo-link.com)

## 📱 Usage

1. **Search for a stock**: Enter a ticker symbol (e.g., AAPL) or company name
2. **Click "Analyze Sentiment"**: The application will fetch news and analyze sentiment
3. **View results**: See overall sentiment, confidence score, and sentiment meter
4. **Browse news**: Review individual news articles with sentiment analysis
5. **Reset**: Use the reset button to start fresh

## ⚠️ Disclaimer

This tool is for informational purposes only and should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions. Past performance and sentiment analysis do not guarantee future results.

**Risk Warning**: Stock market investments carry inherent risks. The sentiment analysis provided by this tool is based on news content and should not be the sole basis for investment decisions.

---

⭐ If you found this project helpful, please give it a star!
