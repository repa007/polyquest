
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
    reply+= "/AllTasks - Вывести все задания из бд\n"
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


@bot.message_handler(commands=['NewTask'])
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
    max = message.text
    reply = "Полноценно опишите задание. Обязательно укажите, куда должен обратиться студент после того как возьмёт задание. "
    bot.send_message(message.chat.id, reply, parse_mode='html')
    bot.register_next_step_handler(message, NewTask_body, course, title, max)

def NewTask_body(message, course, title, max):
    body = message.text
    reply = "Проверьте правильность заполнения."
    reply += "\nЗаголовок: " + title
    reply += "\nДля курса № " + course
    reply += "\nМаксимальное кол-во студентов: " + max
    reply += "\nОписание задания: \n" + body
    keyboard = types.InlineKeyboardMarkup()
    no_nt = types.InlineKeyboardButton(text='Отмена', callback_data='Hide')
    yes_nt = types.InlineKeyboardButton(text='Добавить', callback_data=f'y-nt_{title}_{str(course)}_{str(max)}_{body}')
    keyboard.add(no_nt, yes_nt)
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)






@bot.message_handler(commands=['DeleteTask']) #для отладки
def DeleteTask(message):
    reply,e = mydb.GetTasksAll()
    reply = str(reply)
    bot.send_message(message.chat.id, reply, parse_mode='html')

@bot.message_handler(commands=['MyTasks'])#to do
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

@bot.message_handler(commands=['DeleteTask'])
def delete_task_command_handler(message):
    bot.reply_to(message, "Введите номер задания, которое Вы хотите удалить. Чтобы увидеть список задач введите /AllTask")
    bot.register_next_step_handler(message, delete_task_handler)
def delete_task_handler(message):
    try:
        task_id = int(message.text)
        mydb.DeleteTask(task_id)
        bot.reply_to(message, f"Задание с ID {task_id} было удалено.")
    except ValueError:
        bot.reply_to(message, "Некорректный формат номера задания. Пожалуйста, используйте только цифры для номера задания.")
    except:
        bot.reply_to(message, "Произошла ошибка при удалении задачи.")

@bot.message_handler(commands=['AllTasks'])
def AllTasks(message):
        reply = 'Вот список задач, нажмите на интересующую чтобы узнать подробнее:'
        # records,e = mydb.GetTasksAll()
        records, e = mydb.GetTasksAll()

        keyboard = telebot.types.InlineKeyboardMarkup()
        i = 0
        for record in records:
            button = telebot.types.InlineKeyboardButton(text=str(records[i]["id"]) + ": " + str(records[i]["title"]),
                                                        callback_data=str(records[i]["id"])+'GetAll', align="left")
            keyboard.row(button)
            i += 1

        # Отправляем сообщение с клавиатурой пользователю
        bot.send_message(message.chat.id, reply, reply_markup=keyboard)



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

@bot.message_handler()
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
     if function_call.data == "registration": #to do
        reply = ""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Пойти на хуй?", url="http://go-friend-go.narod.ru/"))
        bot.send_message(function_call.message.chat.id, reply, reply_markup=markup)
        bot.answer_callback_query(function_call.id)

     elif (function_call.data.replace('GetAll','').isdigit()):
        taskid = int(function_call.data.replace('GetAll', ''))
        array = mydb.GetBodyOfTask(taskid)
        data_tuple = array[0]
        data_list = data_tuple[0]
        title = data_list["title"]
        body = data_list["body"]
        text = "<b>" + title + "</b>\n" + body
        reply = "Выбрано задание: " + str(taskid) + text
        bot.send_message(function_call.message.chat.id, reply,  parse_mode='html')
        bot.answer_callback_query(function_call.id)

     elif function_call.data.isdigit():
        taskid = int(function_call.data)
        array = mydb.GetBodyOfTask(taskid)
        data_tuple = array[0]
        data_list = data_tuple[0]
        title = data_list["title"]
        body = data_list["body"]
        left, e = mydb.NumberOfSeatsLeft(taskid)
        text = "<b>" + title + "</b>\n" + body
        reply = "Задание: " + str(taskid) + text + "\n\n\n Свободных мест:" + str(left)
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
         result = mydb.AssignTask(function_call.message.chat.id, numtask)
         if result != None:
             result = str(result)
             bot.reply_to(function_call.message, result)
         else:
             result = "Готово!"
             bot.reply_to(function_call.message, result)

     elif 'y-nt' in function_call.data:
         _, title, course, max, body = function_call.data.split('_')
         chatid = function_call.message.chat.id
         isadmin = mydb.IsAdmin(chatid)
         if (max.isdigit()) and (course.isdigit()):
             max = int(max)
             course = int(max)
             if (isadmin == True):
                 mydb.NewTask(title, body, int(course), int(max))
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