import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ───────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
PORTFOLIO_FILE = BASE_DIR / "portfolio.json"

# ─── API Keys ────────────────────────────────────────
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama-3.3-70b-versatile")

# ─── CORS ────────────────────────────────────────────
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in raw_origins.split(",") if o.strip()]
