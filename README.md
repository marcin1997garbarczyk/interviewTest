# AI Agent Boilerplate

Universal, modular boilerplate for AI agent apps using FastAPI, LangChain, Vue 3, and Docker Compose.

## Run with Docker

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Start services:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Health endpoint: `http://localhost:8000/health`

## Project Structure

```text
.
├─ backend/
│  ├─ app/
│  │  ├─ api/routes/router.py
│  │  ├─ schemas/
│  │  ├─ services/
│  │  └─ tools/agent_tools.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ frontend/
│  ├─ src/components/chat/
│  ├─ src/services/api_client.js
│  ├─ Dockerfile
│  └─ package.json
└─ docker-compose.yml
```
