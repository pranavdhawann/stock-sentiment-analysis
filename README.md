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

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:8080
   ```

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t stock-sentiment-app .

# Run the container
docker run -p 8080:8080 stock-sentiment-app
```

## ☁️ Google Cloud Deployment

### Prerequisites
- Google Cloud SDK installed
- Docker installed
- Google Cloud account with billing enabled

### Deploy to Cloud Run

```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# Deploy to Cloud Run
gcloud run deploy stock-sentiment-app --source . --platform managed --region us-central1 --allow-unauthenticated
```

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

## 🔧 API Endpoints

- `GET /` - Main application interface
- `GET /about` - About page
- `GET /health` - Health check endpoint
- `POST /api/analyze_sentiment` - Analyze stock sentiment
- `GET /api/search_stocks` - Search for stocks
- `GET /api/get_default_markets` - Get market data

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

## 👨‍💻 Author

**Pranav Dhawan**
- GitHub: [@pranavdhawann](https://github.com/pranavdhawann)
- LinkedIn: [Pranav Dhawan](https://linkedin.com/in/pranavdhawan)

## 🙏 Acknowledgments

- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) for sentiment analysis
- [Chart.js](https://www.chartjs.org/) for interactive charts
- [Bootstrap](https://getbootstrap.com/) for responsive design
- [Font Awesome](https://fontawesome.com/) for icons
- [Google Cloud](https://cloud.google.com/) for hosting

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact the author via LinkedIn
- Check the documentation

---

⭐ **Star this repository if you found it helpful!**