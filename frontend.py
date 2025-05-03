import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

# Set Page Configurations
st.set_page_config(page_title="AI Diet Consultant", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    body { font-family: 'Arial', sans-serif; background-color: #f4f9f4; }
    .stTextInput input, .stNumberInput input, .stSelectbox div { font-size: 16px; border-radius: 8px; }
    .stTextArea textarea { font-size: 16px; border-radius: 8px; }
    .stButton button { 
        background-color: #28a745; 
        color: white; 
        font-size: 16px; 
        padding: 10px 20px; 
        border-radius: 8px; 
        border: none; 
    }
    .stButton button:hover { background-color: #218838; }
    .card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        margin-bottom: 20px; 
    }
    .header { color: #2c3e50; font-size: 28px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True
)

# Header Section
st.markdown("<div class='header'>🥗 AI Diet Consultant</div>", unsafe_allow_html=True)
st.write("Your personalized diet planner powered by AI! Enter your details to get a tailored diet plan.")
add_vertical_space(1)

# Sidebar for User Inputs
with st.sidebar:
    st.markdown("### 📋 Your Profile")
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=1.0)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=1.0)
    age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    activity_level = st.selectbox("Activity Level", [
        "Sedentary (little or no exercise)",
        "Lightly active (light exercise/sports 1-3 days/week)",
        "Moderately active (moderate exercise/sports 3-5 days/week)",
        "Very active (hard exercise/sports 6-7 days/week)"
    ])
    work_hours = st.text_input("Work Hours (e.g., 9 AM - 5 PM)", value="9 AM - 5 PM")

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
allow_web_search = st.checkbox("🔎 Allow Web Search for Nutrition Data")

# User Query Input
user_query = st.text_area("💬 Any specific dietary preferences or questions? (e.g., vegetarian, low-carb)", height=100, placeholder="Ask about your diet or leave blank for a general plan...")

# API Endpoint
API_URL = "http://127.0.0.1:9999/chat"

# Session State for Diet Plan
if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = None
    st.session_state.alternative_requested = False

# Send Query Button
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🚀 Generate Diet Plan"):
        if height and weight and age:
            with st.spinner("Calculating your personalized diet plan..."):
                user_data = {
                    "height": height,
                    "weight": weight,
                    "age": age,
                    "gender": gender.lower(),
                    "activity_level": activity_level.split(" (")[0].lower(),
                    "work_hours": work_hours
                }
                payload = {
                    "model_name": selected_model,
                    "model_provider": provider,
                    "system_prompt": "AI Diet Consultant",
                    "messages": [user_query or "Generate a diet plan based on user data"],
                    "allow_search": allow_web_search,
                    "user_data": user_data,
                    "request_alternative": st.session_state.alternative_requested
                }

                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    response_data = response.json()
                    if "error" in response_data:
                        st.error(response_data["error"])
                    else:
                        st.session_state.diet_plan = response_data
                        st.success("✅ Diet Plan Generated!")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
        else:
            st.error("❌ Please fill in all profile details.")

with col2:
    if st.session_state.diet_plan and st.button("🔄 Get Alternative Plan"):
        st.session_state.alternative_requested = True
        with st.spinner("Generating an alternative diet plan..."):
            user_data = {
                "height": height,
                "weight": weight,
                "age": age,
                "gender": gender.lower(),
                "activity_level": activity_level.split(" (")[0].lower(),
                "work_hours": work_hours
            }
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": "AI Diet Consultant",
                "messages": [user_query or "Generate an alternative diet plan"],
                "allow_search": allow_web_search,
                "user_data": user_data,
                "request_alternative": True
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    st.session_state.diet_plan = response_data
                    st.success("✅ Alternative Plan Generated!")
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
            st.session_state.alternative_requested = False

# Display Diet Plan
if st.session_state.diet_plan:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🥗 Your Personalized Diet Plan")
    st.markdown(st.session_state.diet_plan, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
