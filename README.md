# Dream Analysis Room 🌙

A personalized, AI-powered dream interpretation assistant built with **Streamlit**, **LangChain**, and **ZhipuAI**. It helps you record, analyze, and gain deep psychological insights from your dreams.

## ✨ Features
- **Voice-to-Text**: Effortlessly record your dreams using your microphone (powered by OpenAI Whisper).
- **AI Psychological Analysis**: Get 4-dimensional insights into your dreams, including emotional themes and subconscious symbolism.
- **Streaming Response**: Experience real-time AI responses with an elegant "typewriter" effect.
- **Historical Archive**: Save and manage your dream history in a local database.
- **Emotional Insights**: Visualize your emotional trends with interactive charts and word clouds.
- **Interactive Dialogue**: Chat with your AI mentor to explore the hidden meaning behind your dreams.

## 🛠 Tech Stack
- **Frontend**: Streamlit
- **Language**: Python
- **AI Model**: GLM-4-Flash (via ZhipuAI)
- **Transcription**: Whisper (OpenAI)
- **Data Analysis**: Pandas, Plotly, WordCloud

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [ZhipuAI API Key](https://open.bigmodel.cn/)

### Configuration

Before running the application, you need to set up your API keys in a TOML configuration file:

1. Create a `config.toml` file in the project root directory:
   ```bash
   touch config.toml
   ```

2. Add your API keys to `config.toml`:
   ```toml
   [api]
   zhipuai_key = "your-zhipuai-api-key-here"
   openai_key = "your-openai-api-key-here"
   ```

3. **IMPORTANT**: Add `config.toml` to `.gitignore` to protect your credentials:
   ```bash
   echo "config.toml" >> .gitignore
   ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/chwe218/dream-analysis-room.git
   cd dream-analysis-room
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your configuration file (see [Configuration](#configuration) section above)

4. Run the application:
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📝 Usage

1. **Record a Dream**: Click the microphone button and speak your dream
2. **Analyze**: Let the AI analyze your dream with psychological insights
3. **Explore**: Chat with the AI mentor to dig deeper into the meanings
4. **Track**: View your dream history and emotional trends over time

## ⚠️ Troubleshooting

**"API Key not found" error**: 
- Make sure your `config.toml` file exists in the project root
- Verify your API keys are correctly set in `config.toml`
- Check that you haven't accidentally committed `config.toml` to git

**"Whisper Error"**:
- Ensure you have a valid OpenAI API key in `config.toml`
- Check your microphone permissions

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🌟 Acknowledgments

- Powered by [ZhipuAI](https://open.bigmodel.cn/) and [OpenAI](https://openai.com/)
- Built with [Streamlit](https://streamlit.io/) and [LangChain](https://langchain.com/)
