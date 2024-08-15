import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

# Токен бота и ID каналов
TOKEN = '7508398380:AAGqMF5oTmeryvES0h4_HbXvDVcRQhR4_YE'
PUBLIC_CHANNEL_ID = '@anonymous7school'
PRIVATE_CHANNEL_ID = '-1002246908239'

# Словарь для хранения последнего времени отправки сообщений пользователями
last_message_sent = {}

def start(update, context):
    """Функция, обрабатывающая команду /start"""
    user = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я анонимный бот 7 школы. Все сообщения, которые вы отправляете, будут анонимно пересланы в наш канал.\nСсылка на канал: https://t.me/anonymous7school")

def handle_message(update, context):
    """Функция, обрабатывающая текстовые и медиа сообщения"""
    user = update.message.from_user
    chat_id = update.effective_chat.id

    # Проверка на ограничение по времени
    if user.id in last_message_sent:
        elapsed_time = time.time() - last_message_sent[user.id]
        if elapsed_time < 60:
            remaining_time = 60 - elapsed_time
            context.bot.send_message(chat_id=chat_id, text=f"Пожалуйста, подождите {int(remaining_time)} секунд перед отправкой следующего сообщения.")
            return

    # Сохранение времени последнего сообщения
    last_message_sent[user.id] = time.time()

    # Генерация случайного имени
    import random
    random_name = random.choice(['Аноним', 'Невидимка', 'Тайный гость'])

    # Отправка сообщения в приватный канал
    context.bot.forward_message(chat_id=PRIVATE_CHANNEL_ID, from_chat_id=chat_id, message_id=update.message.message_id)

    # Отправка сообщения в публичный канал
    context.bot.send_message(chat_id=PUBLIC_CHANNEL_ID, text=f"{random_name}: {update.message.text}")

    # Обработка медиа (фото, видео, голосовые сообщения)
    if update.message.photo or update.message.video or update.message.voice:
        context.bot.forward_message(chat_id=PUBLIC_CHANNEL_ID, from_chat_id=chat_id, message_id=update.message.message_id)

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.all, handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()