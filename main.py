from telebot import TeleBot
from logic import *
from config import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot(API_TOKEN)

def gen_markup():
    sql = manager.perebor()
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    for row in sql:
        markup.add(InlineKeyboardButton(str(row[0]), callback_data=str(row[0])))
    markup.add(InlineKeyboardButton('Всё', callback_data='all'))
    return markup

def gen_markup1(user_id):
    sql = manager.podbor_raboti(user_id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for row in sql:
        markup.add(InlineKeyboardButton(str(row[0]), callback_data=str(row[0])))
    return markup

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handler_callback(call):
    callback_data = call.data
    bot.answer_callback_query(call.id)
    user_id = call.message.chat.id

    if callback_data == 'all':
        handler_all(call)
    elif callback_data == 'Учитель' or callback_data == 'Архитектор' or callback_data == 'Программист' or callback_data == 'Дизайнер':
        bot.edit_message_text(chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=manager.deskription(callback_data),
                            reply_markup=None
                            )
        manager.delete_user(user_id)

    else:
        manager.registr(user_id, callback_data)
            

def handler_all(call):
    # Редактируем оригинальное сообщение
    user_id = call.message.chat.id
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Вам могут понравиться эти профессии: {manager.recomend_work(user_id)}",
        reply_markup=gen_markup1(user_id))
    
@bot.message_handler(commands=['start'])
def start(message):
    markup = gen_markup()
    bot.send_message(message.chat.id, 'Выбери то, что по душе тебе', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Привет'or message.text == 'привет':
        bot.send_message(message.chat.id, 'Привет, я бы с тобой поболтал, но я создан для другого, напиши /start')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю, напиши /start')


def polling_thread():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    manager = Work(database)
    manager.create_tables()
    polling_thread()
    