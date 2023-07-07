import re

import telebot
import uuid
from datetime import datetime

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
  reply = "Привет!\nЭто бот для выдачи задач. Вы можете открыть инструкцию командой /help\nДля начала следует пройти регистрацию с помощью команды /reg. Касается только студентов."
  bot.send_message(message.chat.id, reply, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    reply = 'Для начала пройдите регистрацию (Пожалуйста, укажите ваши реальные данные, чтоб потом не пришлось выяснять кто такой Taburetka(⌐■_■)).\n\n'
    reply+= "<b>Доступные команды:</b>\n"
    reply+= "/help - как эта штука работает\n"
    reply+= "/reg - Зарегистрироваться (бот создаёт запись в таблице пользователей в своей базе данных и потом записывает за этим пользователем задачи.)\n"
    reply+= "/gettasks - Жми сюда чтобы глянуть какие задачи свободны и взять какие-нибудь себе\n"
    reply+= "\nКогда возьмёте задание, свяжитесь с контактом указанным в описании задания и сообщите об этом\n"
    reply+= "/mytasks - Жми сюда чтобы глянуть какие задачи ты уже взял\n"
    reply+= "/getexcel - Выгружает базу данных бота табличкой\n"
    reply+= "/start - Приветствие (вы его уже видели)\n"
    reply += "\nДля админов:\n"
    reply += "/alltasks - Вывести все задания из бд\n"
    reply += "/newtask - Добавить задачу\n"
    reply += "/deletetask - Удалить задачи\n"
    reply += "/addadmin - Добавить администратора\n"
    reply += "/mychatid - Получить свой chatid\n"
    markup = types.InlineKeyboardMarkup()
    button_registration = types.InlineKeyboardButton(text='Скрыть', callback_data='Hide')
    markup.add(button_registration)
    bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['newtask'])
def NewTask_start(message):
    reply = "Для какого курса задание? "
    bot.send_message(message.chat.id, reply, parse_mode='html')
    bot.register_next_step_handler(message, NewTask_course)

def NewTask_course(message):
    course = message.text
    reply = "Придумайте заголовок: "
    bot.send_message(message.chat.id, reply, parse_mode='html')
    bot.register_next_step_handler(message, NewTask_title, course)

def NewTask_title(message, course):
    title = message.text
    reply = "Сколько человек максимум может взять это задание? "
    bot.send_message(message.chat.id, reply, parse_mode='html')
    bot.register_next_step_handler(message, NewTask_max, course, title)

def NewTask_max(message, course, title):
    maximum = message.text
    reply = "Полноценно опишите задание. Обязательно укажите, куда должен обратиться студент после того как возьмёт задание. "
    bot.send_message(message.chat.id, reply, parse_mode='html')
    bot.register_next_step_handler(message, NewTask_body, course, title, maximum)

tasks = {}


def NewTask_body(message, course, title, maximum):
    body = str(message.text)
    reply = "Проверьте правильность заполнения."
    reply += "\nЗаголовок: " + title
    reply += "\nДля курса № " + course
    reply += "\nМаксимальное кол-во студентов: " + maximum
    reply += "\nОписание задания: \n" + body
    task_id = str(datetime.now())  # создаем уникальный идентификатор для задачи
    tasks[task_id] = {'title': title, 'course': course, 'maximum': maximum, 'body': body}
    keyboard = types.InlineKeyboardMarkup()
    no_nt = types.InlineKeyboardButton(text='Отмена', callback_data='Hide')
    yes_nt = types.InlineKeyboardButton(text='Добавить', callback_data=f'newtaskblet,{task_id}')
    bla = f'response,{task_id}'
    keyboard.add(no_nt, yes_nt)
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)


@bot.message_handler(commands=['mytasks'])#to do
def MyTasks(message):
    chat_id = message.chat.id
    tasks, e = mydb.GetMyTasks(chat_id)

    if not tasks:
        reply = "Вы не взяли ни одной задачи."
    else:
        reply = f"Список ваших задач:\n\n"
        for task in tasks:
            reply += f"Задача {task['id']}:\n"
            reply += f"Название: {task['title']}\n"
            reply += f"Описание:\n {task['body']}\n"
            reply += "——————————————————\n"
    bot.send_message(chat_id, reply)

