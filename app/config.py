import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ───────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
PORTFOLIO_FILE = BASE_DIR / "portfolio.json"

# ─── API Keys ────────────────────────────────────────
GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
GITHUB_BASE_URL = "https://models.inference.ai.azure.com"
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")

# ─── CORS ────────────────────────────────────────────
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in raw_origins.split(",") if o.strip()]
