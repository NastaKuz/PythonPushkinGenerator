import telebot
import config
import Pushkin_generator
import random
import os

from telebot import types

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)
sticker_path = 'Stickers/'
pushkin_pics_path = 'Pushkin_pics/'


def pic(text):
    print(text)


# Обработчик мини-меню
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message == 'pic':
            pic('Вот')

    except Exception as e:
        print(repr(e))


# Обработчик команды '/start'
@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open(sticker_path + '10.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/generate")
    button2 = types.KeyboardButton("/help")

    markup.add(button1, button2)

    bot.send_message(message.chat.id,
                     f"Добро пожаловать, <b>{message.from_user.first_name}</b>!\n Я - {bot.get_me().first_name}, бот",
                     parse_mode='html', reply_markup=markup)


# Обработчик команды '/generate'
@bot.message_handler(commands=['generate'])
def generate_text(message):
    msg = bot.send_message(message.chat.id, "Введите начало (1 или несколько слов):")
    bot.register_next_step_handler(msg, generate_step)


# Генерация текста
def generate_step(message):
    seed = message.text
    bot.send_message(message.chat.id, "Подождите, ищем вдохновение...")
    result = Pushkin_generator.predict(seed)
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton("Сделать картинкой", callback_data='pic')
    markup.add(button)

    bot.send_message(message.chat.id, result, reply_markup=markup)


# Обработчик текстовых команд
@bot.message_handler(content_types=['text'])
def reply(message):
    if message.chat.type == 'private':
        if message.text == "Генерировать цитату":
            generate_text(message)
            # bot.send_message(message.chat.id, "Вот цитата:")
        elif message.text == "Smth":
            bot.send_message(message.chat.id, "Вот еще что-то:")
        else:
            bot.send_message(message.chat.id, "Нипонятно(")
    # bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['sticker'])
def sticker_reply(message):
    random_sticker = sticker_path + str(random.randint(0, 22)) + ".webp"
    sticker = open(random_sticker, 'rb')
    bot.send_sticker(message.chat.id, sticker)


bot.polling(none_stop=True)
