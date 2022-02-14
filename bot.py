import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(filename="bot.log", level=logging.INFO)

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(update, comtext):
    print("start acted")
    update.message.reply_text("Hi!")

def main():
    mybot = Updater("5220783049:AAGzNdxYfqVdQaAaTr2Eicm-JG1XC35IGWg", use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

main()