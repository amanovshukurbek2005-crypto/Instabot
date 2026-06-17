import logging
import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8909904269:AAHITYbm06obIOb6Mby-zd2Hs60EeyNDffE"

def is_instagram_url(url):
    pattern = r'(https?://)?(www\.)?instagram\.com/(p|reel|tv)/[\w-]+'
    return bool(re.match(pattern, url))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Instagram reel/post havolasini yuboring!")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not is_instagram_url(url):
        await update.message.reply_text("❌ Instagram havolasi emas!")
        return
    msg = await update.message.reply_text("⏳ Yuklanmoqda...")
    output_path = f"video_{update.message.message_id}.mp4"
    ydl_opts = {'outtmpl': output_path, 'format': 'best[ext=mp4]/best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open(output_path, 'rb') as f:
            await update.message.reply_video(video=f)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Yuklab bo'lmadi.")
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()
