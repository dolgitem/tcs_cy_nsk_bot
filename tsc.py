import requests
import json
import telebot
import time

import os
TOKEN = os.environ.get('TOKEN', None)

CHANNEL_NAME = '@tcs_piter_cash'

bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=['start', 'go'])
# def start_handler(message):
#     bot.send_message(message.chat.id, 'Буду присылать обновления каждые 5 минут!')
# bot.polling()

url = 'https://api.tinkoff.ru/geo/withdraw/clusters'

currencies = ['USD', 'EUR']

a = 1
while a==1:
# if True:

    bot_response = ""

    for currency in currencies:

        params = {
            'filters' : {
                'showUnavailable': False,
                'currencies': [
                    currency
                ],
                'banks': [
                    'tcs'
                ]
            },

            # ПИТЕР
            'bounds': {
                'bottomLeft': {
                    'lat': 59.81865851138632,
                    'lng': 30.24542629127309
                },
                'topRight': {
                    'lat': 59.88679579775586,
                    'lng': 30.39322673682974
                }
            },
            'zoom': 13

            # НСК
            # 'bounds': {
            #     'bottomLeft': {
            #         'lat': 54.73908113092194,
            #         'lng': 81.42070414453119
            #     },
            #     'topRight': {
            #         'lat': 55.263240661317916,
            #         'lng': 84.49138285546871
            #     }
            # },
            # 'zoom': 9
        }

        params_json = json.dumps(params)

        headers = {'Content-Type': 'application/json'}

        request = requests.post(url, headers=headers, data=params_json)

        response = request.json()

        if response['payload']['clusters']:
            
            bot_response += "---" + str(currency) + "---\n\r"
            bot_response += "\n\r"
            for cluster in response['payload']['clusters']:
                for point in cluster['points']:
                    
                    bot_response += 'Адрес: ' + point['address'] + "\n\r"

                    for limit in point['limits']:
                        if currency == limit['currency']:
                            bot_response +='Валюта: ' + limit['currency'] + "\n\r"
                            bot_response +='Доступно: ' + str(limit['amount']) + "\n\r"
                            bot_response += "\n\r"
        # else:
            # print('Нет '+currency+' в банкаматах')

    bot.send_message(CHANNEL_NAME, bot_response)
    # print(bot_response)

    time.sleep(300)