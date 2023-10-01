import telebot
from telebot import types
import settings
import re
from parser_atlas import get_parser_atlas_result, Ticket

user_dict = {}

class User:
    def __init__(self):
        self.first_town = None
        self.sec_town = None
        self.date = None
        self.day = None
        self.mounth = None
        self.year = None
    
    def date_split(self):
        dateArr = str(self.date).split('.')
        self.day = dateArr[0]
        self.mounth = dateArr[1]
        self.year = dateArr[2]

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
        user.date_split()
        bot.send_message(message.chat.id, 'Обрабатываем ваш запрос...')
        tickets = get_parser_atlas_result(user)
        msg = 'Atlasbus.by \n'
        for item in tickets:
            msg += f'{item.dep_time} \n' 
            msg += f'{item.dep_place}\n'
            msg += f'       v \n'
            msg += f'{item.arr_time} {item.arr_place}\n'
            msg += f'{item.free_space} Цена - {item.cost} \n'
            msg += '------------------------------------------------- \n'
        bot.send_message(message.chat.id, msg)
            
    else:
        msg = bot.send_message(message.chat.id,"Ой, что-то пошло не так. Введите дату отправлления в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(msg, date_message)
        

bot.infinity_polling()