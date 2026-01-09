# Deployment Guide - CX Agent for Stanza Living

This guide explains how to deploy the CX Agent chatbot publicly so users can access it with their own API keys.

## 🚀 Quick Deploy Options

### Option 1: Streamlit Cloud (Recommended - Free & Easy)

1. **Prerequisites**
   - GitHub account
   - Push this repository to GitHub
   - Get a free Groq API key from [console.groq.com](https://console.groq.com)

2. **Deploy Steps**
   ```bash
   # Make sure all changes are committed and pushed
   git add .
   git commit -m "Prepare for public deployment"
   git push origin claude/deploy-public-release-NCFJ3
   ```

3. **On Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `NeerajMehta15/CX_Chatbot_Agent`
   - Branch: `claude/deploy-public-release-NCFJ3` (or your main branch)
   - Main file path: `app.py`
   - Click "Deploy"

4. **That's it!** Your app will be live at: `https://[your-app-name].streamlit.app`

5. **Share with Users**
   - Users visit your app URL
   - They enter their own Groq API key in the sidebar
   - They can start chatting immediately!

---

### Option 2: Docker Deployment

1. **Create Dockerfile** (if not exists)
   ```dockerfile
   FROM python:3.12-slim

   WORKDIR /app

   # Copy requirements
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application files
   COPY . .

   # Expose Streamlit port
   EXPOSE 8501

   # Run the app
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**
   ```bash
   # Build the Docker image
   docker build -t cx-chatbot .

   # Run the container
   docker run -p 8501:8501 cx-chatbot
   ```

3. **Access the app at**: `http://localhost:8501`

---

### Option 3: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/NeerajMehta15/CX_Chatbot_Agent.git
   cd CX_Chatbot_Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app at**: `http://localhost:8501`

---

## 🔑 User Instructions

When users access your deployed app, they should:

1. **Get a Groq API Key** (Free)
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up or log in
   - Navigate to "API Keys" section
   - Click "Create API Key"
   - Copy the generated key

2. **Use the Chatbot**
   - Open your deployed app URL
   - Look for the sidebar on the left
   - Paste their Groq API key in the "Groq API Key" field
   - Enter their user ID (e.g., U101)
   - Start asking questions!

---

## 📦 What's Included

The app includes:
- **FAQ Handling**: Answers common questions using semantic search
- **Ticket Management**: Create and check support tickets
- **Payment Information**: Check payment status and details
- **User Information**: Retrieve user profile data
- **Escalation**: Auto-creates tickets for unresolved issues

---

## 🔒 Security & Privacy

- **No API Keys Stored**: User API keys are stored only in session memory and never saved to disk or database
- **Client-Side Processing**: API keys are used directly from the browser session
- **No Backend Storage**: All data processing happens in real-time with no persistent storage of credentials
- **HTTPS Required**: For production deployment, always use HTTPS

---

## 🛠️ Technical Details

### Tech Stack
- **Frontend**: Streamlit (Python web framework)
- **AI Framework**: LangChain + LangGraph
- **LLM Provider**: Groq (llama3-70b-8192 model)
- **Vector Store**: Chroma DB (for FAQ semantic search)
- **Embeddings**: Mistral AI embeddings

### Data Storage
- Local CSV files for demo data (`data/` directory)
- Vector database stored in `data/chroma/`
- For production, consider migrating to a proper database (PostgreSQL, MongoDB)

### Resource Requirements
- **RAM**: 2GB minimum
- **Storage**: 500MB (including dependencies)
- **CPU**: 1 core sufficient for demo usage

---

## 🌐 Public URL Sharing

After deployment on Streamlit Cloud, you'll get a URL like:
```
https://cx-agent-stanza-living.streamlit.app
```

Share this URL with anyone! They can:
- Use their own Groq API key (free tier available)
- Test all chatbot features
- No login required (except for Groq API key)

---

## 🔧 Customization

### Branding
Edit `app.py` to customize:
- Page title (line 8)
- Page icon (line 9)
- Sidebar text (lines 14-23)
- Color scheme (see `.streamlit/config.toml`)

### Data
Replace CSV files in `data/` directory:
- `faq.csv`: Update FAQ questions and answers
- `tickets.csv`: Ticket history
- `payments.csv`: Payment records
- `user_info.csv`: User profiles

---

## ⚠️ Known Limitations

1. **CSV Data Storage**: Not suitable for production at scale
2. **Single Instance**: No load balancing or horizontal scaling
3. **No Authentication**: Anyone with the URL can access (but they need their own API key)
4. **Session State**: Conversation history is not persisted across sessions
5. **Rate Limits**: Subject to Groq API rate limits (based on user's API key tier)

---

## 📊 Monitoring & Analytics

For production deployment, consider adding:
- **Error Tracking**: Sentry, DataDog
- **Analytics**: Google Analytics, Mixpanel
- **Logging**: CloudWatch, ELK Stack
- **Uptime Monitoring**: UptimeRobot, Pingdom

---

## 🆘 Troubleshooting

### App won't start
- Check `requirements.txt` includes all dependencies
- Verify Python version is 3.12 or compatible
- Ensure `data/` directory exists with CSV files

### API Key errors
- Verify Groq API key is valid
- Check API rate limits haven't been exceeded
- Try generating a new API key from Groq Console

### Vector store initialization fails
- Delete `data/chroma/` directory and restart
- The app will rebuild the vector store from `data/faq.csv`

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Groq API docs: [console.groq.com/docs](https://console.groq.com/docs)


