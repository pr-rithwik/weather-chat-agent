# 🌤️ Weather Chat Agent

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.39+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

A Python-based AI agent that uses Claude (Anthropic) to provide conversational weather information. Built with Streamlit for a clean, minimal frontend that showcases Python backend skills.

[**🚀 Live Demo**](https://weather94.streamlit.app) | [**📖 Documentation**](ROADMAP.md)

---

## 🎯 Project Overview

This project demonstrates professional Python development practices through a working AI agent that provides conversational weather information.

**Key Highlights:**
- ✅ **290 lines of Python** - Clean, maintainable code
- ✅ **API Integration** - Claude API + OpenWeatherMap API
- ✅ **Function Calling** - Claude decides when to use tools
- ✅ **Production-Ready** - Error handling, validation, cost tracking
- ✅ **Unit Tested** - pytest with mocking

---

## ✨ Features

### Core Functionality
- 🤖 **AI-Powered Chat**: Conversational interface using Claude Sonnet 4
- 🌍 **Real-Time Weather**: Current weather data from OpenWeatherMap
- 🎯 **Smart Tool Calling**: Claude automatically decides when to fetch weather

### Professional Features
- 💰 **Cost Tracking**: Real-time API usage and cost monitoring
- ✅ **Input Validation**: Prevents invalid city names and API errors
- 🛡️ **Error Handling**: User-friendly error messages for all failure cases
- 📊 **Session Stats**: Track messages, tokens, and costs per session
- 🧪 **Unit Tested**: Comprehensive test coverage with pytest

---

## 🏗️ Architecture

```
User Input → Streamlit UI → Agent Logic → Claude API
                ↓                           ↓
          City → Coords              Tool Execution
                                            ↓
                                   OpenWeatherMap API
```

**Execution Flow:**
1. User enters city name → Converts to coordinates
2. User asks question → Sent to Claude with tool definitions
3. Claude decides to call weather tool → Fetches data
4. Claude generates natural response → User sees answer

---

## 📁 Project Structure

```
weather-chat-agent/
├── app.py              # Streamlit UI 
├── agent.py            # Core agent logic 
├── tools.py            # API integrations 
├── config.py           # Settings
├── utils.py            # Cost tracking
├── tests/              # Unit tests
│   └── test_tools.py   # Tool tests
├── requirements.txt
├── .env.example
├── README.md
├── ROADMAP.md
└── NEXT_STEPS.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- [Anthropic API key](https://console.anthropic.com/)
- [OpenWeatherMap API key](https://openweathermap.org/api) (free tier)

### Installation

```bash
# Clone repository
git clone https://github.com/pr-rithwik/weather-chat-agent.git
cd weather-chat-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your API keys

# Run app
streamlit run app.py
```

### Run Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add secrets:
   ```toml
   ANTHROPIC_API_KEY = "your-key"
   OPENWEATHER_API_KEY = "your-key"
   ```
5. Deploy!

---

## 💰 Cost Estimate

- **Streamlit Cloud**: Free
- **OpenWeatherMap**: Free (1,000 calls/day)
- **Claude API**: ~$0.01-0.03 per conversation

**Monthly estimate for testing: $1-3**

Cost tracking built into the app sidebar!

---

## 🔧 Technical Details

### Stack
- **Frontend**: Streamlit
- **AI Model**: Claude Sonnet 4
- **Weather API**: OpenWeatherMap
- **Testing**: pytest with mocking
- **Deployment**: Streamlit Cloud

### Code Philosophy
- ✅ Functional over OOP (simpler, cleaner)
- ✅ Type hints throughout
- ✅ Minimal dependencies
- ✅ Single responsibility principle
- ✅ Error handling first

---

## 📝 Usage Examples

```
User: "What's the weather like today?"
Agent: "It's currently 22°C with clear skies in your area..."

User: "Should I bring an umbrella?"
Agent: "No need! It's sunny with no rain expected."

User: "Is it windy?"
Agent: "Light winds at 3.5 m/s - quite calm!"
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Coverage:**
- City name validation
- Weather data fetching
- API error handling
- Timeout scenarios

---

## 📈 Future Enhancements

**Next up:**
- 5-day weather forecast
- Data caching
- CI/CD pipeline
- Performance metrics

---

## 🛡️ Security

- ✅ API keys in `.env` (gitignored)
- ✅ Streamlit secrets for deployment
- ✅ Input validation
- ✅ No sensitive data in code

---

## 👤 Author

**Rithwik** - Portfolio project demonstrating Python backend development, API integration, and clean code principles.

---

## 📄 License

MIT License - Free to use for your portfolio!

---

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) - Claude API
- [OpenWeatherMap](https://openweathermap.org/) - Weather data
- [Streamlit](https://streamlit.io/) - UI framework

---

**⭐ Star this repo if you find it helpful!**