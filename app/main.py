from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.routers import portfolio, chat

app = FastAPI(title="Portfolio AI Backend")

# ─── CORS ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ─────────────────────────────────────────
app.include_router(portfolio.router)
app.include_router(chat.router)
