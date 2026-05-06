from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# تحميل env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

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
                {"role": "system", "content": "You are a helpful assistant."},
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