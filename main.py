# main.py

import os
from fastapi import FastAPI, Request
from alert_handler import handle_alert

app = FastAPI()

@app.post("/alert")
async def alert_endpoint(request: Request):
    payload = await request.json()
    # เรียกฟังก์ชันจัดการ alert
    handle_alert(payload)
    # คืน 200 OK กลับไปยัง Go-Backend
    return {"status": "ok"}
