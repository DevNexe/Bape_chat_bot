import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from datetime import timedelta
import re
import random


API_TOKEN = "7778634250:AAHlgfUNEG246xkQDKh2iIOC3qX1xduG_HQ"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
print("start")

COMMAND_PREFIXES = ["Бот ", "бот ", "Bot ", "bot "]  # Уникальные префиксы
WARNINGS_FILE = "warnings.txt"

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

hll = [
    "Hello", "hello", "привет", "Привет", "Hi", "hi", "прив", "Прив", "пр", "Пр", "Здарова", "здарова",
]

by = [
    "Bye", "bye", "Пока", "пока", "покеда", "Покеда", "досвидания", "Досвидания", "досвидос", "Досвидос", "Чао", "чао",
]

gn = [
    "good night", "Good night", "Спокойной ночи", "спокойной ночи", "Споки ноки", "споки ноки", "Спокойной", "спокойной", "сп", "Сп",
]

rgn = [
    "Спокойной ночи 😴", "спокойной ночи 🥱", "Спокойной 😴", "спокойной 🥱",
]

rdb = [
    "Пока 🤚", "пока 👋", "покеда", "Покеда 🤚", "досвидания 👋", "Досвидания", "досвидос 🤚", "Досвидос", "Чао 👋", "чао 🤚",
]

rndm = [
    "привет ✋", "Привет", "прив 🙋‍♂️", "Прив 👋", "пр", "Пр", "Здарова 🖐️", "здарова",
]

def read_file(filename):
    data = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                username, count = line.strip().split(": ")
                data[username] = int(count)
    except FileNotFoundError:
        pass
    return data

def write_file(data, filename):
    with open(filename, "w") as f:
        for username, count in data.items():
            f.write(f"{username}: {count}\n")

# Функция проверки сообщения на наличие матерных слов
def contains_bad_word(text):
    pattern = r'\b(?:' + '|'.join(map(re.escape, BAD_WORDS)) + r')\b'
    return re.search(pattern, text, re.IGNORECASE)

def hello(text):
    pattern = r'\b(?:' + '|'.join(map(re.escape, hll)) + r')\b'
    return re.search(pattern, text, re.IGNORECASE)

def bye(text):
    pattern = r'\b(?:' + '|'.join(map(re.escape, by)) + r')\b'
    return re.search(pattern, text, re.IGNORECASE)

def good_night(text):
    pattern = r'\b(?:' + '|'.join(map(re.escape, gn)) + r')\b'
    return re.search(pattern, text, re.IGNORECASE)

def add_warning(username):
    warnings = read_file(WARNINGS_FILE)
    warnings[username] = warnings.get(username, 0) + 1
    write_file(warnings, WARNINGS_FILE)

def get_warnings(username):
    warnings = read_file(WARNINGS_FILE)
    return warnings.get(username, 0)

def reset_warnings(username):
    warnings = read_file(WARNINGS_FILE)
    warnings.pop(username, None)
    write_file(warnings, WARNING_FILE)

# Проверка префикса
def has_prefix(message_text):
    for prefix in COMMAND_PREFIXES:
        if message_text.startswith(prefix):
            return True
    return False

def remove_prefix(message_text):
    for prefix in COMMAND_PREFIXES:
        if message_text.startswith(prefix):
            return message_text[len(prefix):].strip()
    return message_text

# Команда предупреждения
@dp.message()
async def handle_commands(message: types.Message):
    if "start" in message.text:
        username = message.from_user.username or message.from_user.full_name
        await message.reply(f"Привет {username}, чем могу помочь?")

    elif "warn" in message.text:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        username = message.reply_to_message.from_user.username or "пользователь"
        add_warning(username)
        warning_count = get_warnings(username)
        await message.answer(f"{username} я даю тебе предупреждение! Всего предупреждений: {warning_count}. ‼️‼️‼️")

        if warning_count >= 3:
            await temp_ban(message.reply_to_message, 1)
            await message.answer(f"{username} временно забанен на 1 день за 3 нарушения.")
            reset_warnings(username)

    elif "ban" in message.text:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        await message.chat.ban(message.reply_to_message.from_user.id)
        await message.answer(f"Пользователь {message.reply_to_message.from_user.username}. был забанен")

    elif "pardon" in message.text:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"{message.reply_to_message.from_user.username} можно вернуться.")

    elif "clear" in message.text:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        async for msg in bot.get_chat_history(message.chat.id, limit=10):
            if msg.from_user.id == message.reply_to_message.from_user.id:
                await msg.delete()

        await message.answer(f"Последние 10 сообщений от {message.reply_to_message.from_user.username} были уничтожены.")

    elif "mute" in message.text:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        mute_duration = timedelta(minutes=10)
        until_date = message.date + mute_duration

        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.answer(f"Пользователю {message.reply_to_message.from_user.username} запрещенно говорить в течении 10 минут.")

    elif "unmute" in message.text:
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"{message.reply_to_message.from_user.username} тебе разрешается говорить.")

    elif hello(message.text):
        rdm = random.choice(rndm)
        await message.reply(rdm)

    elif bye(message.text):
        rdby = random.choice(rdb)
        await message.reply(rdby)

    elif good_night(message.text):
        rdgn = random.choice(rgn)
        await message.reply(rdgn)

    elif not has_prefix(message.text):
        return  # Игнорируем сообщения 
    command_body = remove_prefix(message.text)  # Убираем префикс
    args = command_body.split(maxsplit=1)  # Разделяем команду и аргументы
    command = args[0].lower()
    arg_text = args[1] if len(args) > 1 else ""

    if command == "предупредить":
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        username = message.reply_to_message.from_user.username or "пользователь"
        add_warning(username)
        warning_count = get_warnings(username)
        await message.answer(f"{username} я даю тебе предупреждение! Всего предупреждений: {warning_count}. ‼️‼️‼️")

        if warning_count >= 3:
            await temp_ban(message.reply_to_message, 1)
            await message.answer(f"{username} временно забанен на 1 день за 3 нарушения.")
            reset_warnings(username)

    elif command == "забанить":
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        await message.chat.ban(message.reply_to_message.from_user.id)
        await message.answer(f"Пользователь {message.reply_to_message.from_user.username} забанен.")

    elif command == "разбанить":
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        await bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"{message.reply_to_message.from_user.username} можно вернуться.")

    elif command == "очистить сообщения":
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        async for msg in bot.get_chat_history(message.chat.id, limit=10):
            if msg.from_user.id == message.reply_to_message.from_user.id:
                await msg.delete()

        await message.answer(f"Последние 10 сообщений от {message.reply_to_message.from_user.username} уничтожены.")

    elif command == "мут":
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        mute_duration = timedelta(minutes=10)
        until_date = message.date + mute_duration

        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.answer(f"Пользователю {message.reply_to_message.from_user.username} запрещенно говорить в течении 10 минут.")

    elif command == "размут":
        if not message.reply_to_message:
            await message.answer("Эту команду нужно использовать в ответ на сообщение пользователя.")
            return

        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"{message.reply_to_message.from_user.username} тебе разрешается говорить.")

# Функция временного бана
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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
