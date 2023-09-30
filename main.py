import telebot
from telebot import types
import settings

user_dict = {}

class User:
    def __init__(self):
        self.first_town = None
        self.sec_town = None

bot=telebot.TeleBot(settings.token)
print(settings.token)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Покажи билеты")
    markup.add(item1)
    bot.send_message(message.chat.id,"Привет ✌️. Я бот для поиска билетов дял поездок между городами Беларуси ")
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def button_message(message):
    if message.text == 'Покажи билеты':
        msg = bot.send_message(message.chat.id,"Напишите город откуда хотите ехать")
        bot.register_next_step_handler(msg, first_town_message)
        

def first_town_message(message):
    user = User()
    user.first_town = message.text
    user_dict[message.chat.id] = user
    msg = bot.send_message(message.chat.id,"Напишите город куда хотите ехать")
    bot.register_next_step_handler(msg, sec_town_message)

def sec_town_message(message):
    user = user_dict[message.chat.id]
    user.sec_town = message.text
    user_dict[message.chat.id] = user
    bot.send_message(message.chat.id, 'Из ' + str(user.first_town) + ' В ' + str(user.sec_town))
  
bot.infinity_polling()