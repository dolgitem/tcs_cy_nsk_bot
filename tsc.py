import requests
import json
import telebot
import time



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Буду присылать обновления каждые 5 минут!')
bot.polling()

url = 'https://api.tinkoff.ru/geo/withdraw/clusters'

currencies = ['USD', 'EUR']

while True:

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
            'bounds': {
                'bottomLeft': {
                    'lat': 54.73908113092194,
                    'lng': 81.42070414453119
                },
                'topRight': {
                    'lat': 55.263240661317916,
                    'lng': 84.49138285546871
                }
            },
            'zoom': 9
        }

        params_json = json.dumps(params)

        headers = {'Content-Type': 'application/json'}

        request = requests.post(url, headers=headers, data=params_json)

        response = request.json()

        if response['payload']['clusters']:
            print('---' + currency + '---')
            print('')
            for cluster in response['payload']['clusters']:
                for point in cluster['points']:
                    
                    print('Адрес: ' + point['address'])

                    for limit in point['limits']:
                        if currency == limit['currency']:
                            print('Валюта: ' + limit['currency'])
                            print('Доступно: ' + str(limit['amount']))
                            print('')
        else:
            print('Нет '+currency+' в банкаматах')

    time.sleep(300)