from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.competencesrh.fr"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


# --- Chat ---
class MessageRequest(BaseModel):
    message: str


@app.options("/chat")
def options_chat():
    return {}


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)


@app.post("/chat")
async def chat(req: MessageRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message vide.")

    messages = [
        ("system", "Vous êtes un expert en management des ressources humaines."),
        ("human", req.message)
    ]

    try:
        result = llm.invoke(messages)
        return {"response": result.content}
    except Exception as e:
        return {"response": "Erreur du serveur LLM.", "error": str(e)}
