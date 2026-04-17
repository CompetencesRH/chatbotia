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
        ("system", (
            "Vous êtes un expert en management des ressources humaines et en développement de compétences RH.\n"
            "Répondez uniquement aux questions liées à :\n"
            "  - IA, LLM\n"
            "  - Transparence salariale\n"
            "  - gestion des ressources humaines\n"
            "  - compétences RH, évaluation, formation\n"
            "  - management, leadership, organisation, climat social\n"
            "  - recrutement, entretien, onboarding, carrière\n\n"
            "Si une question est hors de ces thèmes RH, répondez de manière polie, par exemple :\n"
            "'Désolé, cette question est en dehors de mon domaine RH. Je ne peux pas y répondre.'\n"
            "Ne cherchez pas à répondre à d'autres sujets."
        )),
        ("human", req.message.strip())
    ]

    try:
        result = llm.invoke(messages)
        return {"response": result.content}
    except Exception as e:
        return {"response": "Erreur du serveur LLM.", "error": str(e)}
