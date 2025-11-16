# 🚀 Quick Start Guide

## Installation & Running (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install streamlit requests beautifulsoup4 lxml
```

### 2️⃣ Run the Application  
```bash
python -m streamlit run app.py
```

### 3️⃣ Open Browser
```
http://localhost:8501
```

---

## First Research (30 seconds)

1. **Enter a topic** in the text box (e.g., "quantum computing")
2. **Click "Start Research"** button
3. **Watch the agents work** (3 agents in sequence)
4. **View results** in the Results tab
5. **Check metrics** in the Observability tab

---

## Example Research Topics

Try these to test the system:

- **Technology**: "artificial intelligence trends 2024"
- **Science**: "climate change solutions"
- **Business**: "electric vehicle market"
- **History**: "history of the internet"
- **Health**: "benefits of meditation"

---

## Key Tabs

| Tab | Purpose |
|-----|---------|
| 🔬 Research | Start new research |
| 📄 Results | View reports & export |
| 📊 Observability | Metrics, traces, memory |
| ℹ️ About | Documentation |

---

## Features to Explore

### ⚙️ Sidebar Settings
- Adjust max search results (3-10)
- Change summary length (Short/Medium/Detailed)
- View metrics & popular topics
- Browse research history

### 📥 Export Options
- Download as Markdown
- Download as JSON
- Export metrics & traces

### 🧠 Memory System
- Automatically remembers past research
- Shows popular topics
- Tracks access patterns

### 📊 Observability
- Real-time metrics
- Agent performance breakdown
- Execution traces
- Tool usage stats

---

## Troubleshooting

### App won't start?
```bash
# Try with full path
python -m streamlit run app.py
```

### No search results?
- Check internet connection
- App will use fallback results automatically
- Try a different topic

### Import errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Advanced Usage

### With OpenAI API (Optional)
1. Add API key in sidebar
2. Get enhanced summarization
3. Better result ranking

### Session Management
- Sessions auto-save to `sessions/` folder
- Memory persists in `memory_bank/` folder
- Logs saved to `logs/` folder
- Traces saved to `traces/` folder

---

## Architecture Overview

```
User Input
    ↓
🔍 Research Agent (DuckDuckGo + Wikipedia)
    ↓
📝 Summarizer Agent (Extract key insights)
    ↓
📊 Report Generator (Professional report)
    ↓
Results + Metrics + Traces
```

---

## System Requirements

- **Python**: 3.8 or higher
- **Internet**: Required for web search
- **RAM**: 512 MB minimum
- **Storage**: 100 MB for app + logs

---

## What Makes This Special?

✅ **Multi-Agent**: 3 specialized agents working together  
✅ **Observable**: Full logging, tracing, and metrics  
✅ **Memory**: Remembers past research  
✅ **No Setup**: Works without API keys  
✅ **Production-Ready**: Error handling & persistence  

---

## Need Help?

1. Check `README.md` for full documentation
2. View `SUBMISSION.md` for technical details
3. Check `logs/` folder for error logs
4. View Observability tab for system status

---

**Ready to Research! 🔍🤖**

*Built for Kaggle Agents Intensive Capstone Project*
