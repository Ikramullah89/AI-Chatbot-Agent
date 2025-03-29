# Phase-1: AI Agent Creation

import os
from dotenv import load_dotenv

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

# System prompt
system_prompt = "Act as an AI Chatbot who is smart and friendly."

# Function to get response from AI agent
def get_response_from_ai_agent(llm_id, query, allow_search, provider):
    # Select LLM based on provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)
    else:
        raise ValueError("Invalid provider. Use 'Groq' or 'OpenAI'.")

    # Select tools if search is allowed
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # ✅ Fix: Corrected `create_react_agent` usage (removed `state_modifier`)
    agent = create_react_agent(model=llm, tools=tools)

    # Prepare state with system prompt and user query
    state = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    }

    # Invoke the agent
    response = agent.invoke(state)

    # Extract AI messages
    messages = response.get("messages", [])
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1] if ai_messages else "No response from AI."

# ✅ Fix: Now calling the function correctly
query = "Who is the founder of Pakistan?"
ai_response = get_response_from_ai_agent(llm_id="llama3-70b-8192", query=query, allow_search=True, provider="Groq")

# Print AI response
print(ai_response)
