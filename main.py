from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
import os

# Charger .env en local (optionnel)
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

app = FastAPI()

llm = ChatGroq(
    model="llama-3.1.8b-instant",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)

class MessageRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: MessageRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message vide ou invalide.")

    try:
        messages = [
            ("system", "Vous êtes un expert en management des ressources humaines."),
            ("human", req.message)
        ]
        result = llm.invoke(messages)
        return {"response": result.content}
    except Exception as e:
        return {"response": "Erreur du serveur.", "error": str(e)}
