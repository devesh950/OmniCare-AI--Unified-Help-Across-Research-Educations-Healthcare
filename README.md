# 🌟 OmniCare AI - Unified Help Across Research, Learning & Health

A powerful 7-agent system addressing humanity's core needs: **personalized education**, **healthcare navigation**, and **accessible research**. Built with WCAG 2.1 Level AA compliance and designed to serve millions who lack access to tutors, healthcare guidance, or accessible information.

## 🎯 Project Overview

**Created for:** Kaggle Agents Intensive Capstone Project  
**Track:** 🤝 **Agents for Good**  
**Mission:** Empowering Humanity Through Accessible AI

### The Problems We Solve

**📚 Education Gap:**
- **258 million children** worldwide lack access to education
- Private tutors cost $40-100/hour - unaffordable for many
- One-size-fits-all teaching doesn't work for diverse learners
- People with disabilities need adaptive learning support

**🏥 Healthcare Navigation Crisis:**
- **90 million Americans** have low health literacy
- People don't know when to seek urgent vs. routine care
- **30% of ER visits** could be handled elsewhere (unnecessary $1,000+ costs)
- Medical information is confusing and overwhelming

**♿ Research Accessibility:**
- **2.2 billion people** have vision impairment worldwide
- Research websites aren't screen reader friendly
- No audio alternatives for visual content
- Manual accessible research takes 3-5x longer

### Our Solution

A **7-agent collaborative system** providing:
- 🎓 **Free personalized tutoring** for all subjects and levels
- 🩺 **Healthcare navigation** with urgency triage and guidance
- ♿ **Accessible research** with WCAG 2.1 AA compliance
- 🔊 **Audio-ready content** for all outputs

## 🤖 Multi-Agent Architecture (7 Agents)

### 🎓 Education & Learning

### 1. Education Tutor Agent (`agents/education_tutor_agent.py`)
- **Role:** Personalized Learning Assistant
- **Impact:** Free tutoring accessible 24/7
- **Capabilities:**
  - Adaptive difficulty levels (Elementary → Advanced)
  - Multiple learning styles (Visual, Auditory, Kinesthetic, Reading/Writing)
  - Concept explanations with real-world examples
  - Step-by-step problem solving guidance
  - Practice problem generation with solutions
  - Learning path recommendations
- **Subjects:** Math, Science, Computer Science, Language Arts, History

### 🏥 Healthcare & Wellness

### 2. Healthcare Navigator Agent (`agents/healthcare_navigator_agent.py`)
- **Role:** Medical Information Assistant
- **Impact:** Helps people navigate healthcare decisions safely
- **Capabilities:**
  - **Urgency triage:** Emergency, Urgent, Soon, Routine, Self-care
  - **Emergency detection:** Identifies life-threatening situations
  - Symptom assessment guidance
  - Plain language medical information
  - Prevention and wellness tips
  - Healthcare resource navigation
  - **⚠️ Educational only - NOT medical diagnosis**

### 🔬 Research & Information

### 3. Research Agent (`agents/research_agent.py`)
- **Role:** Information Discovery
- **Capabilities:**
  - Web search using DuckDuckGo (no API key required)
  - Wikipedia integration for authoritative information
  - Fallback mechanisms for reliability
  - Content extraction and parsing

### 4. Summarizer Agent (`agents/summarizer_agent.py`)
- **Role:** Information Analysis & Synthesis
- **Capabilities:**
  - Extractive text summarization
  - Key point extraction
  - Sentence scoring and ranking
  - Multiple summary length options

### 5. Report Generator Agent (`agents/report_generator.py`)
- **Role:** Documentation & Presentation
- **Capabilities:**
  - Professional report formatting
  - Citation generation (IEEE-style)
  - Structured analysis sections
  - Multiple export formats

### ♿ Accessibility & Inclusion

### 6. Accessibility Agent (`agents/accessibility_agent.py`)
- **Role:** Universal Access & WCAG Compliance
- **Impact:** Makes all content accessible to people with disabilities
- **Capabilities:**
  - WCAG 2.1 Level AA validation
  - Screen reader optimization
  - Semantic markup generation
  - Accessibility scoring (0-100)
  - Content simplification
  - Heading hierarchy fixes
  - Descriptive link text
  - Reading order optimization

