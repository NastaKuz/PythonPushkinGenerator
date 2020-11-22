import telebot
import config
import Pushkin_generator
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


def generate_text(message):
    bot.send_message(message.chat.id, "Введите начало (1 или несколько слов):")
    seed = message.text
    bot.send_message(message.chat.id, "Подождите, ищем вдохновение...")
    result = Pushkin_generator.predict(seed)
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton("Сделать картинкой", callback_data='pic')
    markup.add(button)

    bot.send_message(message.chat.id, result, reply_markup=markup)


def pic(text):
    print(text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message == 'pic':
            pic("Вот")

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Генерировать цитату", reply_markup=None)

    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Генерировать цитату")
    button2 = types.KeyboardButton("Smth")

    markup.add(button1, button2)

    bot.send_message(message.chat.id,
                     f"Добро пожаловать, <b>{message.from_user.first_name}</b>!\n Я - {bot.get_me().first_name}, бот",
                     parse_mode='html', reply_markup=markup)


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


bot.polling(none_stop=True)
