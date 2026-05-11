from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.portfolio import load_portfolio
from app.services.ai import client, build_system_prompt, stream_chat_response

router = APIRouter(tags=["AI"])


@router.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """AI chat endpoint. Returns a stream of text chunks."""
    if not client:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY is not configured on the server."
        )

    try:
        portfolio_data = load_portfolio()
        system_prompt = build_system_prompt(portfolio_data)

        api_messages = [{"role": "system", "content": system_prompt}]
        for msg in req.messages:
            role = "assistant" if msg.role == "ai" else "user"
            api_messages.append({"role": role, "content": msg.content})

        return StreamingResponse(
            stream_chat_response(api_messages),
            media_type="text/event-stream"
        )

    except Exception as e:
        print(f"[chat_endpoint] Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the response.")


@router.get("/health")
def health_check():
    """Lightweight health check for uptime monitors."""
    from app.services.portfolio import load_portfolio
    portfolio = load_portfolio()
    return {
        "status": "ok",
        "portfolio_owner": portfolio["profile"]["name"],
        "available": portfolio["profile"]["available"],
    }
