# Simple RAG Chat with BeyondLLM

A super simple Retrieval-Augmented Generation (RAG) chatbot that lets you chat with **YouTube videos** or **uploaded files** using Google's Gemini AI. Everything is configured directly in the UI - no .env files needed!

## ✨ Features

- 🎥 **YouTube Video Support** - Chat with any YouTube video
- 📄 **File Upload Support** - Upload PDF, TXT, MD, DOC, or DOCX files
- 🔑 **UI-Based Setup** - Enter API key directly in the app (no .env file required!)
- 💬 **Modern Chat Interface** - Clean, ChatGPT-like experience
- 🤖 **Powered by Google Gemini** - Uses Gemini 2.5 Flash Lite for fast, intelligent responses
- 📝 **Chat History** - Maintains full conversation context
- 🔄 **Easy Reset** - Start over with one click
- 🎨 **Super Simple** - No complex configuration required

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run Streamlit_app.py
```

### 3. Setup in the UI

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get a free API key
2. **Enter API Key**: Paste it in the password field in the app
3. **Choose Source**: Select "YouTube Video" or "Upload File"
4. **Provide Content**: 
   - For YouTube: Paste the video URL
   - For File: Upload your document (PDF, TXT, MD, DOC, DOCX)
5. **Click "Start Chat"**: Wait for initialization (takes a few seconds)
6. **Ask Questions**: Start chatting with your content!

## 📖 How to Use

### With YouTube Videos

1. Copy any YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Select "YouTube Video" option
3. Paste the URL
4. Click "Start Chat"
5. Ask questions about the video content

**Example Questions:**
- "What is this video about?"
- "Summarize the main points"
- "What does the speaker say about [topic]?"

### With Files

1. Prepare your file (PDF, TXT, MD, DOC, or DOCX)
2. Select "Upload File" option
3. Upload your file
4. Click "Start Chat"
5. Ask questions about the document content

**Example Questions:**
- "What are the key points in this document?"
- "Explain [specific topic] from the file"
- "Summarize this document"

## 🛠️ Requirements

- Python 3.8 or higher
- Google API Key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 📦 Dependencies

All dependencies are in `requirements.txt`:
- `streamlit>=1.28.0` - Web interface
- `beyondllm>=0.2.0` - RAG framework
- `python-dotenv>=1.0.0` - Environment variables (optional)

## 🎯 How It Works

1. **Content Loading**: The app loads your YouTube video or uploaded file
2. **Chunking**: Content is split into manageable chunks
3. **Embedding**: Chunks are converted to vector embeddings using Gemini
4. **Retrieval**: When you ask a question, relevant chunks are retrieved
5. **Generation**: Gemini 2.5 Flash Lite generates an answer based on the retrieved context

## 🔄 Reset and Start Over

Click the "🔄 Start Over" button in the sidebar to:
- Clear chat history
- Reset the pipeline
- Choose a new content source

## 🆘 Troubleshooting

### "API key not found" error
- Make sure you entered your Google API key in the text field
- Get a free key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### "Error loading content" message
- For YouTube: Check that the URL is valid and the video has captions/transcript
- For Files: Ensure the file format is supported (PDF, TXT, MD, DOC, DOCX)

### Slow initialization
- First-time loading takes 10-30 seconds (normal)
- YouTube videos with long transcripts take longer
- Large files take longer to process

### No response or error during chat
- Check your internet connection
- Verify your API key is valid
- Try clicking "Start Over" and reinitializing

## 📚 Learn More

- [BeyondLLM Documentation](https://beyondllm.aiplanet.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🎓 Built With

- **Streamlit** - Web framework
- **BeyondLLM** - RAG framework
- **Google Gemini** - LLM and embeddings
- **Python** - Programming language

---

**Made simple for everyone!** 🚀

No complex setup, no configuration files, just run and chat!
