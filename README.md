# 📈 Stock Sentiment Analysis

A real-time stock sentiment analysis application that analyzes news articles and provides sentiment insights for smarter trading decisions.

## 🌟 Features

- **Real-time Sentiment Analysis**: Analyze news sentiment for any stock symbol
- **Multi-Market Support**: US and Indian stock markets
- **Interactive Charts**: Visualize stock price movements and sentiment trends
- **News Integration**: Latest news articles with sentiment scoring
- **Dark/Light Theme**: Toggle between themes for better user experience
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Market Overview**: Real-time market data for major indices

## 🚀 Live Demo

**🌐 [Try the Live Application](https://stock-sentiment-app-egc2jnomta-uc.a.run.app)**

## 📱 Screenshots

### Desktop View
- Clean, modern interface with sidebar navigation
- Interactive sentiment meter and charts
- Real-time market data display

### Mobile View
- Responsive design with hamburger menu
- Touch-friendly interface
- Optimized for mobile trading

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5, Custom CSS
- **Charts**: Chart.js
- **Sentiment Analysis**: VADER Sentiment
- **News Scraping**: BeautifulSoup4, Requests
- **Deployment**: Google Cloud Run
- **Containerization**: Docker

## 📊 How It Works

1. **Stock Search**: Enter a stock symbol (e.g., AAPL, TSLA, TCS)
2. **News Fetching**: System fetches latest news articles from multiple sources
3. **Sentiment Analysis**: VADER sentiment analyzer processes news content
4. **Visualization**: Results displayed with interactive charts and sentiment meters
5. **Insights**: AI-generated insights and market outlook

## 🎯 Supported Markets

### US Stocks
- Apple (AAPL), Microsoft (MSFT), Google (GOOGL)
- Tesla (TSLA), Amazon (AMZN), Meta (META)
- And many more...

### Indian Stocks
- TCS, Infosys, Wipro, HCL Technologies
- Reliance, HDFC Bank, ICICI Bank
- And many more...

## 🎨 Customization

### Themes
The application supports both light and dark themes. Users can toggle between themes using the theme button in the sidebar.

### Adding New Stocks
To add support for new stocks, update the stock lists in `app.py`:
- `indian_stocks` list for Indian market stocks
- Stock search functionality in the frontend

## 📈 Performance

- **Response Time**: < 2 seconds for sentiment analysis
- **Scalability**: Auto-scaling with Google Cloud Run
- **Availability**: 99.9% uptime with global CDN
- **Mobile Optimized**: Responsive design for all devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---

⭐ **Star this repository if you found it helpful!**
