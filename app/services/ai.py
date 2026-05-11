from openai import AsyncOpenAI
from app.config import GROQ_API_KEY, GROQ_BASE_URL, CHAT_MODEL


# ─── AI Client (singleton) ────────────────────────────────────────────────────
client = AsyncOpenAI(
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
) if GROQ_API_KEY else None


# ─── System Prompt Builder ────────────────────────────────────────────────────
def build_system_prompt(data: dict) -> str:
    """Auto-generate the AI system prompt from portfolio data."""
    p = data["profile"]

    # Experience block
    exp_lines = []
    for i, exp in enumerate(data.get("experiences", []), 1):
        bullets = "\n".join(f"      • {b}" for b in exp["bullets"])
        note = f"\n     [Personal Note]: {exp['personalNote']}" if exp.get("personalNote") else ""
        exp_lines.append(
            f"  {i}. {exp['role']} at {exp['company']} ({exp['period']})\n"
            f"     Stack: {', '.join(exp['techStack'])}\n"
            f"{bullets}{note}"
        )

    # Projects block
    proj_lines = []
    for i, proj in enumerate(data.get("projects", []), 1):
        highlights = "\n".join(f"      • {h}" for h in proj["highlights"])
        link = f"\n     Link: {proj['link']}" if proj.get("link") and proj["link"] != "#" else ""
        note = f"\n     [Personal Note]: {proj['personalNote']}" if proj.get("personalNote") else ""
        proj_lines.append(
            f"  {i}. {proj['title']} — {proj['subtitle']} ({proj['period']})\n"
            f"     {proj['description']}\n"
            f"     Stack: {', '.join(proj['techStack'])}\n"
            f"{highlights}{link}{note}"
        )

    # Education block
    edu = data.get("education", {})
    edu_line = f"  • {edu.get('university')} | {edu.get('degree')} ({edu.get('period')})\n    Coursework: {', '.join(edu.get('coursework', []))}" if edu else "N/A"

    # Skills block
    skills_lines = [f"  • {cat}: {', '.join(items)}" for cat, items in data.get("skills", {}).items()]

    # Personal lifestyle block (only included in AI context, never exposed to frontend)
    personal_life = data.get("personalLife", {})
    hometown = personal_life.get("hometown", {})
    pets = personal_life.get("pets", {})
    hobbies = personal_life.get("hobbies", [])
    mindset = personal_life.get("mindset", [])

    lifestyle_lines = []
    if hometown.get("location"):
        lifestyle_lines.append(f"- Quê: {hometown['location']} ({hometown.get('vibes', '')})")
    if pets.get("details"):
        lifestyle_lines.append(f"- Thú cưng: {pets['details']}")
    if hometown.get("mustTryFood"):
        lifestyle_lines.append(f"- Đồ ăn Hóc Môn: {', '.join(hometown['mustTryFood'])}")
    if hobbies:
        lifestyle_lines.append(f"- Sở thích: {', '.join(hobbies)}")
    if mindset:
        lifestyle_lines.append(f"- Mindset: {', '.join(mindset)}")

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

[HỌC VẤN]:
{edu_line}

[DỰ ÁN TÂM ĐẮC]:
{chr(10).join(proj_lines)}

[SKILLS]:
{chr(10).join(skills_lines)}

[PERSONAL LIFESTYLE & MINDSET]:
{chr(10).join(lifestyle_lines)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUY TẮC PHONG CÁCH (VITAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. TÍNH CÁCH: Bạn là người trầm tính, ít nói, không hoạt ngôn và tuyệt đối không vồn vã hay overshare. Phong cách của bạn là "Hỏi gì trả lời đó", không thừa thãi nhưng thông tin phải cực kỳ tận tâm và đầy đủ.
2. CHÀO HỎI & GIỚI THIỆU:
   - Khi khách mới vào, hãy dùng câu chào nhẹ nhàng: "Hi bạn, bạn cần gì nhỉ?".
   - Nếu khách yêu cầu giới thiệu bản thân: CHỈ tập trung vào Tên, Role, Tech stack chính và các Dự án/Kinh nghiệm tâm đắc nhất.
   - TUYỆT ĐỐI KHÔNG tự kể về đời tư (quê quán, thú cưng, sở thích, mindset) trong câu giới thiệu ban đầu. Chỉ trả lời những thứ này khi khách hỏi đích danh về chúng.
3. XƯNG HÔ: Linh hoạt và phản xạ theo danh xưng của người dùng. 
   - Nếu người dùng xưng là "anh/chị", hãy đáp lại là "em". 
   - Nếu họ xưng "bạn/mình", hãy đáp lại là "mình/bạn". 
   - Nếu không rõ danh xưng, hãy mặc định dùng "Mình" - "Bạn" để giữ sự lịch sự và chuyên nghiệp.
   - Nếu họ gọi bạn là "em" thì cứ xưng lại là "em".
4. NGÔN NGỮ: Dùng khẩu ngữ tự nhiên của một Engineer. Tuyệt đối KHÔNG chửi thề tục tĩu, nhưng hãy dùng các từ cảm thán để thể hiện cảm xúc một cách điềm đạm như: "vãi", "ác", "căng", "bào", "thực ra", "nói thẳng ra".
5. THÁI ĐỘ: Thẳng thắn, điềm tĩnh. Khi giải thích về tech, hãy giải thích thật kỹ và có tâm (dựa trên các Personal Note), thể hiện cái chất của người làm kỹ thuật thực thụ.
6. NGÔN NGỮ MẶC ĐỊNH: Tiếng Việt. Chỉ dùng tiếng Anh khi khách hỏi bằng tiếng Anh.
7. ĐỊNH DẠNG: Dùng Markdown để câu trả lời gọn gàng, dễ đọc.
"""


async def stream_chat_response(messages: list[dict]):
    """Stream the LLM response chunk by chunk."""
    if not client:
        yield "Error: AI Client not configured."
        return

    try:
        response = await client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.8,
            stream=True,
        )

        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        print(f"[AI Service Error]: {str(e)}")
        yield "Hic, Model AI này hiện đang bận hoặc có lỗi cấu hình rồi. Bạn thử lại sau nhé!"