### 7. Text-to-Speech Agent (`agents/tts_agent.py`)
- **Role:** Audio Content Generation
- **Impact:** Enables audio consumption of all content
- **Capabilities:**
  - SSML (Speech Synthesis Markup) generation
  - Natural pause insertion
  - Abbreviation expansion
  - Audio navigation menus
  - Duration estimation
  - Speech-ready text optimization
  - Break point identification

### Supporting Systems

### 6. Session Management (`utils/session_manager.py`)
- **SessionService**: Manages user sessions and state
- **MemoryBank**: Long-term memory for research history
- **Context Engineering**: Compacts and optimizes context

### 7. Observability System (`utils/observability.py`)
- **AgentLogger**: Comprehensive logging
- **AgentTracer**: Distributed tracing with trace IDs
- **MetricsCollector**: Performance metrics and analytics

## ✨ Features

### 🤝 Accessibility Features (Agents for Good)
- **♿ WCAG 2.1 Level AA Compliant**: Meets international accessibility standards
- **🔊 Audio Descriptions**: Text-to-speech ready content with SSML
- **📱 Screen Reader Optimized**: Proper semantic markup and structure
- **🎨 High Contrast Mode**: Better visibility for low vision users
- **⌨️ Keyboard Navigation**: Full keyboard accessibility
- **📖 Simplified Text**: Easy-to-understand language
- **🎧 Audio Navigation**: Voice command support
- **📊 Accessibility Scoring**: Real-time compliance metrics (0-100)
- **✓ WCAG Validation**: Automatic compliance checking
- **💾 Multiple Formats**: Accessible Markdown, audio scripts, validation reports

### Core Research Features
- **🌐 No API Key Required**: Works out-of-the-box with web scraping
- **🔑 Optional OpenAI Integration**: Enhanced capabilities with API key
- **📊 Real-time Progress Tracking**: Visual feedback during research
- **💾 Research History**: Save and reload previous sessions
- **📥 Multiple Export Formats**: Accessible formats prioritized
- **🎨 Beautiful UI**: Professional, WCAG-compliant interface
- **⚙️ Customizable Settings**: Adjust for accessibility needs
- **📚 Multi-source Aggregation**: Combines information from various sources

### Advanced Technical Features
- **🤖 5-Agent System**: Specialized agents working collaboratively
- **🔧 Custom Tools**: Web search, summarization, accessibility, TTS
- **💾 Sessions & Memory**: State management with persistence
- **📊 Full Observability**: Logging, tracing, metrics
- **🔄 Context Engineering**: Smart compaction strategies

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Open your browser** to `http://localhost:8501`

### Usage

1. **Enter a research topic** in the Research tab
2. **Configure settings** (optional) in the sidebar
3. **Click "Start Research"** and watch the agents work
4. **View results** in the Results tab
5. **Export your report** in your preferred format

## 📁 Project Structure

```
Agents Intensive/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── SUBMISSION.md                   # Capstone submission writeup
├── .gitignore                      # Git ignore file
├── .env.example                    # Environment variables template
│
├── agents/                         # Agent modules
│   ├── __init__.py                 # Agent module initialization
│   ├── research_agent.py           # Web research & search agent
│   ├── summarizer_agent.py         # Text analysis & summarization agent
│   └── report_generator.py         # Report compilation agent
│
├── utils/                          # Utility modules
│   ├── __init__.py                 # Utils module initialization
│   ├── session_manager.py          # Sessions & Memory management
│   └── observability.py            # Logging, Tracing, Metrics
│
├── sessions/                       # Session storage (created at runtime)
├── memory_bank/                    # Long-term memory storage (created at runtime)
├── logs/                           # Application logs (created at runtime)
└── traces/                         # Execution traces (created at runtime)
```

## 🔧 Configuration

### Basic Configuration (No API Key)
The application works immediately with:
- DuckDuckGo web search
- Wikipedia integration
- Extractive summarization
- All core features

### Enhanced Configuration (With Gemini API Key)
For advanced features, add your Google Gemini API key in the sidebar:
- AI-powered educational content generation
- Enhanced health information
- More sophisticated explanations

