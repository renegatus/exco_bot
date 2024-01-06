import telebot
import sqlite3
import datetime

API_TOKEN = '6489457070:AAH8re67vlrTtUnMcDGZmiXkKulMHPhKvFA'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am HistorySavingBot.
I can save your history, /delete and /show!
""")
    
# Handle '/delete' 
@bot.message_handler(commands=['delete', 'del'])
def delete_history(message):
    
    conn = sqlite3.connect('history_database.db')
    conn.execute('DELETE FROM history WHERE chat_id = ?',(message.chat.id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "Your history was deleted!")    

@bot.message_handler(commands=["show_all"])
def show_all(message):

    conn = sqlite3.connect('history_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, date FROM history WHERE chat_id = ?",(message.chat.id,))
    result_all = cursor.fetchall()

    if result_all:  # не забудь про проверку на случай, если история пуста
        for res in result_all:
            bot.send_message(message.chat.id, f'{res[0]} - {res[1]}')
    else:
        bot.send_message(message.chat.id, "История пуста")


@bot.message_handler(commands=["show"])
def show(message):

    size = telebot.util.extract_arguments(message.text)
    try:
        size = int(size)
    except:
        size = 1

    conn = sqlite3.connect('history_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, date FROM history WHERE chat_id = ?", (message.chat.id,))

    if size == 1:
        result = cursor.fetchone()
        result = [result]
    else:
        result = cursor.fetchmany(size)

    if result:  # не забудь про проверку на случай, если история пуста
        for res in result:
            bot.send_message(message.chat.id, f'{res[0]} - {res[1]}')
    else:
        bot.send_message(message.chat.id, "История пуста")




# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    chat_id = message.chat.id
    date = datetime.datetime.fromtimestamp(message.date)


    conn = sqlite3.connect('history_database.db')
    conn.execute('INSERT INTO history (text, chat_id, date) values(?, ?, ?)', (text, chat_id, date))
    conn.commit()
    conn.close()

    bot.reply_to(message, message.text)


bot.infinity_polling()
