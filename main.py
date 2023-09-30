import telebot
from telebot import types
import settings
import re

user_dict = {}

class User:
    def __init__(self):
        self.first_town = None
        self.sec_town = None
        self.date = None

bot=telebot.TeleBot(settings.token)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Показать билеты")
    markup.add(item1)
    bot.send_message(message.chat.id,"Привет ✌️. Я бот для поиска билетов дял поездок между городами Беларуси ")
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def button_message(message):
    if message.text == 'Покажи билеты':
        msg = bot.send_message(message.chat.id,"Напишите город отправки:")
        bot.register_next_step_handler(msg, first_town_message)
        

def first_town_message(message):
    user = User()
    user.first_town = message.text
    user_dict[message.chat.id] = user
    msg = bot.send_message(message.chat.id,"Напишите город назначения")
    bot.register_next_step_handler(msg, sec_town_message)

def sec_town_message(message):
    user = user_dict[message.chat.id]
    user.sec_town = message.text
    user_dict[message.chat.id] = user
    msg = bot.send_message(message.chat.id,"Введите дату отправлления в формате ДД.ММ.ГГГГ")
    bot.register_next_step_handler(msg, date_message)
    
    
def date_message(message):
    user = user_dict[message.chat.id]
    user.date = message.text
    user_dict[message.chat.id] = user
    pattern = re.compile(r'^(0?[1-9]|1[012])[- /.](0?[1-9]|[12][0-9]|3[01])[- /.](19|20)?[0-9]{2}$',  re.IGNORECASE | re.DOTALL)
    
    if  pattern.search(user.date) is not None:
        bot.send_message(message.chat.id, f'Из  {str(user.first_town)} В {str(user.sec_town)} {str(user.date)}')
    else:
        msg = bot.send_message(message.chat.id,"Ой, что-то пошло не так. Введите дату отправлления в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(msg, date_message)
bot.infinity_polling()