import telebot
from dotenv import load_dotenv
import os
import requests

API_KEY = '5134259994:AAFH9cJAWEXC3vRD91U5LB_NixEwLtT45hU'

bot = telebot.TeleBot(API_KEY)


def get_url():
    contents = requests.get('https://thatcopy.pw/catapi/rest/').json()
    image_url = contents['url']
    return image_url


def get_fact():
    contents = requests.get(
        'https://cat-fact.herokuapp.com/facts/random?animal_type=dog&amount=1'
    ).json()
    fact = contents['text']
    if len(fact) < 10:
        return get_fact()
    return fact


@bot.message_handler(commands=['greet', 'start'])
def greet(message):
    msg = '''Hello, how are you?
  Send /pic to get a Sun's image.
  Send /fact to get random Dog Fact.'''
    bot.send_message(message.chat.id, msg)


counter = 0


def get_sun_pic(message):
    global counter
    for i in range(2):
        counter = counter + 1
        if (counter > 9):
            msg = "Finish"
            bot.send_message(message.chat.id, msg)
            return
        filename = 'sun/sun (%s).jpg' % counter
        bot.send_photo(message.chat.id, open(filename, 'rb'))
    msg = "Want more? Press /pic"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['pic'])
@bot.message_handler(regexp=r'pic')
def pic(message):
    get_sun_pic(message)


@bot.message_handler(commands=['fact'])
@bot.message_handler(regexp=r'fact')
def fact(message):
    fact = get_fact()
    bot.send_message(message.chat.id, fact)


@bot.message_handler(func=lambda m: True)
def repeat(message):
    bot.send_message(message.chat.id, message.text)


def main():
    bot.polling()


if __name__ == '__main__':
    main()
