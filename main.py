#coding:utf-8
import telebot, config
from telegram import update
from datetime import date
import random
import time
import os, re
import urllib.request, urllib.parse,urllib
import requests
from googleapiclient.discovery import build
import pprint
from telebot import types


#----------------------------------------------------------------------------------
#///////////////////////////////Связь с ботом//////////////////////////////////////
#----------------------------------------------------------------------------------


bot = telebot.TeleBot(config.token)
service = build("customsearch", "v1", developerKey=config.CUSTOM_SEARCH_TOKEN)



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

#-------------------------------Старт функция--------------------------------------


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    #user_markup.row('/start', '/stop')
    user_markup.row('Фото расписания', 'Рандом стикер')
    user_markup.row('Хелпа', 'Пары на завтра')
    user_markup.row('Остаток по модулю')
    #user_markup.row('Закрыть панель', 'Остаток по модулю')
    bot.send_message(message.chat.id, "Здарова братва !", reply_markup=user_markup)
    bot.send_message(message.chat.id, "Для начала добавь меня в личные диалоги чтобы я мог отсылать тебе информацию \n @Cyber41_bot <-- Жми !")



#------------------------------Стоп функция-----------------------------------------


@bot.message_handler(commands=['stopthisshit'])
def stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Чтобы вызвать панель кнопок - набери /start", reply_markup=hide_markup)


#@bot.message_handler(commands=['stop'])
#def stop(message):
#    hide_markup = telebot.types.ReplyKeyboardRemove()
#    bot.send_message(message.chat.id, "Чтобы вызвать панель кнопок - набери /start", reply_markup=hide_markup)



#------------------------------Хелп функция------------------------------------------


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, config.help_message)



#-----------------------------Инлайн поискового бота---------------------------------



@bot.inline_handler(lambda query: len(query.query) > 3)
def gle(inline_query):
    response = []  # store list of responses from the server
    try:

        results = service.cse().list(q=inline_query.query, cx=config.CSE_ID).execute()  # fetch result for the query.

        if results:
            # if result is found for the query

            resp = types.InlineQueryResultArticle('1', 'Топ результатов',
                                                  types.InputTextMessageContent('Топ 5 результатов: '))
            response.append(resp)
            item = results.get('items')

            for i in range(0, 5, 1):
                print(item[i])
                resp = types.InlineQueryResultArticle(str(i+2), item[i]["Заголовок"],
                                                      types.InputTextMessageContent(
                                                               '*'+ item[i]["Заголовок"] + '*\n'
                                                                + item[i]["snippet"] + '\n'
                                                                + '[Смотреть больше]('+item[i]['link']+') ', parse_mode='Markdown'),
                                                      url=item[i]['link'],
                                                      description=item[i]['snippet'][:100])
                response.append(resp)
        else:
            resp = types.InlineQueryResultArticle('1', 'Братан, очень сложный запрос, сделай проще?',
                                                  types.InputTextMessageContent('Ещё раз поищи используя @thesearchbot'))
            response.append(resp)
        # print(response, "\n")

    except Exception as e:
        if str(e).__contains__('403'):
            # if daily maximum search result exceeds.
            resp = types.InlineQueryResultArticle('1', 'Сорян, максимум за день',
                                                  types.InputTextMessageContent(
                                                      'Лимит за день исчерпан порпобуй завтра :)'))
        else:
            resp = types.InlineQueryResultArticle('1', 'Не понял тебя \n' +
                                                  'try again?',
                                                  types.InputTextMessageContent('Ещё раз поищи с @thesearchbot'))
        response.append(resp)

        print("Exception: ", str(e))
    finally:
        # respond to the inline query
        bot.answer_inline_query(inline_query.id, response, cache_time=1)



#-----------------------------Калькулятор модуля-------------------------------------


@bot.message_handler(commands=['mod'])
def modul(message):
    msg = bot.reply_to(message, "Введи 3 числа через пробел (число, степень, модуль)")
    bot.register_next_step_handler(msg, modul_calculate)
def modul_calculate(message):
    a = message.text
    print(a)
    counts = a.split()
    for i in counts:
        if i.isdigit():
            if int(i) > 0:
                print(counts)
                result = (int(counts[0])**int(counts[1]))%int(counts[2])
                print(result)
                bot.send_message(message.chat.id, "Остаток по модулю = " + str(result))
                break
            else:
                print("ne chislo")
                bot.send_message(message.chat.id, "Начни заново и введи числа, без нулей и букв!")
                break
        else:
            print("ne chislo")
            bot.send_message(message.chat.id, "Начни заново и введи числа, без нулей и букв!")
            break



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
        answer = "Photo shared"
        directory = "C:/Users/ivan.savarin/Documents/GitHub/cyber41/photos"
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


    elif message.text.lower() == "остаток по модулю":
        answer = "модуль включен"
        log(message, answer)
        modul(message)



#    elif message.text.lower() == "закрыть панель":
#        answer = "закрыта пенель"
#        log(message, answer)
#        stop(message)


#------------------------Функция вывода расписания на завтра--------------------------

    elif message.text.lower() in config.shedule_ask:
        send = config.wdays[time.localtime().tm_wday+1]
        print(send)
        weekNumber = date.today().isocalendar()[1]
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
        bot.send_message(message.from_user.id, config.help_message)

#---------------------------------Молчание------------------------------------------

    else:
        print('nothing happens')


#---------------------------Бесконечная работа--------------------------------------

bot.polling(none_stop=True, interval=0)