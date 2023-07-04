import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot('6323243276:AAFYCmIuRfV3b8U83N4H1oqqdEHZ5-Wc_Do')
from telebot import types


#Commands
@bot.message_handler(commands=['start'])
def startBot(message):
  reply = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\nЭто бот для выдачи задач. Для начала следует пройти регистрацию."
  markup = types.InlineKeyboardMarkup()
  button_registration = types.InlineKeyboardButton(text = 'Регистрация', callback_data='registration')
  markup.add(button_registration)
  bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['GetTask'])
def startBot(message):
    reply = 'Вот список задач, нажмите на интересующую чтобы узнать подробнее:'
    records = [('запись 1', 1), ('запись 2', 2), ('запись 3', 3)]

    buttons = [InlineKeyboardButton(r[0], callback_data=str(r[1])) for r  in records]

    # Создаем объект клавиатуры и добавляем в него кнопки
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)

    # Отправляем сообщение с клавиатурой пользователю
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)

@bot.message_handler(commands=['GetExcel'])



@bot.message_handler()#tol'ko vnizu
def info(message):
    bot.reply_to(message, "Я тебя не понимать 「(°ヘ°) \n Используй стандартные команды бота")
#That is all Commands



#Callback
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
        markup.add(types.InlineKeyboardButton("Нет", callback_data="Nope"), types.InlineKeyboardButton("Принять", callback_data="Ofcourse" + str(numtask)))
        bot.send_message(function_call.message.chat.id, reply, reply_markup=markup)
        bot.answer_callback_query(function_call.id)
     elif function_call.data == "Nope":
         bot.delete_message(chat_id=function_call.message.chat.id, message_id=function_call.message.message_id)
     elif "Ofcourse" in function_call.data:
         numtask = function_call.data.replace("Ofcourse", '')
         #здесь значит надо прихуярить метод привязывания задачки к студенту (Семён, сделай метод для приписывания челу задачки по её номеру numtask)



bot.infinity_polling() #For permonent working