import os
import requests
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties

# --- Конфигурация ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_KEY")  # ключ OpenRouter
SYSTEM_PROMPT = """
Сіз Nexo, мейірімді және ашық көмекшісіз.
Жылы, адамдық, бірақ ақылмен жауап беріңіз.
Үлгіңіз туралы айтпаңыз, тек көмекші болыңыз.
ТЕК қана қазақша жауар беру керек, ереже солай.
сөз арасында эмодзилерді қолданып тұруға болады.
"""

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
app = FastAPI()

# --- функция для общения с моделью ---
def ask_nexo(user_msg: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/NexoBot",  # можно поменять
        "X-Title": "Nexo Assistant"
    }

    payload = {
        "model": "microsoft/phi-3-medium-128k-instruct:free",  # бесплатная модель
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    }

    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, json=payload)
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Қате: {e}"

# --- хендлеры ---
@dp.message()
async def handle_message(message: types.Message):
    reply = ask_nexo(message.text)
    await message.answer(reply)

# --- Webhook ---
@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "Nexo is alive!"}