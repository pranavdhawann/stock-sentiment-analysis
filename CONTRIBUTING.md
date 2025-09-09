# 🤝 Contributing to InfoEdge

Thank you for your interest in contributing to InfoEdge! We welcome contributions from the community and appreciate your help in making this project better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Please report unacceptable behavior to [your-email@example.com].

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package installer)
- Basic knowledge of Flask, HTML, CSS, and JavaScript

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/pranavdhawann/stock-sentiment-analysis.git
   ```

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8 mypy
```

### 3. Run the Application

```bash
# Start the development server
python app.py

# The application will be available at http://localhost:8080
```

## 🎯 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- 🐛 **Bug Fixes**: Fix existing issues
- ✨ **New Features**: Add new functionality
- 📚 **Documentation**: Improve documentation
- 🎨 **UI/UX Improvements**: Enhance user interface
- ⚡ **Performance**: Optimize code performance
- 🧪 **Tests**: Add or improve test coverage
- 🔧 **DevOps**: Improve deployment and CI/CD

### Contribution Workflow

1. **Check existing issues** and pull requests
2. **Create an issue** if you're planning a significant change
3. **Fork and clone** the repository
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```
5. **Make your changes** following our coding standards
6. **Test your changes** thoroughly
7. **Commit your changes** with clear commit messages
8. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Create a Pull Request**

## 📝 Pull Request Process

### Before Submitting

- [ ] Code follows the project's coding standards
- [ ] Self-review of your code has been performed
- [ ] Code has been commented, particularly in hard-to-understand areas
- [ ] Tests have been added/updated (if applicable)
- [ ] Documentation has been updated (if applicable)
- [ ] No new warnings or errors are introduced

### Pull Request Template

When creating a pull request, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Manual testing completed
- [ ] No regression issues

## Screenshots (if applicable)
Add screenshots to help explain your changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have made corresponding changes to documentation
```

## 🐛 Issue Guidelines

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check if it's already fixed** in the latest version
3. **Gather information** about your environment

### Issue Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.8.10]
- Browser: [e.g., Chrome 91, Firefox 89]

**Additional context**
Any other context about the problem.
```

## 📏 Coding Standards

### Python Code Style

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

### Example Code Style

```python
def analyze_sentiment(text: str, model: str = "default") -> dict:
    """
    Analyze sentiment of the given text.
    
    Args:
        text (str): The text to analyze
        model (str): The sentiment analysis model to use
        
    Returns:
        dict: Sentiment analysis results with confidence score
        
    Raises:
        ValueError: If text is empty or invalid
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Implementation here
    return {
        "sentiment": "positive",
        "confidence": 0.85,
        "model_used": model
    }
```

### Frontend Code Style

- Use **semantic HTML**
- Follow **BEM methodology** for CSS
- Use **ES6+** JavaScript features
- Keep **CSS organized** and modular
- Use **responsive design** principles

### Commit Message Format

Use clear, descriptive commit messages:

```
feat: add real-time sentiment analysis
fix: resolve chart rendering issue on mobile
docs: update API documentation
style: format code according to PEP 8
refactor: improve error handling in sentiment analysis
test: add unit tests for news aggregation
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_sentiment.py
```

### Writing Tests

- Write **unit tests** for new functions
- Write **integration tests** for API endpoints
- Aim for **80%+ code coverage**
- Test **edge cases** and error conditions

### Example Test

```python
import pytest
from app import analyze_sentiment

def test_analyze_sentiment_positive():
    """Test sentiment analysis with positive text."""
    result = analyze_sentiment("This is great news!")
    assert result["sentiment"] == "positive"
    assert result["confidence"] > 0.5

def test_analyze_sentiment_empty_text():
    """Test sentiment analysis with empty text."""
    with pytest.raises(ValueError):
        analyze_sentiment("")
```

## 📚 Documentation

### Code Documentation

- Write **docstrings** for all functions and classes
- Include **type hints** for better code understanding
- Add **inline comments** for complex logic
- Update **README.md** for new features

### API Documentation

- Document **new API endpoints**
- Include **request/response examples**
- Add **error code documentation**
- Update **API changelog**

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Release notes prepared

## 🆘 Getting Help

### Resources

- 📖 **Documentation**: Check the README.md and inline docs
- 🐛 **Issues**: Search existing issues or create new ones
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Email**: Contact maintainers directly

### Community

- Join our **GitHub Discussions** for community support
- Follow **@pranavdhawann** on social media for updates
- Star the repository to show your support

## 🎉 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

## 📄 License

By contributing to InfoEdge, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing to InfoEdge! 🚀**

*Your contributions help make financial sentiment analysis more accessible to everyone.*
