from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.router import router as api_router

app = FastAPI(title="AI Chat Boilerplate", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
