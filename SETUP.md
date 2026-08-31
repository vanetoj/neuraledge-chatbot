# NeuralEdge AI Chatbot - Streamlit Setup

## Files You Have

- `app.py` - Your complete chatbot (ONE file!)
- `requirements.txt` - Dependencies
- `.env.example` - Template (copy to `.env`)

## Step 1: Get API Key

1. Go to: https://console.anthropic.com/account/keys
2. Copy your key
3. Create file `.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxx
```

## Step 2: Install Dependencies

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 3: Run Locally

```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

## Step 4: Deploy FREE

### On Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your GitHub repo and `app.py`
5. In app Settings → Secrets, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-xxxxxxx"
   ```
6. Done! Your app is live

### On Your Website

Add a button or link:
```html
<a href="https://your-app.streamlit.app" target="_blank">
    💬 Chat with AI
</a>
```

## Customize

Edit `app.py`:

```python
CALENDLY_LINK = "https://calendly.com/your-link"  # Line ~10
SERVICE_KNOWLEDGE = """Update with your services"""  # Line ~15
```

## Troubleshooting

**"No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

**"ANTHROPIC_API_KEY not found"**
- Make sure `.env` file exists with your key
- Or set environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`

**"Message takes too long"**
- Normal on free tier (2-3 seconds)
- Upgrade to Streamlit Cloud paid for faster responses

## Done! 🎉

That's literally all you need. The chatbot is ready to use.
