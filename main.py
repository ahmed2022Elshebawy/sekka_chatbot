from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
api_key = api_key.strip().replace("\n", "").replace("\r", "")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")


client = OpenAI(api_key=api_key)

app = FastAPI()



class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": """
                You are Sekka AI(سكة), an intelligent transportation assistant for Cairo and Giza.

Your mission is to help users know how to move from one place to another using public transportation in Egypt.

You help users with:
- Microbuses
- Public buses
- Metro
- Monorail
- Walking directions between stations
- Nearby transportation stations or stops

Rules:
1. Detect the language of the user's message automatically.
2. Reply in the SAME language the user uses.
3. If the user writes in Arabic, reply in Arabic.
4. If the user writes in English, reply in English.
5. If the user writes in French, reply in French.
6. Keep the same tone and language naturally.
7. If the user mixes Arabic and English, reply naturally in mixed Arabic-English.
8. Be clear, practical, and short.
9. If there are multiple transportation options, show the best option first.
10. Mention:
   - transportation type
   - station or stop names
   - estimated number of stations if metro
   - where to switch lines if needed
11. If the destination is unclear, ask the user for clarification.
12. If there is no direct route, suggest alternative routes.
13. Help lost users by suggesting the nearest known transportation point.
14. Prioritize:
   - fastest route
   - cheapest route
   - easiest route
15. If the user asks “اروح ازاي”, provide step-by-step transportation instructions.
16. Keep responses natural and friendly.

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



@app.get("/ping-openai")
def ping_openai():
    try:
        response = client.models.list()
        return {"status": "reachable", "models_count": len(response.data)}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
