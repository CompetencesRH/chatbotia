# Chatbot RH — API FastAPI + Groq

API REST d'un assistant RH basé sur LLaMA 3.1 via Groq, déployable sur Railway, Render ou tout hébergeur compatible Python.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Framework API | FastAPI |
| LLM | LLaMA 3.1 8B Instant (via Groq) |
| Client LLM | LangChain Groq |
| Serveur ASGI | Uvicorn |
| Validation | Pydantic |

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/CompetencesRH/chatbot-rh
cd chatbot-rh
```

### 2. Installer les dépendances

```bash
pip install fastapi uvicorn langchain-groq pydantic python-dotenv
```

### 3. Configurer la clé API Groq

Créez un fichier `.env` à la racine :

```env
GROQ_API_KEY=votre_clé_groq_ici
```

Obtenez votre clé sur [console.groq.com](https://console.groq.com).

---

## Lancement

```bash
python main.py
```

L'API est disponible sur `http://localhost:8000`.

---

## Endpoint

### `POST /chat`

Envoie un message à l'assistant RH et retourne une réponse.

**Request body :**

```json
{
  "message": "Comment réduire le turnover dans mon équipe ?"
}
```

**Response :**

```json
{
  "response": "Pour réduire le turnover, plusieurs leviers sont activables..."
}
```

**Erreurs :**

| Code | Raison |
|---|---|
| 400 | Message vide |
| 500 | Erreur LLM |

---

## CORS

L'API autorise les requêtes depuis :

- `https://competencesrh.fr`
- `https://www.competencesrh.fr`

Pour tester en local, ajoutez `http://localhost` à la liste `allow_origins` dans `main.py`.

---

## Comportement du modèle

Le système prompt limite le modèle aux sujets RH uniquement :

- IA & People Analytics
- Compétences et formation
- Management et engagement
- Recrutement et rétention

Toute question hors périmètre RH est ignorée ou redirigée.

---

## Déploiement

### Variables d'environnement requises

```env
GROQ_API_KEY=votre_clé_groq
PORT=8000  # optionnel, 8000 par défaut
```

### Railway / Render

1. Connectez votre repo GitHub
2. Ajoutez `GROQ_API_KEY` dans les variables d'environnement
3. Commande de démarrage : `python main.py`

---

## Structure du projet

```
.
├── main.py          # Application FastAPI
├── .env             # Variables d'environnement (ne pas committer)
├── .gitignore
└── README.md
```

---

## Améliorations possibles

- Ajouter un historique de conversation (mémoire multi-tours)
- Implémenter un RAG sur vos documents RH internes
- Ajouter une authentification par token
- Logger les échanges pour analyser les questions fréquentes

---

## Licence

MIT — [CompétencesRH](https://competencesrh.fr)
