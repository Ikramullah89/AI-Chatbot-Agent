# Phase-2: AI Agent Backend

# Step 1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List, Dict, Optional

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool
    user_data: Optional[Dict] = None
    request_alternative: bool = False

# Step 2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

app = FastAPI(title="AI Diet Consultant API")

ALLOWED_MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the AI Diet Consultant.
    Processes user data and generates a personalized diet plan.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages[0] if isinstance(request.messages, list) else request.messages
    allow_search = request.allow_search
    provider = request.model_provider
    user_data = request.user_data
    request_alternative = request.request_alternative

    # Create AI Agent and get response
    response = get_response_from_ai_agent(
        llm_id=llm_id,
        query=query,
        allow_search=allow_search,
        provider=provider,
        user_data=user_data,
        request_alternative=request_alternative
    )

    return response

# Step 3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
