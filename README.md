# 🌤️ Weather Chat Agent

A Python-based AI agent that uses Claude (Anthropic) to provide conversational weather information. Built with Streamlit for a clean, minimal frontend that showcases Python backend skills.

## 🎯 Project Overview

This project demonstrates:
- **API Integration**: Claude API with function calling + OpenWeatherMap API
- **Agent Orchestration**: Tool calling workflow and response handling
- **Clean Code**: Functional approach with type hints and minimal LOC 
- **Production-Ready**: Error handling, environment management, deployment-ready

## 🏗️ Architecture

```
User Input → Streamlit UI → Agent Logic → Claude API
                                    ↓
                              Tool Execution
                                    ↓
                           OpenWeatherMap API
```

### Execution Flow

1. **User provides location** (city name or IP-based auto-detection)
2. **User asks weather question** (e.g., "What's the weather like today?")
3. **Agent sends to Claude** with tool definitions and location context
4. **Claude decides** if it needs to call the weather tool
5. **Tool executes** if needed, fetching data from OpenWeatherMap
6. **Claude generates** natural language response with weather data
7. **User sees** conversational response in chat interface

## 📁 Project Structure

```
weather-chat-agent/
├── app.py              # Streamlit UI 
├── agent.py            # Core agent logic 
├── tools.py            # API integrations 
├── config.py           # Settings
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # Documentation
```


## 🚀 Setup

### Prerequisites
- Python 3.9+
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd weather-chat-agent
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

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🌐 Deployment

### Streamlit Community Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in dashboard:
   - `ANTHROPIC_API_KEY`
   - `OPENWEATHER_API_KEY`
5. Deploy!

Your app will be live at: `https://your-username-weather-agent.streamlit.app`

## 💰 Cost Estimate

- **Streamlit Cloud**: Free tier (sufficient for personal use)
- **OpenWeatherMap**: Free tier (1,000 calls/day)
- **Claude API**: Pay-as-you-go
  - ~$0.01-0.03 per conversation
  - **Estimated**: $1-3/month for personal testing

**Total: ~$1-3/month**

## 🔧 Technical Details

### Tools & Libraries
- **Streamlit**: Web interface
- **Anthropic SDK**: Claude API integration
- **Requests**: HTTP calls to weather API
- **python-dotenv**: Environment management

### API Models
- **Claude**: `claude-sonnet-4-20250514`
- **Weather**: OpenWeatherMap Current Weather API

### Function Calling
The agent uses Claude's tool calling feature:
```python
WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Get current weather information",
    "input_schema": {...}
}
```

## 📝 Usage Examples

**Example 1: Direct weather query**
```
User: "What's the weather like today?"
Agent: "It's currently 22°C with clear skies in your area..."
```

**Example 2: Conversational**
```
User: "Should I bring an umbrella?"
Agent: [Checks weather] "No need! It's sunny with no rain expected."
```

**Example 3: Future plans**
```
User: "Is it good weather for a picnic?"
Agent: [Checks weather] "Perfect! It's 25°C and sunny with light winds."
```

## 🛠️ Development

### Adding New Tools

1. Define tool schema in `tools.py`
2. Implement function
3. Add to `WEATHER_TOOL` list in `agent.py`
4. Update system prompt in `config.py`

### Code Style
- **Functional approach**: No classes, pure functions
- **Type hints**: All functions annotated
- **Minimal docstrings**: Brief but clear
- **Clean code**: Single responsibility, small functions

## 🔒 Security

- API keys stored in `.env` (never committed)
- `.gitignore` configured properly
- Streamlit secrets for deployment
- No sensitive data in code

## 📈 Future Enhancements

- [ ] Add conversation history (session management)
- [ ] Support multiple locations
- [ ] Add weather forecasts (3-day, 7-day)
- [ ] Integrate additional APIs (news, stocks)
- [ ] Add unit tests
- [ ] Add cost tracking dashboard

## 📄 License

MIT License - feel free to use for your portfolio!

## 👤 Author

Built by Rithwik as a portfolio project to showcase Python development skills.

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome!