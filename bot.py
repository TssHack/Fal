import logging
import requests
import os
import random
from telethon import TelegramClient, events

# اطلاعات ربات
api_id = 25790571  # جایگزین کن
api_hash = "2b95fb1f6f630a83e0712e84ddb337f2"  # جایگزین کن
# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO)

# مقداردهی اولیه کلاینت
bot = TelegramClient('my_session', api_id, api_hash)

# تابع دریافت و ذخیره تصویر فال
def get_fal_image():
    url = "https://api.daradege.ir/faal"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # بررسی خطاهای HTTP

        # تولید نام فایل تصادفی
        random_number = random.randint(1000, 9999)
        file_path = f"fal_{random_number}.jpg"

        # ذخیره تصویر در فایل
        with open(file_path, "wb") as file:
            file.write(response.content)

        return file_path
    except requests.exceptions.RequestException as e:
        logging.error(f"خطا در دریافت فال: {e}")
        return None

# هندلر برای پیام "فال"
@bot.on(events.NewMessage(pattern=r"^فال$"))
async def send_fal(event):
    image_path = get_fal_image()
    if image_path:
        try:
            await bot.send_file(event.chat_id, image_path, caption="🔮 فال شما:")
        finally:
            os.remove(image_path)  # حذف فایل بعد از ارسال
    else:
        await event.reply("❌ خطایی در دریافت فال رخ داد. لطفاً دوباره امتحان کنید.")

# اجرای ربات
print("ربات فعال شد...")
bot.run_until_disconnected()
