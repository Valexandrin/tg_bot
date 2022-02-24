import logging
import settings
import ephem
import arrow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def greet_user(update, context):
    text = 'Вызван /start'
    logger.info(text)
    update.message.reply_text(text)


def ask_planet_name(update, context):
    user_text = update.message.text.split()
    current_date = update.message.date
    logger.info(user_text)
    for word in user_text[1:]:        
        word = word.capitalize()                
        if hasattr(ephem, word):        
            planet = getattr(ephem, word)
            planet_info = planet(current_date)
            constellation = ephem.constellation(planet_info)
            update.message.reply_text('{} in constellation {}'.format(word, constellation))              
        else:
            update.message.reply_text('{} did not found'.format(word))
            logger.info('Planet %s not found', word)    
                     

def humanize_ephem_date(ephem_date):
    date = arrow.get(str(ephem_date))
    output_date = date.format('YYYY-MM-DD')    
    future = date.humanize(locale='ru')
    return f'{future} ({output_date})'


def next_full_moon(update, context):    
    logger.info(update.message.text)    
    next_full_moon_date = ephem.next_full_moon(update.message.date)
    msg = humanize_ephem_date(next_full_moon_date)       
    update.message.reply_text(msg)


def word_count(update, context):
    user_text = update.message.text.split()[1:]
    logger.info(user_text)
    if not user_text:
        update.message.reply_text('Nothing to count')
        return
    filtered_text = [word for word in user_text if word.isalpha()]
    update.message.reply_text('Words quantity: {} '.format(len(filtered_text)))   


def talk_to_me(update, context):
    user_text = update.message.text
    logger.info(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    
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
