from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# تحميل Environment Variables
load_dotenv()

# قراءة API Key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

# إنشاء OpenAI Client
client = OpenAI(api_key=api_key)

# إنشاء FastAPI App
app = FastAPI()

# رسالة النظام
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """
أنت شات بوت لتطبيق Sekka ودورك هنا أنك مساعد ذكي لتطبيق Sekka.

تطبيق Sekka يساعد الناس في معرفة المواصلات المناسبة مثل:
- المترو
- المونوريل
- الميكروباصات

إذا كان المستخدم في مكان معين ولا يعرف كيف يصل إلى وجهته،
ساعده بطريقة واضحة وبسيطة ومحترمة.

لا ترد على أي أسئلة خارج نطاق المواصلات أو التطبيق.
"""
}

# سجل المحادثة
chat_log = [SYSTEM_MESSAGE]


# شكل البيانات القادمة من المستخدم
class ChatRequest(BaseModel):
    message: str


# Route رئيسي للتأكد أن السيرفر شغال
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Sekka Chatbot is running 🚀"
    }


# Route الشات
@app.post("/chat")
async def chat(request: ChatRequest):
    global chat_log

    try:
        # إضافة رسالة المستخدم
        chat_log.append({
            "role": "user",
            "content": request.message
        })

        # استدعاء OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_log
        )

        # استخراج الرد
        bot_response = response.choices[0].message.content

        # حفظ الرد
        chat_log.append({
            "role": "assistant",
            "content": bot_response
        })

        # إرسال الرد
        return {
            "success": True,
            "user": request.message,
            "bot": bot_response
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# تشغيل السيرفر محليًا
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )