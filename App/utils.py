from urllib.parse import parse_qs
from django.conf import settings
from telegram import Bot
from telegram.error import NetworkError
import time, hmac, hashlib, asyncio



# بررسی صحت هش دریافتی از تلگرام
def validate_telegram_hash(initdata):
    initdata = initdata[1:-1]     # اول و اخر متن '' اضافی داره
    
    data = parse_qs(initdata)     # query string -> dict
    if 'hash' not in data:
        return False

    expected_hash = data.pop('hash')[0]

    sorted_data = sorted(data.items())

    data_check_string = ''

    for key, value in sorted_data:
        data_check_string += f"{key}={value[0]}\n"
    
    data_check_string = data_check_string.rstrip('\n')     # اضافی \n حذف

    bot_token = settings.BOT_TOKEN

    secret_key = hmac.new('WebAppData'.encode('utf-8'), bot_token.encode('utf-8'), hashlib.sha256)

    calculated_hash = hmac.new(secret_key.digest(), data_check_string.encode('utf-8'), hashlib.sha256).hexdigest()

    return calculated_hash == expected_hash


# بررسی جدید بودن احراز هویت (حداکثر 10 دقیقه)
def is_recent_auth(auth_date, max_time_diff=600):
    try:
        current_time = int(time.time())

        return (current_time - int(auth_date)) < max_time_diff

    except ValueError:
        print("value error!")
        return False


#گرفتن پروفایل کاربر با استفاده از ایدی
async def get_profile_picture(telegram_id, retries=3):

    bot_token = settings.BOT_TOKEN
    bot = Bot(token=bot_token)
    for attempt in range(retries):
        try:
            profile_photos = await bot.get_user_profile_photos(user_id=telegram_id)

            picture_url = None
            if profile_photos and profile_photos.total_count > 0:
                # گرفتن آخرین عکس پروفایل با بالاترین کیفیت
                last_photo = profile_photos.photos[0][-1]
                file = await bot.get_file(file_id=last_photo.file_id)
                picture_url = file.file_path
            return picture_url  # برگرداندن URL عکس پروفایل
        
        except NetworkError:
            print(f"⚠️ تلاش مجدد ({attempt + 1}/{retries}) به دلیل TimeoutError...")
            await asyncio.sleep(1)
        
        except Exception as e:
            print(f"❌ خطا در دریافت عکس پروفایل: {e}")
            break  # در صورت بروز خطای دیگر از حلقه خارج می‌شود

    print("❌ خطا: همه تلاش‌ها برای دریافت عکس پروفایل ناموفق بود!")
    return None  # در صورت عدم موفقیت در همه تلاش‌ها، None برمی‌گردد