@bot.message_handler(commands=['deletetask'])
def delete_task_command_handler(message):
    chatid = message.chat.id
    isadmin = mydb.IsAdmin(chatid)
    if (isadmin == True):
        bot.reply_to(message, "Введите номер задания, которое Вы хотите удалить. Чтобы увидеть список задач введите /AllTask")
        bot.register_next_step_handler(message, delete_task_handler)
    else:
        bot.reply_to(message, "Для удаления заданий нужны права администратора!")

def delete_task_handler(message):
    try:
        task_id = int(message.text)
        mydb.DeleteTask(task_id)
        bot.reply_to(message, f"Задание с ID {task_id} было удалено.")
    except ValueError:
        bot.reply_to(message, "Некорректный формат номера задания. Пожалуйста, используйте только цифры для номера задания.")
    except:
        bot.reply_to(message, "Произошла ошибка при удалении задачи.")

@bot.message_handler(commands=['alltasks'])
def AllTasks(message):
        reply = 'Вот список задач, нажмите на интересующую чтобы узнать подробнее:'
        # records,e = mydb.GetTasksAll()
        records, e = mydb.GetTasksAll()

        keyboard = telebot.types.InlineKeyboardMarkup()
        i = 0
        for record in records:
            button = telebot.types.InlineKeyboardButton(text=str(records[i]["id"]) + ": " + str(records[i]["title"]), callback_data=str(records[i]["id"])+'GetAll', align="left")
            keyboard.row(button)
            i += 1

        # Отправляем сообщение с клавиатурой пользователю
        bot.send_message(message.chat.id, reply, reply_markup=keyboard)



@bot.message_handler(commands=['mychatid'])
def MyChatid(message):
    reply = message.chat.id
    reply = str(reply)
    bot.send_message(message.chat.id, reply, parse_mode='html')

@bot.message_handler(commands=['gettasks'])
def GetTasks(message):
    reply = 'Вот список задач, нажмите на интересующую чтобы узнать подробнее:'
    #records,e = mydb.GetTasksAll()
    records, e = mydb.GetFreeTasks(message.chat.id)

    keyboard = telebot.types.InlineKeyboardMarkup()
    i = 0
    for record in records:
        button = telebot.types.InlineKeyboardButton(text=str(records[i]["id"])+": "+str(records[i]["title"]), callback_data=str(records[i]["id"])+"GetTask", align="left")
        keyboard.row(button)
        i += 1

    # Отправляем сообщение с клавиатурой пользователю
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)

@bot.message_handler(commands=['getexcel'])
def GetExcel(message):
    data, e = mydb.GetAllData()
    columns = ['id', 'name', 'lastname', 'group_number', 'course', 'chatid', 'task_id', 'title', 'body',
               'task_course',
               'max']
    # transpose .T Если перевернуло
    df = pd.DataFrame(data=data, columns=columns)
    df.to_excel('Itog.xlsx', index=False)
    bot.send_document(message.chat.id, open("Itog.xlsx", "rb"))

#AddStudent('name', 'lastname', 'group_number', course, 'chatid')
@bot.message_handler(commands=['reg'])
def reg_start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_lastname, name)
def get_lastname(message, name):
    lastname = message.text
    bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Укажите курс как целое число.')
    bot.send_message(message.from_user.id, 'На каком ты курсе?')
    bot.register_next_step_handler(message, get_course, name, lastname)
def get_course(message, name, lastname):
    #Надо придумать как обработать ошибку, except и catch того рот ебали, не работает
    course = message.text  # проверяем, что введено корректно
    bot.send_message(message.from_user.id, 'Цифрами, пожалуйста. Укажите номер группы как целое число.')
    bot.send_message(message.from_user.id, 'Какая у тебя группа?')
    bot.register_next_step_handler(message, get_group, name, lastname, course)

