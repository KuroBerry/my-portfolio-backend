from fastapi import APIRouter
from app.services.portfolio import get_public_portfolio

router = APIRouter(prefix="/api", tags=["Portfolio"])


@router.get("/portfolio")
def get_portfolio():
    """Return public portfolio data to the frontend."""
    return get_public_portfolio()
