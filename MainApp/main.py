import telebot
import datetime
from news_parser import parse
from telebot import types
from DB_conn.DB_conn import DBConnection

token = "2024403137:AAG-ZXMvorH6nMrApa0JlELgdF-fERtU15g"
bot = telebot.TeleBot(token)

last_news = ""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f"Привет {message.from_user.first_name}. \nЧтобы узнать последние новости набери 'Новости'")
    con = DBConnection()
    con.add_user(username=message.from_user.username,
                 us_name=message.from_user.first_name,
                 us_sname=message.from_user.last_name)
    bot.reply_to(message, "Ваши данные были добавленны в базу")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, f"Чтобы узнать последние новости набери 'Новости'")


@bot.message_handler(content_types=["text"])
def send_news(message):
    if message.text.upper() == "НОВОСТИ":
        global last_news
        content = parse()
        if last_news != content["title"]:
            read_keyboard = types.InlineKeyboardMarkup()
            key_read = types.InlineKeyboardButton(text="Читать полностью", callback_data="read")
            read_keyboard.add(key_read)
            bot.send_photo(message.from_user.id,
                           photo=content['pict'],
                           caption=f"{content['date']}\n{content['title']}",
                           reply_markup=read_keyboard)
            last_news = content["title"]
        else:
            bot.send_message(message.from_user.id, text="Других новостей пока нет")

    if message.text.upper() == "СДЕЛАЙ ЗАМЕТКУ":
        bot.send_message(message.from_user.id, "Ведите текст заметки")
        bot.register_next_step_handler(message, insert_record)

    if message.text.upper() == "ПОСЛЕДНЯЯ ЗАМЕТКА":
        con = DBConnection()
        records = con.get_record(un=message.from_user.username)
        dates = [key for key in records]
        dates.sort()
        last_date = dates[-1]
        last_record = records[last_date]
        bot.send_message(message.from_user.id, text=f"ДАТА: {last_date}\nТЕКСТ: {last_record}")


insert_record_text = ""


def insert_record(message):
    global insert_record_text
    record_keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да", callback_data="insert_record_yes")
    record_keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет", callback_data="insert_record_no")
    record_keyboard.add(key_no)
    insert_record_text= message.text
    bot.send_message(message.from_user.id, text="Cохранить заметку?", reply_markup=record_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "read":
        content_body = parse(body=True)
        bot.send_message(call.message.chat.id,  text=f"{content_body}")
    if call.data == "insert_record_yes":
        print(call.message)
        con = DBConnection()
        con.add_record(rec_text=insert_record_text, un=call.message.chat.username)
        bot.send_message(call.message.chat.id, text="Заметка сохранена")
    elif call.data == "insert_record_no":
        bot.send_message(call.message.chat.id, text="Заметка отменена")

bot.infinity_polling()
