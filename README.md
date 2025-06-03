# telegram-alert-bot

## ภาพรวม
Service นี้ทำหน้าที่รับ HTTP request จาก go-backend (ผ่าน webhook) เพื่อ forward ข้อความแจ้งเตือนไปยังกลุ่ม Telegram ตามประเภทที่กำหนด (เติมเงิน, รีวิว, error logs ฯลฯ)

## โครงสร้างโฟลเดอร์

- **main.py**  
  – รับ request (เช่น `POST /alert`) จาก go-backend แล้วส่งต่อให้ `alert_handler.py`  

- **alert_handler.py**  
  – วิเคราะห์ประเภทของ Alert (เช่น coinเติมเงิน, review new, error) แล้วเรียกส่งข้อความตาม template ที่กำหนดใน `templates.py`  

- **access_control.py**  
  – ตรวจสอบว่า request ที่เข้ามามี GroupID/Token ถูกต้องหรือไม่ (security check)  

- **templates.py**  
  – เก็บฟังก์ชันฟอร์แมตข้อความแจ้งเตือน เช่น  
    ```python
    def format_coin_charge_alert(data): ...
    def format_review_alert(data): ...
    def format_error_alert(data): ...
    ```  

- **config.py**  
  – ตั้งค่า environment variables เช่น  
    ```python
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    ADMIN_GROUP_ID = os.getenv("TELEGRAM_ADMIN_GROUP_ID")
    REVIEW_GROUP_ID = os.getenv("TELEGRAM_REVIEW_GROUP_ID")
    ```  

- **Dockerfile / requirements.txt**  
  – ไลบรารีหลัก: `python-telegram-bot`, `fastapi` หรือ `flask` (ถ้าเลือกใช้เฟรมเวิร์กในการรัน server)  

## วิธีติดตั้งและรัน

1. ติดตั้ง dependencies  
   ```bash
   pip install -r requirements.txt
   ```  
2. ตั้งค่า environment variables  
   ```
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_ADMIN_GROUP_ID=...
   TELEGRAM_REVIEW_GROUP_ID=...
   ```  
3. รัน bot  
   ```bash
   python main.py
   ```  
