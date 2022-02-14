from telegram.ext import Updater, CommandHandler

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(update, comtext):
    print("Вызван /start")

def main():
    mybot = Updater("5220783049:AAGzNdxYfqVdQaAaTr2Eicm-JG1XC35IGWg", use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    mybot.start_polling()
    mybot.idle()

main()