import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
CALENDLY_LINK = "https://calendly.com/todorovania"

SERVICE_KNOWLEDGE = """NeuralEdge AI offers 10 core AI services:

1. **Voice agents** - 24/7 AI phone support, appointment booking, call handling
   - 30% of calls resolved without humans
   - Always available, no hold times
   - Technologies: ElevenLabs, Vapi, Retell AI

2. **AI copilots** - Custom AI assistants trained on business data
   - 4x productivity gain reported
   - 65% of Fortune 500 use AI copilots
   - Technologies: Claude API, OpenAI API, RAG, Fine-tuning

3. **RAG systems** - AI that searches your docs and databases accurately
   - 97% accuracy with grounding
   - Searches across 1M+ docs in <1s
   - Technologies: LlamaIndex, LangChain, Pinecone

4. **Custom LLM fine-tuning** - Domain-specialized models trained on your data
   - 10x better domain accuracy
   - 60% lower inference cost
   - Technologies: OpenAI fine-tuning, Hugging Face, LoRA

5. **Document processing** - Extract and structure data from invoices, contracts, forms
   - 90% less manual data entry
   - Supports any document type
   - Technologies: Azure Document AI, AWS Textract, Google DocAI

6. **Translation & localization** - 100+ language support for content and AI systems
   - Real-time live translation
   - Content localization at scale
   - Technologies: DeepL API, GPT-4o, ElevenLabs

7. **Predictive analytics & NLP** - Forecasting, regression, ML, text analysis
   - 95% forecast accuracy
   - Works with any industry or data type
   - Technologies: Prophet, ARIMA, LSTM, XGBoost

8. **AI scribes** - Transcribe and summarize meetings, calls, consultations
   - 35% less documentation time
   - 99% transcription accuracy
   - Technologies: Whisper, AssemblyAI, Deepgram

9. **Audio & video AI** - Generate podcasts, voiceovers, synthetic video
   - 10x faster than traditional production
   - Any language or voice style
   - Technologies: ElevenLabs, Suno, Udio, HeyGen, Runway

10. **AI consulting** - Roadmap, POC, ROI analysis, vendor selection
    - Free discovery call
    - 2 weeks to working POC
    - Includes: AI roadmap, ROI analysis, vendor selection, team training

Company info:
- Small team of data scientists and engineers
- Custom-built solutions, not off-the-shelf
- You work directly with engineers, not salespeople
- Fast decisions, faster delivery
- Book a free discovery call: {CALENDLY_LINK}"""

SYSTEM_PROMPT = f"""You are a sales assistant for NeuralEdge AI, a specialist AI services company. Your role is to:

1. Understand what the prospect needs
2. Recommend relevant NeuralEdge AI services
3. Explain benefits specific to their use case
4. Naturally guide them toward booking a free discovery call
5. Be conversational, warm, and knowledgeable - not pushy

SERVICE KNOWLEDGE:
{SERVICE_KNOWLEDGE}

In every response:
- Be helpful and specific about our services
- Ask qualifying questions to understand their needs
- When they show interest in a service, briefly explain the benefit
- Suggest booking a discovery call when appropriate - phrase it as "Let me connect you with our team" or "This deserves a proper conversation with the engineers"
- Keep responses concise (2-3 sentences typically)
- Always be ready to answer follow-ups about specific services
- If they ask to book a call, provide the Calendly link: {CALENDLY_LINK}"""

# ==================== STREAMLIT CONFIG ====================
st.set_page_config(
    page_title="NeuralEdge AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    footer {visibility: hidden;}
    .stChatMessage {padding: 1rem;}
    h1 {background: linear-gradient(135deg, #534AB7 0%, #1D9E75 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;}
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    try:
        st.session_state.api_key = st.secrets["ANTHROPIC_API_KEY"]
    except:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY")

# ==================== HEADER ====================
col1, col2 = st.columns([1, 5])
with col1:
    st.write("🤖")
with col2:
    st.markdown("### NeuralEdge AI Assistant")
    st.markdown('<div style="color: #666; font-size: 13px;">Ready to help • Ask about our AI services</div>', unsafe_allow_html=True)

st.divider()

# ==================== CHAT HISTORY ====================
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# ==================== CHAT INPUT ====================
if prompt := st.chat_input("Ask me about our services..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        if not st.session_state.api_key:
            st.error("❌ ANTHROPIC_API_KEY not found. Check your .env file.")
        else:
            with st.spinner("Thinking..."):
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    
                    message = client.messages.create(
                        model="claude-opus-4-6",
                        max_tokens=500,
                        system=SYSTEM_PROMPT,
                        messages=[
                            {"role": msg["role"], "content": msg["content"]}
                            for msg in st.session_state.messages
                        ]
                    )
                    
                    assistant_message = message.content[0].text
                    st.write(assistant_message)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                    
                except anthropic.AuthenticationError:
                    st.error("❌ Invalid API key. Check your .env file.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ==================== SUGGESTIONS ====================
if len(st.session_state.messages) == 0:
    st.write("")
    st.markdown("**💡 Try asking about:**")
    cols = st.columns(2)
    
    suggestions = [
        ("Voice Agents", "Can you help with 24/7 call handling?"),
        ("AI Copilots", "How do I train AI on our company data?"),
        ("Document Processing", "Can you extract data from invoices?"),
        ("Translation", "Do you support multilingual AI?"),
    ]
    
    for idx, (title, question) in enumerate(suggestions):
        col = cols[idx % 2]
        with col:
            if st.button(f"📌 {title}", key=f"btn_{idx}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

# ==================== FOOTER ====================
st.divider()
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>🎯 <strong>Ready to explore further?</strong></p>
    <p><a href="{CALENDLY_LINK}" target="_blank" style="color: #534AB7; text-decoration: none; font-weight: 600;">
        → Book a free 30-minute discovery call
    </a></p>
    <p style="margin-top: 1rem; font-size: 11px;">NeuralEdge AI • Specialist AI Services</p>
</div>
""", unsafe_allow_html=True)
