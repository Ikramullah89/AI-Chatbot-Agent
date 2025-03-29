import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

# Set Page Configurations
st.set_page_config(page_title="LangGraph AI Chatbot", layout="centered")

# Custom Styling
st.markdown(
    """
    <style>
    body { font-family: 'Arial', sans-serif; }
    .stTextArea textarea { font-size: 16px; }
    .stButton button { background-color: #4CAF50; color: white; font-size: 16px; padding: 10px 20px; border-radius: 8px; }
    .stSelectbox div { font-size: 16px; }
    .stRadio div { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True
)

# Header Section
st.markdown("## 🤖 AI Chatbot Agents")
st.write("Create and Interact with AI Agents using LangGraph!")
add_vertical_space(1)

# System Prompt Input
system_prompt = st.text_area("📝 Define your AI Agent:", height=80, placeholder="Type your system prompt here...")

# Model Selection
st.markdown("### 🔍 Select AI Model")
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("🌐 Choose Provider:", ("Groq", "OpenAI"), horizontal=True)

if provider == "Groq":
    selected_model = st.selectbox("🤖 Groq Models:", MODEL_NAMES_GROQ)
else:
    selected_model = st.selectbox("🤖 OpenAI Models:", MODEL_NAMES_OPENAI)

# Allow Web Search Option
allow_web_search = st.checkbox("🔎 Allow Web Search")

# User Query Input
user_query = st.text_area("💬 Enter your query:", height=150, placeholder="Ask Anything!")

# API Endpoint
API_URL = "http://127.0.0.1:9999/chat"

# Send Query Button
if st.button("🚀 Ask AI Agent!"):
    if user_query.strip():
        with st.spinner("Processing your request..."):
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    st.success("✅ Response received!")
                    st.markdown("### 🤖 AI Response")
                    st.markdown(f"**{response_data}**")
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
