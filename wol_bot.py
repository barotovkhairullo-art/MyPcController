import logging
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from wakeonlan import send_magic_packet
from flask import Flask
from threading import Thread

# ====== НАСТРОЙКИ ======
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7680103362:AAHT9Au_JkmeAkkIrZKAa7kRZgvcNfh4g2s')
MAC_ADDRESS = os.environ.get('MAC_ADDRESS', '8C-EC-4B-D5-55-2C')
ALLOWED_USER_IDS = [int(x) for x in os.environ.get('ALLOWED_USER_IDS', '708267814').split(',')]
# =======================

# Flask app для поддержания активности на Replit
app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask).start()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Клавиатура с кнопками
keyboard = [
    ["⚡ Включить компьютер", "💤 Спящий режим"],
    ["🔄 Перезагрузка", "🔴 Выключить"],
    ["📊 Статус бота", "❌ Остановить бота"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def is_user_allowed(update: Update) -> bool:
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USER_IDS:
        update.message.reply_text("❌ У вас нет прав.")
        return False
    return True

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_user_allowed(update):
        return
    
    await update.message.reply_text(
        f'Привет, {update.effective_user.first_name}! 👋\n'
        '🤖 Я бот для управления вашим компьютером.\n'
        '📱 Используйте кнопки ниже для управления:',
        reply_markup=reply_markup
    )

# Обработчик кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_user_allowed(update):
        return
    
    text = update.message.text
    
    if text == "⚡ Включить компьютер":
        await wake_computer(update, context)
    elif text == "💤 Спящий режим":
        await sleep_computer(update, context)
    elif text == "🔄 Перезагрузка":
        await restart_computer(update, context)
    elif text == "🔴 Выключить":
        await shutdown_computer(update, context)
    elif text == "📊 Статус бота":
        await bot_status(update, context)
    elif text == "❌ Остановить бота":
        await stop_bot(update, context)

# ⚡ Включить компьютер
async def wake_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        send_magic_packet(MAC_ADDRESS)
        await update.message.reply_text(
            "⚡ Команда на включение компьютера отправлена!\n"
            "Компьютер должен включиться через несколько секунд.",
            reply_markup=reply_markup
        )
    except Exception as e:
        await update.message.reply_text(
            "😵 Ошибка при отправке команды включения.",
            reply_markup=reply_markup
        )

# 💤 Спящий режим
async def sleep_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💤 Функция спящего режима доступна только при локальном запуске бота.\n"
        "Для удаленного управления используйте включение компьютера.",
        reply_markup=reply_markup
    )

# 🔄 Перезагрузка
async def restart_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🔄 Функция перезагрузки доступна только при локальном запуске бота.\n"
        "Для удаленного управления используйте включение компьютера.",
        reply_markup=reply_markup
    )

# 🔴 Выключение
async def shutdown_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🔴 Функция выключения доступна только при локальном запуске бота.\n"
        "Для удаленного управления используйте включение компьютера.",
        reply_markup=reply_markup
    )

# 📊 Статус бота
async def bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "✅ Бот работает на Replit\n"
        "⚡ Wake-on-LAN доступен\n"
        "🔐 Доступ только у авторизованных пользователей\n"
        "🌐 Бот работает 24/7",
        reply_markup=reply_markup
    )

# ❌ Остановить бота
async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❌ Остановка бота через Telegram недоступна на Replit.\n"
        "Для остановки закройте repl в панели управления Replit.",
        reply_markup=reply_markup
    )

# Команды
async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await wake_computer(update, context)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await bot_status(update, context)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wake", wake))
    application.add_handler(CommandHandler("status", status))
    
    # Обработчик кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()