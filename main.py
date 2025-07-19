import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

# گرفتن توکن از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک یا اسم آهنگتو بفرست تا برات MP3 بفرستم 🎵")

# پردازش پیام‌های کاربر
async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("در حال جستجو و دانلود آهنگ... ⏳")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            await update.message.reply_audio(audio=open(filename, 'rb'), title=info.get('title'))
            os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"خطا در دانلود آهنگ: {str(e)}")

# اجرای ربات
if __name__ == '__main__':
    if not TOKEN:
        print("❌ توکن ربات تعریف نشده!")
        exit()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_music))

    print("✅ ربات با موفقیت اجرا شد.")
    app.run_polling()