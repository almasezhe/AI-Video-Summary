# 🎬 YouTube AI Video Analyzer

🚀 A mini-application for analyzing YouTube videos with AI:
- downloads audio from YouTube,
- transcribes it using OpenAI Whisper,
- analyzes the content using GPT-4o,
- returns a short, structured summary: bullet points + key highlights.

## ✨ Features
- 🔥 Audio-only download from YouTube
- 🧠 Transcription of audio using Whisper
- 🤖 Smart text analysis with ChatGPT
- 📜 Output includes video title + short structured summary
- 🖥 Chrome Extension for quick YouTube link submission

## 📦 Technologies Used
- FastAPI for backend server
- yt-dlp for downloading audio
- OpenAI Whisper for transcription
- OpenAI GPT-4o for text summarization
- Chrome Extension for user interface

## ⚙️ Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/ai-youtube-analyzer.git
cd ai-youtube-analyzer/backend
```

### 2. Install backend dependencies
```bash
pip install -r requirements.txt
```
> Note: Make sure [ffmpeg](https://ffmpeg.org/) is installed on your system.

### 3. Create a `.env` file
Inside the `backend/` folder, create a `.env` file containing your OpenAI API key:
```dotenv
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 4. Run the backend server
```bash
uvicorn main:app --reload
```
The server will run at http://127.0.0.1:8000

### 5. Install Chrome Extension
- Open `chrome://extensions`
- Enable "Developer Mode"
- Click "Load unpacked"
- Select the `extension/` folder from the project

## 🚀 How to Use
1. Start the FastAPI server.
2. Open the Chrome Extension.
3. Paste the YouTube video link.
4. Click "Analyze."
5. After a few seconds, you will receive:
   - Video title
   - 5–7 bullet points summarizing the content
   - Key important highlights
   - A brief overall description

