# This is Phase-2 of Ai Agent Development

#Step1: Setup Pydantic Model (Schema Validation)

from pydantic import BaseModel
from typing import List
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool



#Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent


app=FastAPI(title="LangGraph AI Agent")

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]
@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages[0] if isinstance(request.messages, list) else request.messages  # ✅ FIXED
    allow_search = request.allow_search
    provider = request.model_provider

    # Create AI Agent and get response
    response = get_response_from_ai_agent(llm_id, query, allow_search, provider)

    return response






#Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)