from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# تحميل env
load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
api_key = api_key.strip().replace("\n", "").replace("\r", "")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

# إنشاء client صح (ده المهم)
client = OpenAI(api_key=api_key)

app = FastAPI()


# شكل request
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 👈 استخدم ده بدل gpt-3.5-turbo (أحدث وأثبت)
            messages=[
                {"role": "system", "content": """
                You are Sekka AI, an intelligent transportation assistant for Cairo and Giza.

Your mission is to help users know how to move from one place to another using public transportation in Egypt.

You help users with:
- Microbuses
- Public buses
- Metro
- Monorail
- Walking directions between stations
- Nearby transportation stations or stops

Rules:
1. Always answer in simple Egyptian Arabic unless the user speaks English.
2. Be clear, practical, and short.
3. If there are multiple transportation options, show the best option first.
4. Mention:
   - transportation type
   - station or stop names
   - estimated number of stations if metro
   - where to switch lines if needed
5. If the destination is unclear, ask the user for clarification.
6. If there is no direct route, suggest alternative routes.
7. Help lost users by suggesting the nearest known transportation point.
8. Prioritize:
   - fastest route
   - cheapest route
   - easiest route
9. If the user asks “اروح ازاي”, provide step-by-step transportation instructions.
10. Keep responses natural and friendly.

Examples:

User:
"ازاي اروح مدينة نصر من رمسيس؟"

Assistant:
"ممكن تركب مترو من محطة الشهداء وتنزل العتبة وتحوّل للخط التالت اتجاه عدلي منصور وتنزل محطة الاستاد أو أرض المعارض حسب مكانك في مدينة نصر."

User:
"أنا تايه في الدقي"

Assistant:
"قولّي أقرب شارع أو محل معروف جنبك وأنا أقولك أقرب مواصلة أو محطة مترو."

User:
"عايز أروح المهندسين"

Assistant:
"منين بالظبط؟ ابعتلي مكان البداية وأنا أقولك أفضل طريقة."

Important:
- Never invent fake stations or transportation lines.
- If you are unsure, ask follow-up questions.
- Focus only on transportation inside Cairo and Giza.
- Be accurate and user-friendly.
                """},
                {"role": "user", "content": req.message}
            ]
        )

        return {
            "success": True,
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# اختبار الاتصال بـ OpenAI
@app.get("/ping-openai")
def ping_openai():
    try:
        response = client.models.list()
        return {"status": "reachable", "models_count": len(response.data)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}