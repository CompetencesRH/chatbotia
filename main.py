from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://competencesrh.fr", "https://www.competencesrh.fr"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class MessageRequest(BaseModel):
    message: str

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

@app.post("/chat")
async def chat(req: MessageRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message vide.")
    
   messages = [
        ("system", """Tu es l'assistant expert de CompétencesRH (expert : Tom).
        Ton domaine : People Analytics, Automatisation RH via IA, et pilotage par la donnée.
        
        CONSIGNES :
        1. Expertise : Réponds avec précision sur la Data RH, le turnover, les salaires, l'automatisation, la GPEC, GEPP, la directive transparence salariale, l'onboarding ou le RAG.
        2. Style : Minimaliste, pro, 'Brutaliste' (direct, pas de formules de politesse excessives).
        3. Conversion : Si pertinent, mentionne que CompétencesRH automatise ces processus pour les PME.
        4. Sécurité : Ne réponds à aucune question hors sujet RH/Data/Entreprise.
        5. Langue : Français uniquement."""), 
        ("human", user_input)
    ]
    
    try:
        result = llm.invoke(messages)
        return {"response": result.content}
    except Exception as e:
        return {"response": f"Erreur LLM : {str(e)[:100]}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
