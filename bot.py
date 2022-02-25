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
players = {}

class CityGamePlayer:
    def __init__(self):
        self.city_list = {
            'А': ['Армавир', 'Архангельск', 'Альметьевск'],
            'К': ['Калуга', 'Коломна'],
            'М': ['Москва'],
            'Р': ['Рыбинск']
        }
        self.used_cities = []
        self.last_letter = None


    def check_used(self, city):
        return city in self.used_cities

    
    def check_if_correct(self, city):
        if city[0] != self.last_letter:
            return self.last_letter        


    def check_known(self, city):
        if not city[0] in self.city_list.keys():
            return False

        cities_by_letter = self.city_list[city[0]]
        if not city in cities_by_letter:
            return False

        cities_by_letter.remove(city)
        self.used_cities.append(city)
        self.last_letter = city[-1].upper()
        return True        

    
    def find_answer(self):
        city = self.city_list[self.last_letter].pop()        
        self.last_letter = city[-1].upper()
        return city
        

    def check_is_finish(self):   
        return not self.city_list[self.last_letter]             


def check_input(update):
    user_text = update.message.text.split()[1:]
    filtered_text = [word for word in user_text if word.isalpha()]
    if len(filtered_text) != 1:        
        return    
    return filtered_text[0].capitalize()


def get_city(update, context):    
    user_city = check_input(update)    
    if not user_city:
        update.message.reply_text('Write one city')
        return
    
    chat_id = update.message.chat['id']
    if not chat_id in players.keys():
        players[chat_id] = CityGamePlayer()
    
    player = players[chat_id]

    correct_input = player.check_if_correct(user_city)
    if correct_input:
        update.message.reply_text(f'City name should start with "{correct_input}"')
        return
    
    if player.check_used(user_city):
        update.message.reply_text('This city was used')
        return

    if not player.check_known(user_city):
        update.message.reply_text('I do not know this city')
        return
    
    if player.check_is_finish():
        players.pop(chat_id)
        update.message.reply_text('You win!')
        return

    answer = player.find_answer()
    update.message.reply_text(answer)   
    logger.info(player.city_list) 
    logger.info(player.used_cities) 


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
    dp.add_handler(CommandHandler("city", get_city))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
