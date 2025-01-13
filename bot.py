import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from dotenv import load_dotenv
import os
import logging
import sqlite3
import re
import random
from datetime import timedelta

load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not API_TOKEN:
    raise ValueError("Не указан TELEGRAM_API_TOKEN. Проверьте файл .env.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
logging.info("Бот запущен с безопасным хранением токена.")

COMMAND_PREFIXES = ["Бот ", "бот ", "Bot ", "bot "]  # Уникальные префиксы

BAD_WORDS = [
    "блядь", "сука", "пизда", "хуй", "ебать", "еблан", "хер", "тварь", "мудила", "дрочить", 
    "пидор", "пиздец", "шлюха", "сучка", "гондон", "педик", "гандон", "хуета", "охуеть", 
    "нахуй", "ебаный", "срака", "пидорас", "тупая", "дура", "ебучий", "мудрец", "урод", 
    "пошел нахуй", "блядь", "чмо", "похуй", "сосать", "уродка", "петух", "долбоеб", "козел",
    "сучий", "курва", "пиздатый", "сука блять", "пиздатина", "херовина", "мать твою", "пиздин", 
    "ебало", "сучар", "пиздюк", "педик", "дерьмо", "говно", "долбанутый", "ублюдок", "все хреново",
    "Блядь", "Сука", "Пизда", "Хуй", "Ебать", "Еблан", "Хер", "Тварь", "Мудила", "Дрочить", 
    "Пидор", "Пиздец", "Шлюха", "Сучка", "Гондон", "Педик", "Гандон", "Хуета", "Охуеть", 
    "Нахуй", "Ебаный", "Срака", "Пидорас", "Тупая", "Дура", "Ебучий", "Мудрец", "Урод", 
    "Пошел нахуй", "Блядь", "Чмо", "Похуй", "Сосать", "Уродка", "Петух", "Долбоеб", "Козел",
    "Сучий", "Курва", "Пиздатый", "Сука Блять", "Пиздатина", "Херовина", "Мать Твою", "Пиздин", 
    "Ебало", "Сучар", "Пиздюк", "Педик", "Дерьмо", "Говно", "Долбанутый", "Ублюдок", "Все Хреново",
    "Блядь", "Сука", "Пизда", "Хуй", "Ебать", "Еблан", "Хер", "Тварь", "Мудила", "Дрочить", 
    "Пидор", "Пиздец", "Шлюха", "Сучка", "Гондон", "Педик", "Гандон", "Хуета", "Охуеть", 
    "Нахуй", "Ебаный", "Срака", "Пидорас", "Тупая", "Дура", "Ебучий", "Мудрец", "Урод", 
    "Пошел Нахуй", "Блядь", "Чмо", "Похуй", "Сосать", "Уродка", "Петух", "Долбоеб", "Козел",
    "Сучий", "Курва", "Пиздатый", "Сука Блять", "Пиздатина", "Херовина", "Мать Твою", "Пиздин", 
    "Ебало", "Сучар", "Пиздюк", "Педик", "Дерьмо", "Говно", "Долбанутый", "Ублюдок", "Все Хреново",
    "БЛЯДЬ", "СУКА", "ПИЗДА", "ХУЙ", "ЕБАТЬ", "ЕБЛАН", "ХЕР", "ТВАРЬ", "МУДИЛА", "ДРОЧИТЬ", 
    "ПИДОР", "ПИЗДЕЦ", "ШЛЮХА", "СУЧКА", "ГОНДОН", "ПЕДИК", "ГАНДОН", "ХУЕТА", "ОХУЕТЬ", 
    "НАХУЙ", "ЕБАНЫЙ", "СРАКА", "ПИДОРАС", "ТУПАЯ", "ДУРА", "ЕБУЧИЙ", "МУДРЕЦ", "УРОД", 
    "ПОШЕЛ НАХУЙ", "БЛЯДЬ", "ЧМО", "ПОХУЙ", "СОСАТЬ", "УРОДКА", "ПЕТУХ", "ДОЛБОЕБ", "КОЗЕЛ",
    "СУЧИЙ", "КУРВА", "ПИЗДАТЫЙ", "СУКА БЛЯТЬ", "ПИЗДАТИНА", "ХЕРОВИНА", "МАТЬ ТВОЮ", "ПИЗДИН", 
    "ЕБАЛО", "СУЧАР", "ПИЗДЮК", "ПЕДИК", "ДЕРЬМО", "ГОВНО", "ДОЛБАНУТЫЙ", "УБЛЮДОК", "ВСЕ ХРЕНОВО",
    # добавьте больше слов по вашему усмотрению...
]

# Оптимизация: создаем один раз компилированное регулярное выражение для плохих слов
BAD_WORDS_PATTERN = re.compile(r'\b(?:' + '|'.join(map(re.escape, BAD_WORDS)) + r')\b', re.IGNORECASE)

# Списки для приветствий, прощаний и т.д.
RESPONSES = {
    "hello": ["привет ✋", "Привет", "прив 🙋‍♂️", "Прив 👋", "здарова 🖐️", "Здарова"],
    "bye": ["Пока 🤚", "пока 👋", "покеда", "Досвидания 👋", "Досвидос 🤚", "чао 👋"],
    "good_night": ["Спокойной ночи 😴", "спокойной ночи 🥱", "Спокойной 😴", "спокойной 🥱"]
}

HELLO_PATTERN = re.compile(r'\b(?:привет|здарова|hi|hello)\b', re.IGNORECASE)
BYE_PATTERN = re.compile(r'\b(?:пока|досвидания|bye|чао)\b', re.IGNORECASE)
GOOD_NIGHT_PATTERN = re.compile(r'\b(?:спокойной ночи|good night)\b', re.IGNORECASE)

# Подключение к базе данных
conn = sqlite3.connect("warnings.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    username TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0
)
""")
conn.commit()

# Функции работы с базой данных
def add_warning(username):
    cursor.execute("""
    INSERT INTO warnings (username, count)
    VALUES (?, 1)
    ON CONFLICT(username) DO UPDATE SET count = count + 1
    """, (username,))
    conn.commit()
    logging.info(f"Добавлено предупреждение для пользователя {username}")

def get_warnings(username):
    cursor.execute("SELECT count FROM warnings WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else 0

def reset_warnings(username):
    cursor.execute("DELETE FROM warnings WHERE username = ?", (username,))
    conn.commit()

# Проверка текста на нецензурные слова
def contains_bad_word(text):
    return BAD_WORDS_PATTERN.search(text)

# Проверка текста на приветствия, прощания и т.д.
def match_pattern(text, pattern):
    return bool(pattern.search(text))

# Проверка префикса
def has_prefix(message_text):
    return any(message_text.startswith(prefix) for prefix in COMMAND_PREFIXES)

def remove_prefix(message_text):
    for prefix in COMMAND_PREFIXES:
        if message_text.startswith(prefix):
            return message_text[len(prefix):].strip()
    return message_text

# Обработчик сообщений
@dp.message()
async def handle_message(message: types.Message):
    logging.info(f"Получено сообщение от {message.from_user.username}: {message.text}")

    if contains_bad_word(message.text):
        username = message.from_user.username or message.from_user.full_name
        add_warning(username)
        warning_count = get_warnings(username)
        await message.reply(f"Ай ай ай {username}, нельзя материться! Всего предупреждений: {warning_count}.")
        
        if warning_count >= 3:
            await temp_ban(message, 1)
            await message.reply(f"{username} временно заблокирован на 1 день за 3 нарушения.")
            reset_warnings(username)

    if match_pattern(message.text, HELLO_PATTERN):
        await message.reply(random.choice(RESPONSES["hello"]))

    if match_pattern(message.text, BYE_PATTERN):
        await message.reply(random.choice(RESPONSES["bye"]))

    if match_pattern(message.text, GOOD_NIGHT_PATTERN):
        await message.reply(random.choice(RESPONSES["good_night"]))

    if not has_prefix(message.text):
        return

    command_body = remove_prefix(message.text)
    args = command_body.split(maxsplit=1)
    command = args[0].lower()
    arg_text = args[1] if len(args) > 1 else ""

    if command in ["предупредить", "забанить", "разбанить"] and not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя!")
        return

    if command == "предупредить":
        username = message.reply_to_message.from_user.username or "пользователь"
        add_warning(username)
        warning_count = get_warnings(username)
        await message.answer(f"{username}, предупреждение! Всего предупреждений: {warning_count}.")

    elif command == "забанить":
        await message.chat.ban(message.reply_to_message.from_user.id)
        await message.answer(f"Пользователь {message.reply_to_message.from_user.username} заблокирован.")

    elif command == "разбанить":
        await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.answer(f"{message.reply_to_message.from_user.username} разбанен.")

# Временный бан
async def temp_ban(message: types.Message, days: int):
    until_date = message.date + timedelta(days=days)
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=until_date,
    )

# Основная функция
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
