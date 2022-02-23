import logging
import settings
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn',
        'password': 'python'
    }
}


def greet_user(update, context):
    text = 'Вызван /start'
    logger.info(text)
    update.message.reply_text(text)


def ask_planet_name(update, context):
    user_text = update.message.text.split()
    current_date = update.message.date
    logger.info(user_text)
    for word in user_text:        
        word = word.capitalize()        
        try:
            planet = getattr(ephem, word)
            planet_info = planet(current_date)
            constellation = ephem.constellation(planet_info)
            update.message.reply_text('{} in constellation {}'.format(word, constellation))              
        except AttributeError:
            logger.info('Planet %s not found', word)    
                     

def next_full_moon(update, context):    
    logger.info(update.message.text)
    date_time = ephem.next_full_moon(update.message.date)
    update.message.reply_text(str(date_time)[:9])


def word_count(update, context):
    user_text = update.message.text.split()[1:]
    logger.info(user_text)
    if user_text:
        filtered_text = [word for word in user_text if word.isalpha()]
        update.message.reply_text('Words quantity: {} '.format(len(filtered_text)))
        return
    update.message.reply_text('Nothing to count')


def talk_to_me(update, context):
    user_text = update.message.text
    logger.info(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.API_KEY, use_context=True) #request_kwargs=PROXY
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", ask_planet_name))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
