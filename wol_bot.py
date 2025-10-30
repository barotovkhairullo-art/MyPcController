import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from wakeonlan import send_magic_packet

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "7680103362:AAHT9Au_JkmeAkkIrZKAa7kRZgvcNfh4g2s"
MAC_ADDRESS = "8C-EC-4B-D5-55-2C"
ALLOWED_USER_IDS = [708267814]
# =======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ Доступ запрещен")
        return
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}!\n"
        "Я бот для включения компьютера.\n"
        "Команда: /wake"
    )

async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    try:
        send_magic_packet(MAC_ADDRESS)
        await update.message.reply_text("⚡ Команда на включение компьютера отправлена!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

if __name__ == '__main__':
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wake", wake))
    application.run_polling()
