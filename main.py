# main.py

from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from telegram import Bot

# โหลดค่าจากไฟล์ .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_GROUP_ID = os.getenv("TELEGRAM_ADMIN_GROUP_ID")
REVIEW_GROUP_ID = os.getenv("TELEGRAM_REVIEW_GROUP_ID")

# สร้าง Bot instance
bot = Bot(token=TELEGRAM_TOKEN)

app = FastAPI()

@app.post("/alert")
async def receive_alert(request: Request):
    data = await request.json()
    alert_type = data.get("type", "unknown")
    message = f"มีการแจ้งเตือนประเภท: {alert_type}\nรายละเอียด: {data}"
    # ส่งข้อความไปกลุ่ม Admin
    try:
        await bot.send_message(chat_id=int(ADMIN_GROUP_ID), text=message)
    except Exception as e:
        return {"status": "failed", "error": str(e)}
    return {"status": "ok"}
