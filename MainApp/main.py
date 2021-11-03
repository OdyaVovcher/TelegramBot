import telebot
from news_parser import parse
from telebot import types


token = "2024403137:AAG-ZXMvorH6nMrApa0JlELgdF-fERtU15g"
bot = telebot.TeleBot(token)


last_news = ""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f"Привет {message.from_user.first_name}. \nЧтобы узнать последние новости набери 'Новости'")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, f"Чтобы узнать последние новости набери 'Новости'")


@bot.message_handler(func=lambda message: True)
def send_news(message):
    if message.text.upper() == "НОВОСТИ":
        global last_news
        content = parse()
        if last_news != content["title"]:
            keyboard = types.InlineKeyboardMarkup()
            key_read = types.InlineKeyboardButton(text="Читать статью", callback_data="read")
            keyboard.add(key_read)
            bot.send_photo(message.from_user.id,
                           photo=content['pict'],
                           caption=f"{content['date']}\n{content['title']}",
                           reply_markup=keyboard)
            last_news = content["title"]
        else:
            bot.send_message(message.from_user.id, text="Других новостей пока нет")
    else:
        bot.reply_to(message, text=message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "read":
        content_body = parse(body=True)
        bot.send_message(call.message.chat.id,  text=f"{content_body}")


bot.infinity_polling()

#Testing