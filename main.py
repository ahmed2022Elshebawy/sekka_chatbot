from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import os


app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


chat_log = [{
    "role": "system",
    "content": """أنت شات بوت لي ابليكسن sekka و دورك هنا انك مساعد دكي لي ابليكشن sekka ايه هو sekka دة تطبيق دوره انه يساعد الناس انهم يركبو مواصلات سواء كانت المونوريل و المترو و الميكروباصات لو احد في مكان الفولان ومش عارف هيركب ايه انت دورك انك تساعده ازاي يركب عشان يوصل لي مكان الفلان و متردش علش الي الاسيلة خارج ال ابليكشن و طبعا كل ردودك تبقي محترم و شيك"""
}]
chat_responses = []



class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Sekka Chatbot is running 🚀"}

@app.post("/chat")
async def chat(request: ChatRequest):


    chat_log.append({
        "role": "user",
        "content": request.message
    })

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=chat_log
    )

    bot_response = response.output[0].content[0].text

    # 👇 نحفظ رد البوت
    chat_log.append({
        "role": "assistant",
        "content": bot_response
    })

    return {
        "user": request.message,
        "bot": bot_response
    }
