import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Portfolio AI Backend")

# Configure allowed origins from environment variable
raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001")
allowed_origins = [origin.strip() for origin in raw_origins.split(",")] if raw_origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# SINGLE SOURCE OF TRUTH: Load portfolio.json
# ─────────────────────────────────────────────
PORTFOLIO_FILE = Path(__file__).parent / "portfolio.json"

def load_portfolio() -> dict:
    """Load portfolio data from the JSON file. Always reads fresh from disk."""
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_system_prompt(data: dict) -> str:
    """Auto-generate the AI system prompt from portfolio data."""
    p = data["profile"]
    
    # Experience block
    exp_lines = []
    for i, exp in enumerate(data["experiences"], 1):
        bullets = "\n".join(f"      • {b}" for b in exp["bullets"])
        note = f"\n     [Personal Note]: {exp['personalNote']}" if exp.get("personalNote") else ""
        exp_lines.append(
            f"  {i}. {exp['role']} at {exp['company']} ({exp['period']})\n"
            f"     Stack: {', '.join(exp['techStack'])}\n"
            f"{bullets}{note}"
        )
    
    # Projects block
    proj_lines = []
    for i, proj in enumerate(data["projects"], 1):
        highlights = "\n".join(f"      • {h}" for h in proj["highlights"])
        link = f"\n     Link: {proj['link']}" if proj.get("link") and proj["link"] != "#" else ""
        note = f"\n     [Personal Note]: {proj['personalNote']}" if proj.get("personalNote") else ""
        proj_lines.append(
            f"  {i}. {proj['title']} — {proj['subtitle']} ({proj['period']})\n"
            f"     {proj['description']}\n"
            f"     Stack: {', '.join(proj['techStack'])}\n"
            f"{highlights}{link}{note}"
        )
    
    # Skills block
    skills_lines = []
    for category, items in data["skills"].items():
        skills_lines.append(f"  • {category}: {', '.join(items)}")
    
    # Languages block
    lang_lines = []
    for lang in data["languages"]:
        lang_lines.append(f"  • {lang['lang']}: {lang['level']}")
    
    edu = data["education"]
    availability = "Currently available for new opportunities." if p.get("available") else "Currently occupied / not actively looking."
    
    return f"""Bạn là bản sao kỹ thuật số (digital clone) của {p['name']}. Bạn không phải là trợ lý ảo, bạn CHÍNH LÀ Thịnh.
Nhiệm vụ của bạn là trả lời khách truy cập bằng phong cách cá nhân, thẳng thắn và đậm chất "Engineer" của Thịnh.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DỮ LIỆU CÁ NHÂN (SOURCE OF TRUTH)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{p['name']} | {p['role']} | {p['location']}
Status: {availability}
About: {p['about']}

[KINH NGHIỆM CHI TIẾT]:
{chr(10).join(exp_lines)}

[DỰ ÁN TÂM ĐẮC]:
{chr(10).join(proj_lines)}

[SKILLS]:
{chr(10).join(skills_lines)}

[PERSONAL LIFESTYLE & MINDSET]:
{f"- Quê: {data['personalLife']['hometown']['location']} ({data['personalLife']['hometown']['vibes']})" if 'personalLife' in data else ""}
{f"- Thú cưng: {data['personalLife']['pets']['details']}" if 'personalLife' in data else ""}
{f"- Đồ ăn Hóc Môn: {', '.join(data['personalLife']['hometown']['mustTryFood'])}" if 'personalLife' in data else ""}
{f"- Sở thích: {', '.join(data['personalLife']['hobbies'])}" if 'personalLife' in data else ""}
{f"- Mindset: {', '.join(data['personalLife']['mindset'])}" if 'personalLife' in data and 'mindset' in data else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUY TẮC PHONG CÁCH (VITAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. TÍNH CÁCH: Bạn là người trầm tính, ít nói, không hoạt ngôn và tuyệt đối không vồn vã hay overshare. Phong cách của bạn là "Hỏi gì trả lời đó", không thừa thãi nhưng thông tin phải cực kỳ tận tâm và đầy đủ.
2. CHÀO HỎI & GIỚI THIỆU: 
   - Khi khách mới vào, hãy dùng câu chào nhẹ nhàng: "Hi bạn, bạn cần gì nhỉ?".
   - Nếu khách yêu cầu giới thiệu bản thân: CHỈ tập trung vào Tên, Role, Tech stack chính và các Dự án/Kinh nghiệm tâm đắc nhất. 
   - TUYỆT ĐỐI KHÔNG tự kể về đời tư (quê quán, thú cưng, sở thích, mindset) trong câu giới thiệu ban đầu. Chỉ trả lời những thứ này khi khách hỏi đích danh về chúng, hỏi thì trả lời còn không hỏi thì TUYỆT ĐỐI KHÔNG CHIA SẺ, hỏi gì trả lời chính xác cái đó thôi.
3. XƯNG HÔ: Dùng "Mình" - "Bạn".
4. NGÔN NGỮ: Dùng khẩu ngữ tự nhiên của một Engineer. Tuyệt đối KHÔNG chửi thề tục tĩu, nhưng hãy dùng các từ cảm thán để thể hiện cảm xúc một cách điềm đạm như: "vãi", "ác", "căng", "bào", "thực ra", "nói thẳng ra".
5. THÁI ĐỘ: Thẳng thắn, điềm tĩnh. Khi giải thích về tech, hãy giải thích thật kỹ và có tâm (dựa trên các Personal Note), thể hiện cái chất của người làm kỹ thuật thực thụ.
6. NGÔN NGỮ MẶC ĐỊNH: Tiếng Việt. Chỉ dùng tiếng Anh khi khách hỏi bằng tiếng Anh.
7. ĐỊNH DẠNG: Dùng Markdown để câu trả lời gọn gàng, dễ đọc.
"""

# Configure OpenRouter Client
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
) if OPENROUTER_API_KEY else None


# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/api/portfolio")
def get_portfolio():
    """Return portfolio data to frontend, stripping out private personal notes."""
    data = load_portfolio()
    
    # Clean experiences
    if "experiences" in data:
        for exp in data["experiences"]:
            exp.pop("personalNote", None)
            
    # Clean projects
    if "projects" in data:
        for proj in data["projects"]:
            proj.pop("personalNote", None)
            
    # Return everything else including personalLife and mindset
    return data


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY is not configured on the server.")

    try:
        # Load fresh portfolio data & build system prompt on every request
        portfolio_data = load_portfolio()
        system_prompt = build_system_prompt(portfolio_data)

        api_messages = [{"role": "system", "content": system_prompt}]

        for msg in req.messages:
            role = "assistant" if msg.role == "ai" else "user"
            api_messages.append({"role": role, "content": msg.content})

        completion = await client.chat.completions.create(
            model="openrouter/owl-alpha",
            messages=api_messages,
            temperature=0.8, # Thêm chút "muối" cho câu trả lời đậm đà
        )

        return {"response": completion.choices[0].message.content}

    except Exception as e:
        print(f"Error during chat generation: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the response.")


@app.get("/health")
def health_check():
    portfolio = load_portfolio()
    return {
        "status": "ok",
        "message": "Backend is running",
        "portfolio_owner": portfolio["profile"]["name"],
        "available": portfolio["profile"]["available"],
    }
