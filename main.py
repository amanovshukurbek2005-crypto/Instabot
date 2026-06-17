import logging
import re
import os
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8909904269:AAHITYbm06obIOb6Mby-zd2Hs60EeyNDffE"

def is_instagram_url(url):
    return bool(re.match(r'(https?://)?(www\.)?instagram\.com/(p|reel|tv)/[\w-]+', url))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Instagram reel havolasini yuboring!")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not is_instagram_url(url):
        await update.message.reply_text("❌ Instagram havolasi emas!")
        return
    msg = await update.message.reply_text("⏳ Yuklanmoqda...")
    output_path = f"video_{update.message.message_id}.mp4"
    ydl_opts = {'outtmpl': output_path, 'format': 'best[ext=mp4]/best', 'quiet': True}
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        with open(output_path, 'rb') as f:
            await update.message.reply_video(video=f)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Yuklab bo'lmadi.")
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND
