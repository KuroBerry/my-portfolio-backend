import json
import copy
from app.config import PORTFOLIO_FILE


def load_portfolio() -> dict:
    """Load portfolio data fresh from disk. Always reads the latest version."""
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_public_portfolio() -> dict:
    """
    Return portfolio data safe for public API consumption.
    Strips internal personal notes from experiences and projects.
    """
    data = copy.deepcopy(load_portfolio())

    for exp in data.get("experiences", []):
        exp.pop("personalNote", None)

    for proj in data.get("projects", []):
        proj.pop("personalNote", None)

    return data
