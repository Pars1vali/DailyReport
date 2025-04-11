import os,logging
import aiogram

logging.getLogger().setLevel(logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = aiogram.Bot(token=BOT_TOKEN)

chat_id = "7405295017"

async def send_report(report: str):
    await bot.send_message(chat_id, report)