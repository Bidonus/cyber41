#coding:utf-8
import telebot, config
from datetime import date
import random
import time
import os

#----------------------------------------------------------------------------------
#///////////////////////////////Связь с ботом//////////////////////////////////////
#----------------------------------------------------------------------------------
a = 42

bot = telebot.TeleBot(config.token)


#----------------------------------------------------------------------------------
#//////////////////////Логгирование и доп функции//////////////////////////////////
#----------------------------------------------------------------------------------


def log(message, answer):
    print("\n --------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. {{id = {2}}} \n TEXT = {3}".format(message.from_user.first_name,
                                                                  message.from_user.last_name,
                                                                  str(message.from_user.id),
                                                                  message.text))
    print(answer)




#----------------------------------------------------------------------------------
#//////////////////////Декораторы основных команд//////////////////////////////////
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    #user_markup.row('/start', '/stop')
    user_markup.row('Фото расписания', 'Рандом стикер')
    user_markup.row('Хелпа', 'Пары на завтра')
    user_markup.row('/stop', '/mod')
    bot.send_message(message.chat.id, "Стартуем", reply_markup=user_markup)

#----------------------------------------------------------------------------------

@bot.message_handler(commands=['stop'])
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Чтобы вызвать меня - набери /start", reply_markup=hide_markup)

#------------------------------------------------------------------------------------

@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, config.help_message)

#-----------------------------Калькулятор модуля-------------------------------------

@bot.message_handler(commands=['mod'])
def modul(message):
    msg = bot.reply_to(message, "Введи 3 числа через пробел (число, степень, модуль)")
    bot.register_next_step_handler(msg, modul_calculate)
def modul_calculate(message):
    a = message.text
    print(a)
    counts = a.split()
    print(counts)
    result = (int(counts[0])**int(counts[1]))%int(counts[2])
    print(result)
    bot.send_message(message.chat.id, "Остаток по модулю = " +str(result))

#---------------------------Проверка на стикер--------------------------------------

@bot.message_handler(content_types=['sticker'])
def handle_text(message):
    answer = 'sticker received'
    log(message,answer)



#----------------------------------------------------------------------------------
#//////////////////////Декоратор анализа текста////////////////////////////////////
#----------------------------------------------------------------------------------



@bot.message_handler(content_types=["text"])
def handle_text(message):

# -----------------------Пасхалка на желдакова--------------------------------------

    if message.text in config.jeldak:
        answer = "Jeldak answer completed"
        log(message, answer)
        bot.send_message(message.chat.id, config.jeldak_message)

#-----------------------Функция фото расписания--------------------------------------

    elif message.text == "Фото расписания":
        answer = "Photot shared"
        directory = "E:/cyber_bot/cyber41/photos"
        all_files_in_dir = os.listdir(directory)
        print(all_files_in_dir)
        for file in all_files_in_dir:
            img = open(directory + '/' + file, 'rb')
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, img)
            img.close()

# -----------------------Функция рандомного стикера----------------------------------

    elif message.text == "Рандом стикер":
        answer = "Sticker sent"
        stick = random.choice(config.sticker_pack_ids)
        log(message, answer)
        bot.send_sticker(message.chat.id, stick)


#------------------------Функция вывода расписания на завтра--------------------------

    elif message.text.lower() in config.shedule_ask:
        send = config.wdays[time.localtime().tm_wday+1]
        print(send)
        weekNumber = date.today().isocalendar()[1]
        #vivod = []
        print("weeknumber is " +str(weekNumber))
        if weekNumber%2 == 0:
            if send in config.shedule['2t']:
                print(config.shedule['2t'][send])
                for i in config.shedule['2t'][send]:
                    bot.send_message(message.chat.id, config.shedule['2t'][send][i])
        elif weekNumber%2 != 0:
            if send in config.shedule['1t']:
                print(config.shedule['1t'][send])
                for i in config.shedule['1t'][send]:
                    bot.send_message(message.chat.id, config.shedule['1t'][send][i])

#-----------------------------Вывод хелпы-------------------------------------------

    elif message.text.lower() == "хелпа":
        print("HELP CALLED")
        bot.send_message(message.chat.id, config.help_message)

#---------------------------------Молчание------------------------------------------

    else:
        print('nothing happens')


#---------------------------Бесконечная работа--------------------------------------

bot.polling(none_stop=True)




























































                
























    












