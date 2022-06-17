import sqlite3 as db
import telebot as tb
from telebot import types

try:
    bot = tb.TeleBot("5371827834:AAFfQDohC2UDvvVo-YWm57XEHxtOOOKa4Eo")
    print("Bot connection success")
except tb.ExceptionHandler:
    print("[!] Can't connect to Telegram")
try:
    data_connection = db.connect("database.db", check_same_thread=False)
    base = data_connection.cursor()
    print("DataBase Connection Success")
except db.OperationalError:
    print("[!] Can't connect to database")


@bot.message_handler(commands=['start'])
def start(m):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("RomanLabs", url="http://project5615402.tilda.ws/")
    markup.add(bt1)
    #bt2 = types.InlineKeyboardButton("Начать", callback_data='bot_start')
    #markup.add(bt2)
    bot.send_message(m.chat.id, "Привет! Вы используете PhasmoBot, созданный командой RomanLabs. Бот поможет вам "
                                "быстро и удобно получать информацию о призраках\n Бот основан на механиках игры "
                                "Phasmophobia.\n Чтобы начать - отправьте любое сообщение", reply_markup=markup)


#@bot.callback_query_handler(func=lambda call: True)
#def help_print(call):
    #markup = types.ReplyKeyboardMarkup()
    #bt1 = types.KeyboardButton("Летс го!")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    ghosts_db = base.execute("""SELECT * FROM ghosts""")
    ghosts = ghosts_db.fetchall()
    if message.text == "Информация о призраках":
        markup_ghosts = types.ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
        ghosts_size = 0
        bt_arr = []
        for i in ghosts:
            ghost = str(i[1])
            bt_arr.append(types.KeyboardButton(ghost))
            ghosts_size += 1
        markup_ghosts.add(*bt_arr)
        bot.send_message(message.chat.id,"Выберите призрака",reply_markup=markup_ghosts)
    elif {i for i in ghosts if i[1] == message.text}:
        for i in ghosts:
            if i[1] == message.text:
                markup_top_choose = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
                bt1 = types.KeyboardButton("Информация о призраках")
                bt2 = types.KeyboardButton("Информация о локациях")
                markup_top_choose.add(bt1, bt2)

                bot.send_message(message.chat.id,"Признаки:\n"+str(i[3])+"\nОсобенности:\n"+ str(i[2]),reply_markup=markup_top_choose)
    elif message.text == "Информация о локациях":
        bot.send_message(message.chat.id, "Раздел в разработке")
    else:
        markup_top_choose = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        bt1 = types.KeyboardButton("Информация о призраках")
        bt2 = types.KeyboardButton("Информация о локациях")
        markup_top_choose.add(bt1, bt2)
        bot.send_message(message.chat.id, text="Выберите раздел", reply_markup=markup_top_choose)


bot.polling(none_stop=True, interval=0)
