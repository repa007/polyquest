
import telebot
import pandas as pd
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import DB
#mydb = DB("127.0.0.1",3306,"root","228228228Nm","mydb")#дима
mydb = DB("127.0.0.1",3306,"root","j58AEiPY12@5","mydb")#Локальный

bot = telebot.TeleBot('6323243276:AAFYCmIuRfV3b8U83N4H1oqqdEHZ5-Wc_Do')
from telebot import types


#Commands
@bot.message_handler(commands=['start'])
def startBot(message):
  reply = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nЭто бот для выдачи задач. Вы можете открыть инструкцию командой /help\nДля начала следует пройти регистрацию."
  markup = types.InlineKeyboardMarkup()
  button_registration = types.InlineKeyboardButton(text = 'Регистрация', callback_data='registration')
  markup.add(button_registration)
  bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    reply = 'Для начала пройдите регистрацию (Пожалуйста, укажите ваши реальные данные, чтоб потом не пришлось выяснять кто такой Taburetka(⌐■_■)). Если вы меняли имя пользователя в Telegram после регистрации, то вам следует зарегистрироваться повторно /registration или сменить имя пользователя на прежнее, иначе бот вас не узнает.\n\n'
    reply+= "<b>Доступные команды:</b>\n"
    reply+= "/help - как эта штука работает\n"
    reply+= "/registration - Зарегистрироваться (бот создаёт запись в таблице пользователей в своей базе данных и потом записывает за этим пользователем задачи.)\n"
    reply+= "/GetTasks - Жми сюда чтобы глянуть какие задачи свободны и взять какие-нибудь себе\n"
    reply+= "/MyTasks - Жми сюда чтобы глянуть какие задачи ты уже взял\n"
    reply+= "/GetExcel - Выгружает базу данных бота табличкой\n"
    reply+= "/Start - Приветствие (вы его уже видели)\n"
    reply+= "\nКогда возьмёте задание, свяжитесь с контактом указанным в описании задания и сообщите об этом\n"
    markup = types.InlineKeyboardMarkup()
    button_registration = types.InlineKeyboardButton(text='Скрыть', callback_data='Hide')
    markup.add(button_registration)
    bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['GetTask'])
def GetTasks(message):
    reply = 'Вот список задач, нажмите на интересующую чтобы узнать подробнее:'
    rec = mydb.GetTasksAll()
    records = [('запись 1', 1), ('запись 2', 2), ('запись 3', 3)]

    buttons = [InlineKeyboardButton(r[0], callback_data=str(r[1])) for r  in rec]

    # Создаем объект клавиатуры и добавляем в него кнопки
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)

    # Отправляем сообщение с клавиатурой пользователю
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)

@bot.message_handler(commands=['GetExcel'])
def GetExcel(message):
    #import sqlite3
    #db = sqlite3.connect('yourdatabase.db')
    #cursor = db.cursor()
    #cursor.execute('''SELECT * FROM students''')
    #rows = cursor.fetchall()
    #db.close()
    #my_list = [[None for j in range(7)] for i in range(len(rows))]
    #for i in range(len(rows)):
       # my_list[i] = list(rows[i])
   # print(my_list)

    #cols = SELECT COUNT(*) FROM fooTable;
  cols = 12 #считать сколько строк в бд
  i = 0
  #rows = 6

  data = [[1, 'Id', 'ФИО', 'имяТГ', 'quest', 'курс', 'группа'],
          [2, 'Id', 'ФИО', 'имяТГ', 'quest', 'курс', 'группа'],
          [3, 'Id', 'ФИО', 'имяТГ', 'quest', 'курс', 'группа']]
  #for i in range(cols):
      #bot.reply_to(message, data[[]])
  #transpose .T Если перевернуло
  df = pd.DataFrame(data=data)
  df.to_excel('Itog.xlsx')
  bot.send_document(message.chat.id, open("Itog.xlsx", "rb"))


@bot.message_handler()#tol'ko vnizu
def info(message):
    bot.reply_to(message, "Я тебя не понимать 「(°ヘ°) \n Используй стандартные команды бота")

    bot.reply_to(message, "Я тебя не понимать 「(°ヘ°) \nИспользуй стандартные команды бота \n/help")
#That is all Commands


@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if function_call.data == "registration": #to do
        reply = "Это ебать бот типо который для пд можно выбрать задачу или иди нахуй короче"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Пойти на хуй?", url="http://go-friend-go.narod.ru/"))
        bot.send_message(function_call.message.chat.id, reply, reply_markup=markup)
        bot.answer_callback_query(function_call.id)

     elif function_call.data.isdigit():
        reply = "Выбрана кнопка: " + function_call.data
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Принять", callback_data="WantIt" + function_call.data))
        bot.send_message(function_call.message.chat.id, reply, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
     elif "WantIt" in function_call.data:
        numtask = function_call.data.replace("WantIt", '')
        reply = "Вы точно хотите принять задание №" + numtask + "?\nОтменить это действие будет невозможно!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Нет", callback_data="Hide"), types.InlineKeyboardButton("Принять", callback_data="Ofcourse" + str(numtask)))
        bot.send_message(function_call.message.chat.id, reply, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
     elif function_call.data == "Hide":
         bot.delete_message(chat_id=function_call.message.chat.id, message_id=function_call.message.message_id)
     elif "Ofcourse" in function_call.data:
         numtask = function_call.data.replace("Ofcourse", '')
         #здесь значит надо прихуярить метод привязывания задачки к студенту (Семён, сделай метод для приписывания челу задачки по её номеру numtask)



bot.infinity_polling() #For permonent working