def get_group(message, name, lastname, course):
    group = message.text
    reply = message.chat.id
    chatid = int(reply)

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data=f'yes-reg_{name}_{lastname}_{group}_{course}_{chatid}')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no-reg')
    keyboard.add(key_yes, key_no)

    question = 'Ты учишься на '+str(course)+' курсе\n'+'Твоя группа - '+str(group)+'\nТебя зовут '+name+' '+lastname+'?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.message_handler(commands=['addadmin'])
def AddAdmin(message):
    isadmin = mydb.IsAdmin(message.chat.id)
    if (isadmin == True):
        e = mydb.IsAdmin(message.chat.id)
        if (e!=None):
            bot.send_message(message.from_user.id, str(e))
        else:
            reply = "Готово!"
            bot.send_message(message.from_user.id, reply)
    else:
        reply = "Только администраторы могут добавлять администраторов"
        bot.send_message(message.from_user.id, reply)

@bot.message_handler()#tol'ko vnizu
def info(message):
    bot.reply_to(message, "Я тебя не понимать 「(°ヘ°) \n Используй стандартные команды бота")

    bot.reply_to(message, "Я тебя не понимать 「(°ヘ°) \nИспользуй стандартные команды бота \n/help")
#That is all Commands



@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     if (function_call.data.replace('GetAll','').isdigit()):
        taskid = int(function_call.data.replace('GetAll', ''))
        array = mydb.GetBodyOfTask(taskid)
        data_tuple = array[0]
        data_list = data_tuple[0]
        title = data_list["title"]
        body = data_list["body"]
        left, e = mydb.NumberOfSeatsLeft(taskid)
        text = "<b>" + title + "</b>\n" + body
        reply = "Выбрано задание: " + str(taskid) + text + "\n\n\n Свободных мест: " + str(left)
        bot.send_message(function_call.message.chat.id, reply,  parse_mode='html')
        bot.answer_callback_query(function_call.id)

     elif function_call.data.replace('GetTask','').isdigit():
        taskid = int(function_call.data.replace('GetTask', ''))
        array = mydb.GetBodyOfTask(taskid)
        data_tuple = array[0]
        data_list = data_tuple[0]
        title = data_list["title"]
        body = data_list["body"]
        left, e = mydb.NumberOfSeatsLeft(taskid)
        text = "<b>" + title + "</b>\n" + body
        reply = "Задание: " + str(taskid) + text + "\n\n\n Свободных мест: " + str(left)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Принять", callback_data="WantIt" + str(taskid)))
        bot.send_message(function_call.message.chat.id, reply,  parse_mode='html', reply_markup=markup)
        bot.answer_callback_query(function_call.id)

     elif "UUID" in function_call.data:
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
         result = mydb.AssignTask(function_call.message.chat.id, numtask)
         if result != None:
             result = str(result)
             bot.reply_to(function_call.message, result)
         else:
             result = "Готово!"
             bot.reply_to(function_call.message, result)

     elif ('newtaskblet' in function_call.data):
         task_id = function_call.data.replace("newtaskblet,", '')
         title = tasks[task_id]['title']
         course = tasks[task_id]['course']
         maximum = tasks[task_id]['maximum']
         body = tasks[task_id]['body']
             #сюда надо передать переменные из функции
         chatid = function_call.message.chat.id
         isadmin = mydb.IsAdmin(chatid)
         if (maximum.isdigit()) and (course.isdigit()):
             gmax = int(maximum)
             gcourse = int(course)
             if (isadmin == True):
                 mydb.NewTask(title, body, int(gcourse), int(maximum))
                 reply = "Готово!"
             else:
                 reply = "У вас нет прав администратора."
             bot.send_message(function_call.message.chat.id, reply)
 #def callback_worker(call, name=None, lastname=None, group=None, course=None, chatid=None):
     elif 'yes-reg' in function_call.data:
        _, name, lastname, group, course, chatid = function_call.data.split('_')
        result = mydb.AddStudent(name, lastname, group, course, chatid)
        bot.send_message(function_call.message.chat.id, 'Запомню : )')
     elif 'no-reg' == function_call.data:# переспрашиваем
        bot.send_message(function_call.message.chat.id, 'Давай проведём регистрацию заново. Введи /reg')



bot.infinity_polling() #For permonent working
