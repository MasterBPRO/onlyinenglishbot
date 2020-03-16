import telebot
import regex as re
import os
from googletrans import Translator
from flask import Flask, request



TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
server = Flask(__name__)
bot = telebot.TeleBot(TOKEN)
translator = Translator()


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, "OK!")


@bot.message_handler(content_types=["text"])
def start_conv(message):
    """Функция для ответа пользователю"""
    if get_lang(message.text):
        try:
            if message.from_user.first_name != "Telegram":
                bot.send_message(message.chat.id, text="Dear {}! \n\nNow you are connected with <b>NASA</b>, please,  gain your ideas and whatever you want to say and write it in <b>English</b> right here. \n\nThank you for your understanding!".format(user_mention(message.from_user)), parse_mode="html")
                bot.delete_message(message.chat.id, message.message_id)
        except Exception as A:
            print("[LOG]", A)


def get_lang(text):
    """Функция для определения языка текста"""
    clean = clean_message(text)
    result = translator.detect(clean).lang
    if result == "en":
        return False
    else:
        return True


def clean_message(text):
    """Функуия для очистки текста от посторонних символов"""
    return re.sub(r'[^\w\s]', '', '{}'.format(text))


def user_mention(user):
    """Функция для определения наличия @username"""
    return "@" + user.username if user.username else user.first_name


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
