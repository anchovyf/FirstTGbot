import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8577545519:AAEQ8KMUQEiL3QkmIgqT6s3WPycyuaJyzMQ'
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_rate(base: str, target: str):
    url = f'https://api.exchangerate-api.com/v4/latest/{base}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get(target)
            if rate:
                return f'Курс {base} к {target}: {rate}'
            else:
                return f'Валюта {target} не найдена'
        else:
            return 'Ошибка запроса к API'
    except:
        return 'Ошибка подключения к серверу'

button_rate = KeyboardButton(text='/rate')
button_help = KeyboardButton(text='/help')
button_start = KeyboardButton(text='/start')
button_chup = KeyboardButton(text='/chup')

keyboard = types.ReplyKeyboardMarkup(keyboard = [[button_rate, button_help, button_start, button_chup]], resize_keyboard = True)

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Привет, это бот для определения курса валют. Используй /rate USD RUB и другие валюты, чтобы всегда быть в курсе курсов', reply_markup = keyboard)

@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer('Существующие пока команды:\n/start - приветствие\n/help - справка по командам\n/rate - курс валют\n/chup - чюпъ\n', reply_markup = keyboard)

@dp.message(Command('rate'))
async def rate(message: types.Message):
    args = message.text.split()
    if len(args) != 3:
        await message.answer('Пример: /rate USD RUB', reply_markup = keyboard)
        return

    base = args[1].upper()
    target = args[2].upper()
    result = get_rate(base, target)
    await message.answer(result, reply_markup = keyboard)

@dp.message(Command('chup'))
async def chup(message: types.Message):
    chup_url = 'https://imgfy.ru/vkOG59eNcrUnnEC'
    await message.answer_photo(photo = chup_url, caption = 'чюпъ', reply_markup = keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
