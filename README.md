# AI Chatbot Agent

AI Chatbot Agent is a web-based AI assistant built using **FastAPI** for the backend and **Streamlit** for the frontend. It supports multiple AI models, including **Groq's LLaMA-3 and Mixtral** and **OpenAI's GPT-4o-mini**, enabling users to interact with AI agents effectively.

## Features

✅ **Multi-Model Support**: Choose between Groq (LLaMA-3, Mixtral) and OpenAI (GPT-4o-mini).  
✅ **Custom AI Agents**: Define system prompts to customize agent behavior.  
✅ **Web-Based UI**: User-friendly interface built with Streamlit.  
✅ **Web Search Option**: Enable AI agents to fetch real-time web data.  
✅ **REST API Backend**: FastAPI handles chat interactions via a dedicated API endpoint.  
✅ **GitHub Integration**: Project is version-controlled and hosted on GitHub.  

## Installation

### Prerequisites
- Python 3.9+
- pip
- Git

### Clone the Repository
```bash
git clone https://github.com/Ikramullah89/AI-Chatbot-Agent.git
cd AI-Chatbot-Agent
```

### Create and Activate Virtual Environment
```bash
python -m venv myenv  # Create a virtual environment
source myenv/bin/activate  # On macOS/Linux
myenv\Scripts\activate  # On Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the FastAPI Backend
```bash
cd backend
uvicorn main:app --host 127.0.0.1 --port 9999 --reload
```

### Start the Streamlit Frontend
```bash
cd frontend
streamlit run frontend.py
```

## Usage
1. Open the Streamlit UI in your browser.
2. Define your AI agent’s behavior using system prompts.
3. Select an AI model (Groq/OpenAI).
4. Enter a user query and interact with the AI.
5. (Optional) Enable web search for real-time data retrieval.

## Contributing
Pull requests are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Create a Pull Request.



## Contact
For inquiries, contact **Ikramullah** via [LinkedIn]([https://www.linkedin.com/in/your-profile](https://www.linkedin.com/in/ikramullah-4736b5178/)) 
