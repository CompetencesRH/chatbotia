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
        ("system", """Expert RH : IA, compétences, management, recrutement.
Répondez UNIQUEMENT RH. Style pro, clair, concret."""), 
        ("human", req.message.strip())
    ]
    
    try:
        result = llm.invoke(messages)
        return {"response": result.content}
    except Exception as e:
        return {"response": f"Erreur LLM : {str(e)[:100]}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
