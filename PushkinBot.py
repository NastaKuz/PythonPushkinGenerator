import telebot
import Pushkin_generator
import random
import os

from telebot import types

TOKEN = os.getenv('TOKEN')
# TOKEN = config.TOKEN

bot = telebot.TeleBot(TOKEN)
sticker_path = 'Stickers/'
commands = ['/start', '/help', '/generate']


# Обработчик команды '/help'
@bot.message_handler(commands=['help'])
def help_mes(message):
    result = 'По команде /generate этот бот может сгенерировать цитату в стиле Пушкина' \
             ' с заданным началом'

    bot.send_message(message.chat.id, result)


# Обработчик команды '/start'
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open(sticker_path + '10.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('/generate')
    button2 = types.KeyboardButton('/help')

    markup.add(button1, button2)

    bot.send_message(message.chat.id,
                     f'Добро пожаловать, <b>{message.from_user.first_name}</b>!\n Я - {bot.get_me().first_name}, бот',
                     parse_mode='html', reply_markup=markup)


# Inline клавиатура, попробовать снова
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'again':
                generate_text(call.message)
    except Exception as e:
        print(repr(e))


# Обработчик команды '/generate'
@bot.message_handler(commands=['generate'])
def generate_text(message):
    msg = bot.send_message(message.chat.id, 'Введите начало (1 или несколько слов):')
    bot.register_next_step_handler(msg, generate_step)


# Генерация текста
def generate_step(message):
    try:
        seed = message.text
        if seed == '/help':
            help_mes(message)
        elif seed == '/generate':
            generate_text(message)
        else:
            bot.send_message(message.chat.id, 'Подождите, ищем вдохновение...')
            result = Pushkin_generator.letsgo(False, seed)
            gen_markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Попробовать еще", callback_data='again')
            gen_markup.add(item1)
            msg = bot.send_message(message.chat.id, result, reply_markup=gen_markup)
    except AttributeError:
        msg = bot.send_message(message.chat.id, 'Это точно слова? Попробуй снова')
        generate_text(msg)


# Обработчик текстовых команд
@bot.message_handler(content_types=['text'])
def reply(message):
    if message.chat.type == 'private':
        if message.text == 'Генерировать цитату':
            generate_text(message)
        elif message.text == 'Помощь':
            help_mes(message)
        else:
            bot.send_message(message.chat.id, 'Нипонятно(')


# Развлечение
@bot.message_handler(content_types=['sticker'])
def sticker_reply(message):
    random_sticker = sticker_path + str(random.randint(0, 22)) + '.webp'
    sticker = open(random_sticker, 'rb')
    bot.send_sticker(message.chat.id, sticker)


bot.polling(none_stop=True)
