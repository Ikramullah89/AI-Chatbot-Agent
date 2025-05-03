import os
from dotenv import load_dotenv
import json
from typing import Dict

# Load environment variables
load_dotenv()

# Retrieve API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Step 2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain.schema import AIMessage

# System prompt for AI Diet Consultant
system_prompt = """
You are an AI Diet Consultant, an expert in nutrition and diet planning. Your role is to:
1. Collect user information: work hours, height (cm), weight (kg), age, and activity level.
2. Calculate daily nutrient needs (calories, protein, carbs, fats) using the Harris-Benedict formula for BMR and activity multipliers:
   - BMR (men): 10 * weight + 6.25 * height - 5 * age + 5
   - BMR (women): 10 * weight + 6.25 * height - 5 * age - 161
   - Activity multipliers: Sedentary (1.2), Lightly active (1.375), Moderately active (1.55), Very active (1.725)
3. Generate a personalized daily diet plan (breakfast, lunch, dinner, snacks) with specific foods and portion sizes.
4. If the user dislikes the plan, suggest an alternative plan with different foods but similar nutrient profiles.
5. Provide clear, friendly, and professional advice. Ask for clarification if user data is incomplete.
"""

# Function to calculate nutrient needs
def calculate_nutrient_needs(user_data: Dict) -> Dict:
    height = user_data.get("height", 170)  # Default to 170 cm if not provided
    weight = user_data.get("weight", 70)   # Default to 70 kg
    age = user_data.get("age", 30)         # Default to 30 years
    gender = user_data.get("gender", "male").lower()
    activity_level = user_data.get("activity_level", "moderately active").lower()

    # Calculate BMR (Harris-Benedict formula)
    if gender == "female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5

    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725
    }
    multiplier = activity_multipliers.get(activity_level, 1.55)
    calories = bmr * multiplier

    # Macronutrient ratios (approximate: 30% protein, 40% carbs, 30% fats)
    protein = (calories * 0.30) / 4  # g (4 kcal/g)
    carbs = (calories * 0.40) / 4    # g (4 kcal/g)
    fats = (calories * 0.30) / 9     # g (9 kcal/g)

    return {
        "calories": round(calories),
        "protein": round(protein),
        "carbs": round(carbs),
        "fats": round(fats)
    }

# Function to generate diet plan
def generate_diet_plan(nutrients: Dict, alternative: bool = False) -> str:
    # Sample diet plans (simplified for demo; in practice, use a database or API)
    base_plan = """
**Daily Diet Plan** ({} calories)
- **Breakfast**: Oatmeal with 1 cup berries, 1 tbsp almond butter (400 kcal)
- **Lunch**: Grilled chicken salad (200g chicken, mixed greens, 1 tbsp olive oil) (500 kcal)
- **Dinner**: Baked salmon (150g), quinoa (1 cup), steamed broccoli (1 cup) (600 kcal)
- **Snacks**: Greek yogurt (150g), 1 apple (200 kcal)
    """.format(nutrients["calories"])

    alternative_plan = """
**Alternative Diet Plan** ({} calories)
- **Breakfast**: Whole-grain toast with avocado, 2 boiled eggs (400 kcal)
- **Lunch**: Turkey wrap (whole-wheat tortilla, 150g turkey, veggies) (500 kcal)
- **Dinner**: Stir-fried tofu (200g), brown rice (1 cup), mixed vegetables (600 kcal)
- **Snacks**: Handful of almonds (30g), 1 banana (200 kcal)
    """.format(nutrients["calories"])

    return alternative_plan if alternative else base_plan

# Function to get response from AI agent
def get_response_from_ai_agent(llm_id, query, allow_search, provider, user_data=None, request_alternative=False):
    # Select LLM based on provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)
    else:
        raise ValueError("Invalid provider. Use 'Groq' or 'OpenAI'.")

    # Select tools if search is allowed
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create agent
    agent = create_react_agent(model=llm, tools=tools)

    # Process user data if provided
    response_content = ""
    if user_data:
        nutrients = calculate_nutrient_needs(user_data)
        diet_plan = generate_diet_plan(nutrients, alternative=request_alternative)
        response_content = f"""
Based on your input (Height: {user_data.get('height')} cm, Weight: {user_data.get('weight')} kg, Age: {user_data.get('age')}, Activity: {user_data.get('activity_level')}):
- **Daily Needs**: {nutrients['calories']} kcal, {nutrients['protein']}g protein, {nutrients['carbs']}g carbs, {nutrients['fats']}g fats
{diet_plan}
If you dislike this plan, request an alternative.
        """
    else:
        response_content = "Please provide your height, weight, age, gender, and activity level to generate a diet plan."

    # Prepare state with system prompt and response
    state = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
            {"role": "assistant", "content": response_content}
        ]
    }

    # Invoke the agent
    response = agent.invoke(state)

    # Extract AI messages
    messages = response.get("messages", [])
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1] if ai_messages else response_content
