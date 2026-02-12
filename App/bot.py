from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings
from telegram.ext import ContextTypes

async def handle_start_command(update: Update):
    bot_token = settings.BOT_TOKEN
    bot = Bot(token=bot_token)

    name = update.effective_user.full_name

        
    link = f"https://t.me/DuClick_bot/?startapp"   # تا جایی که یادمه اینجوری اگه رفرال بفرستی با چیزی به این حالت در میومد : start_param

    message = (
        f"کاربر {name} سلام! 👋\n"
        "برای دسترسی به مینی اپ روی دکمه زیر کلیک کنید. 🚀"
    )

    button = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                text="ورود به مینی اپ",
                # web_app=WebAppInfo(url=link)
                url=link
                )
            ]
        ]
    )
    chat_id = update.message.chat.id

    await bot.send_message(chat_id=chat_id, text=message, reply_markup=button, reply_to_message_id=update.message.message_id)


async def handle_support_command(update: Update):
    bot_token = settings.BOT_TOKEN
    bot = Bot(token=bot_token)

    message = """
💪 اگه ربات رو دوست داری و می‌خوای به ما کمک کنی…
هر مبلغی دلت می‌خواد به این کارت‌ها واریز کن:

6037997117978735 | سید امیرحسینی بانک ملی
6219861935462704 | مصطفی شکفته بانک سامان

با هر کمک تو تیم توسعه دهنده ربات انرژی می‌گیره که رباتو خفن‌تر کنه! ⚡🚀
"""
    chat_id = update.message.chat.id
    await bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=update.message.message_id)


async def handle_unknown_command(update: Update):
    bot_token = settings.BOT_TOKEN
    bot = Bot(token=bot_token)

    chat_id = update.message.chat.id

    help_message = (
        "دستور شما قابل فهم نیست.\n"
        "برای شروع از دستور /start استفاده کنید تا به لینک مورد نظر هدایت شوید."
    )

    await bot.send_message(chat_id=chat_id, text=help_message, reply_to_message_id=update.message.message_id)