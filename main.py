from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# الرسالة المبدئية للنظام
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """أنت شات بوت لتطبيق Sekka ودورك هنا أنك مساعد ذكي لتطبيق Sekka. تطبيق Sekka هو تطبيق دوره يساعد الناس أنهم يركبوا مواصلات سواء كانت المونوريل، المترو، والميكروباصات. إذا كان أحد في مكان معين ولا يعرف كيف يركب ليصل إلى مكانه، دورك هو أن تساعده. لا ترد على أي أسئلة خارج نطاق التطبيق. كل ردودك يجب أن تكون محترمة وشيك."""
}

# قائمة المحادثات (للتجربة)
chat_log = [SYSTEM_MESSAGE]


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Sekka Chatbot is running 🚀"}


@app.post("/chat")
async def chat(request: ChatRequest):
    global chat_log

    # نضيف رسالة المستخدم
    chat_log.append({
        "role": "user",
        "content": request.message
    })

    try:
        # استدعاء OpenAI API بالطريقة الصحيحة
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # الموديل الصحيح
            messages=chat_log
        )

        # قراءة الرد بالشكل السليم
        bot_response = response.choices[0].message.content

        # نحفظ رد البوت
        chat_log.append({
            "role": "assistant",
            "content": bot_response
        })

        return {
            "user": request.message,
            "bot": bot_response
        }

    except Exception as e:
        return {"error": str(e)}, 500


# تشغيل السيرفر يكون في نهاية الملف
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)