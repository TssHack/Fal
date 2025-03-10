import logging
import requests
import os
import random
from telethon import TelegramClient, events

# اطلاعات ورود (از my.telegram.org بگیر)
api_id = 25790571  # جایگزین کن
api_hash = "2b95fb1f6f630a83e0712e84ddb337f2"  # جایگزین کن
phone_number = "+98XXXXXXXXXX"  # شماره تلفن خودت

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO)

# مقداردهی اولیه کلاینت مخصوص اکانت شخصی
client = TelegramClient("my_session", api_id, api_hash)

async def main():
    await client.start(phone_number)  # ورود به اکانت شخصی
    print("✅ اکانت شخصی شما متصل شد!")

# تابع دریافت و ذخیره تصویر فال
def get_fal_image():
    url = "https://api.daradege.ir/faal"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # بررسی خطاهای HTTP
        
        # بررسی نوع محتوا
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            logging.error("❌ محتوای دریافتی تصویر نیست!")
            return None

        # تولید نام فایل تصادفی
        file_path = f"fal_{random.randint(1000, 9999)}.jpg"

        # ذخیره تصویر
        with open(file_path, "wb") as file:
            file.write(response.content)

        return file_path
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ خطا در دریافت فال: {e}")
        return None

# هندلر برای پیام "فال"
@client.on(events.NewMessage(pattern=r"^فال$"))
async def send_fal(event):
    image_path = get_fal_image()
    if image_path:
        try:
            # ارسال تصویر به صورت ریپلای به پیام کاربر
            await event.reply("🔮 فال شما:", file=image_path)
        except Exception as e:
            logging.error(f"❌ خطا در ارسال تصویر: {e}")
            await event.reply("❌ خطایی در ارسال تصویر فال رخ داد.")
        finally:
            os.remove(image_path)  # حذف فایل بعد از ارسال
    else:
        await event.reply("❌ خطایی در دریافت فال رخ داد. لطفاً دوباره امتحان کنید.")

# اجرای ربات با اکانت شخصی
async def run_client():
    await client.start(phone_number)  # ورود به اکانت شخصی
    print("📢 ربات آماده دریافت پیام است...")
    await client.run_until_disconnected()  # اجرای ربات و انتظار برای پیام‌ها

# اجرای ربات در حالت non-blocking
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_client())
