# alert_handler.py

import os
import requests
from typing import Any, Dict

# ดึงค่าจาก .env
ADMIN_CHAT_ID = int(os.getenv("TELEGRAM_GROUP_ID_ADMIN", "0"))
SEER_CHAT_ID = int(os.getenv("TELEGRAM_GROUP_ID_SEER", "0"))
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# ฟังก์ชันส่งข้อความเข้า Telegram
def send_telegram_message(chat_id: int, text: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"  # ถ้าอยากใช้ Markdown ในข้อความ
    }
    resp = requests.post(url, json=payload)
    print(f"sendMessage status={resp.status_code}, response={resp.text}")


# ฟังก์ชันหลักในการจัดการ alert แต่ละประเภท
def handle_alert(payload: Dict[str, Any]) -> None:
    """
    payload ตัวอย่าง:
    {"type":"coin_topup","data":{"userId":"abc123","amount":100}}
    {"type":"booking_request","data":{"userId":"abc123","seerId":"seer456","slot":"2025-06-10T14:00"}}
    """
    t = payload.get("type")
    d = payload.get("data", {})

    # เติมเงิน – แจ้ง Admin group
    if t == "coin_topup":
        user_id = d.get("userId")
        amount = d.get("amount")
        if user_id is None or amount is None:
            print("coin_topup payload missing userId or amount")
            return

        text = f"💰 *เติมเหรียญสำเร็จ*\nUser `{user_id}` เติมเหรียญจำนวน *{amount}* เหรียญ"
        send_telegram_message(ADMIN_CHAT_ID, text)
        return

    # คิวดูดวง (Booking) – แจ้ง Seer group
    if t == "booking_request":
        user_id = d.get("userId")
        seer_id = d.get("seerId")
        slot = d.get("slot")
        if user_id is None or seer_id is None or slot is None:
            print("booking_request payload missing userId, seerId, or slot")
            return

        text = (
            "🔔 *คำขอดูดวงใหม่*\n"
            f"User `{user_id}` ขอจองคิวดูดวงกับ Seer `{seer_id}`\n"
            f"ช่วงเวลา: `{slot}`"
        )
        send_telegram_message(SEER_CHAT_ID, text)
        return

    # ถ้ามีประเภทอื่นๆ เพิ่ม elif ได้เลย
    # elif t == "another_type":
    #     ...

    print(f"Unhandled alert type: {t}")
