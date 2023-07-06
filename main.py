
import telebot
import pandas as pd
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import DB
#mydb = DB("127.0.0.1",3306,"root","228228228Nm","mydb")#дима
mydb = DB("127.0.0.1",3306,"root","228228228Nm","mydb")#Локальный

bot = telebot.TeleBot('6361892876:AAEsCPl6R8Rh7c3XWmuHb3Ab9X5vOQHTHTY')
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

@bot.message_handler(commands=['Huy']) #для отладки
def Huy(message):
    reply,e = mydb.GetTasksAll()
    reply = str(reply)
    bot.send_message(message.chat.id, reply, parse_mode='html')

@bot.message_handler(commands=['MyTasks'])#to do
def MyTasks(message):
    reply = message.chat.id
    reply = str(reply)
    bot.send_message(message.chat.id, reply, parse_mode='html')

@bot.message_handler(commands=['MyChatid'])
def MyChatid(message):
    reply = message.chat.id
    reply = str(reply)
    bot.send_message(message.chat.id, reply, parse_mode='html')

@bot.message_handler(commands=['GetTasks'])
def GetTasks(message):
    reply = 'Вот список задач, нажмите на интересующую чтобы узнать подробнее:'
    #records,e = mydb.GetTasksAll()
    records, e = mydb.GetFreeTasks(message.chat.id)

    keyboard = telebot.types.InlineKeyboardMarkup()
    i = 0
    for record in records:
        button = telebot.types.InlineKeyboardButton(text=str(records[i]["id"])+": "+str(records[i]["title"]), callback_data=str(records[i]["id"]), align="left")
        keyboard.row(button)
        i += 1

    # Отправляем сообщение с клавиатурой пользователю
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)

@bot.message_handler(commands=['GetExcel'])
def GetExcel(message):
    data, e = mydb.GetAllData()
    columns = ['id', 'name', 'lastname', 'group_number', 'course', 'tgname', 'chatid', 'task_id', 'title', 'body',
               'task_course',
               'max']
    # for i in range(cols):
    # bot.reply_to(message, data[[]])
    # transpose .T Если перевернуло
    df = pd.DataFrame(data=data, columns=columns)
    df.to_excel('Itog.xlsx', index=False)
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
        taskid = int(function_call.data)
        array = mydb.GetBodyOfTask(taskid)
        data_tuple = array[0]
        data_list = data_tuple[0]
        title = data_list["title"]
        body = data_list["body"]
        text = "<b>" + title + "</b>\n" + body
        reply = "Выбрано задание: " + str(taskid) + text
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Принять", callback_data="WantIt" + str(taskid)))
        bot.send_message(function_call.message.chat.id, reply,  parse_mode='html', reply_markup=markup)
        bot.answer_callback_query(function_call.id)
     elif "WantIt" in function_call.data:
        numtask = function_call.data.replace("WantIt", '')
        reply = "Вы точно хотите принять задание " + numtask + "?\nОтменить это действие будет невозможно!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Нет", callback_data="Hide"), types.InlineKeyboardButton("Принять", callback_data="Ofcourse" + str(numtask)))
        bot.send_message(function_call.message.chat.id, reply, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
     elif function_call.data == "Hide":
         bot.delete_message(chat_id=function_call.message.chat.id, message_id=function_call.message.message_id)
     elif "Ofcourse" in function_call.data:
         numtask = function_call.data.replace("Ofcourse", '')
         mydb.AssignTask(function_call.message.chat.id, numtask)
         #здесь значит надо прихуярить метод привязывания задачки к студенту (Семён, сделай метод для приписывания челу задачки по её номеру numtask)



bot.infinity_polling() #For permonent working