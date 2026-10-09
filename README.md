# Dream Analysis Room 🌙

A Chinese-language dream journal built with **Streamlit**, **LangChain** and **GLM-4-Flash**. Speak your dream, get a structured AI analysis, and track your moods over time.

> **Status:** early-stage learning project. I built it to practise connecting speech recognition, an LLM and data visualisation in one app.

## Features

- **Voice input:** record a dream with your microphone; it is transcribed locally with OpenAI's open-source Whisper model (`base`, Chinese).
- **AI analysis:** GLM-4-Flash (via LangChain) streams a four-part analysis (emotion, imagery, subconscious message, advice) and a mood tag.
- **Follow-up chat:** ask the AI mentor more questions about the dream.
- **Dream archive:** save each dream with a mood score to a local CSV file (`dream_log.csv`).
- **Insights:** mood-trend chart, mood-tag pie chart (Plotly) and a word cloud of recurring themes.

## Tech stack

Python · Streamlit · LangChain (`langchain-community`, `ChatZhipuAI`) · GLM-4-Flash (ZhipuAI) · OpenAI Whisper (local) · Pandas · Plotly · Matplotlib · WordCloud · OpenCC

## Getting started

**Prerequisites**

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) installed (required by Whisper)
- A [ZhipuAI API key](https://open.bigmodel.cn/)

**Install**

```bash
git clone https://github.com/chwe218/dream-analysis-room.git
cd dream-analysis-room
pip install -r requirements.txt
```

**Add your API key**

Create `.streamlit/secrets.toml` in the project folder:

```toml
ZHIPUAI_API_KEY = "your-zhipuai-api-key-here"
```

This file is listed in `.gitignore` so your key is never committed.

**Run**

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Usage

1. **Record** a dream with the microphone and edit the transcript if needed.
2. **Analyse** it and read the streamed result.
3. **Ask** follow-up questions in the chat.
4. **Archive** the dream with a mood score, then open the archive tab to see your trends.

## Known limitations

- The word cloud uses a Windows font path (`C:\Windows\Fonts\msyh.ttc`). On macOS or Linux, change this path to a Chinese-capable font on your system.
- The archive tab reads `dream_log.csv`, which is created when you archive your first dream. Archive one dream before opening it.
- The interface and prompts are in Chinese.

## Possible next steps

- Cross-platform font handling
- Replace the CSV with a small database
- Input validation and error handling
- Automated tests

## Acknowledgments

Built with [Streamlit](https://streamlit.io/), [LangChain](https://langchain.com/), [ZhipuAI](https://open.bigmodel.cn/) and [OpenAI Whisper](https://github.com/openai/whisper).