### Settings You Can Customize:
- **Max Search Results**: 3-10 results
- **Summary Length**: Short, Medium, or Detailed
- **Research Type**: General, Academic, News, Technical
- **Export Format**: Markdown, PDF, JSON
- **Citations**: Enable/disable source citations

## 💡 Example Use Cases

1. **Academic Research**
   - Topic: "Climate change impact on biodiversity"
   - Get: Comprehensive analysis with academic sources

2. **Technology Trends**
   - Topic: "Latest developments in quantum computing"
   - Get: Current information from multiple tech sources

3. **Market Research**
   - Topic: "Electric vehicle market trends 2024"
   - Get: Aggregated data and analysis

4. **General Knowledge**
   - Topic: "History of artificial intelligence"
   - Get: Well-structured overview with citations

## 🛠️ Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **Requests**: HTTP library for web scraping
- **BeautifulSoup4**: HTML parsing
- **Google Gemini API**: Optional AI-powered content generation
- **Python 3.8+**: Programming language

### Agent Communication Flow
```
User Input → Research Agent → Search Results
                ↓
         Summarizer Agent → Analysis
                ↓
      Report Generator → Final Report → User
```

### Key Design Decisions

1. **No API Key Required**: Uses DuckDuckGo and Wikipedia for accessibility
2. **Modular Architecture**: Each agent is independent and reusable
3. **Fallback Mechanisms**: Ensures reliability even when searches fail
4. **Clean UI**: Focus on user experience with Streamlit
5. **Export Options**: Multiple formats for different use cases

## 🎓 Learning Objectives Demonstrated

This project showcases:
- ✅ Multi-agent system design (3 sequential agents)
- ✅ Custom tool creation (web search, summarization, report generation)
- ✅ Task decomposition and specialization
- ✅ Sessions & state management (SessionService)
- ✅ Long-term memory (MemoryBank)
- ✅ Context engineering (compaction strategies)
- ✅ Observability: Logging (AgentLogger)
- ✅ Observability: Tracing (AgentTracer with trace IDs)
- ✅ Observability: Metrics (MetricsCollector)
- ✅ Web scraping and API integration
- ✅ Natural language processing
- ✅ User interface design
- ✅ Error handling and fallback strategies
- ✅ Data persistence and history management
- ✅ Report generation and formatting

### Capstone Requirements Met

✅ **Multi-agent system**: 3 sequential agents (Research → Summarize → Report)
✅ **Custom tools**: Web search, Wikipedia, text summarization, report generation
✅ **Sessions & Memory**: SessionService + MemoryBank + Context compaction
✅ **Observability**: Comprehensive logging, distributed tracing, metrics collection

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Search returns no results
**Solution:** 
- Check your internet connection
- The app will use fallback results automatically
- Try a different search query

### Issue: Streamlit won't start
**Solution:**
```bash
# Try running with explicit Python
python -m streamlit run app.py
```

### Issue: OpenAI features not working
**Solution:**
- Verify your API key is correct
- Check you have OpenAI credits available
- The app still works without OpenAI features

## 📝 Future Enhancements

Possible improvements:
- [ ] Add more search providers (Google, Bing)
- [ ] Implement PDF export functionality
- [ ] Add image search and inclusion
- [ ] Create comparison mode for multiple topics
- [ ] Add collaborative filtering
- [ ] Implement caching for faster repeated searches
- [ ] Add multilingual support
- [ ] Create API endpoint for programmatic access

## 🤝 Contributing

This is a capstone project, but suggestions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Share your use cases

## 📄 License

This project is created for educational purposes as part of the Kaggle Agents Intensive Capstone Project.

## 👨‍💻 Author

Created for Kaggle Agents Intensive - November 2025

## 🙏 Acknowledgments

- Kaggle for the Agents Intensive program
- Streamlit for the amazing framework
- DuckDuckGo for providing search capabilities
- Wikipedia for open knowledge access

---

## 📞 Support

For questions or issues:
1. Check the Troubleshooting section above
2. Review the code comments for implementation details
3. Check Streamlit documentation: https://docs.streamlit.io

---

**Happy Researching! 🔍🤖**

*This multi-agent system demonstrates how specialized AI agents can collaborate to solve complex tasks efficiently and effectively.*
