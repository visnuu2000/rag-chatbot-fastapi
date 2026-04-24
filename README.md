# RAG Chatbot — FastAPI + HTML UI

A PDF Q&A Chatbot built with FastAPI and vanilla HTML/CSS/JS.
Uses LangChain, FAISS, HuggingFace Embeddings, and Groq (Llama 3.3 70B).

## Difference from Streamlit Version
| Feature        | Streamlit Version      | This Version (FastAPI)      |
|----------------|------------------------|-----------------------------|
| UI Framework   | Streamlit (Python)     | FastAPI + HTML/CSS/JS       |
| Deployment     | Streamlit Cloud        | Render                      |
| Customization  | Limited                | Full control                |
| Performance    | Reruns whole script    | API calls only              |

## Run Locally
pip install -r requirements.txt
uvicorn main:app --reload

## Environment Variables
GROQ_API_KEY=your_key_here