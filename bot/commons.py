import configparser
import bbot

settings = configparser.ConfigParser()
settings.read('settings.ini')

bot = bbot.BBot(settings['bot']['api_key'])
bot.about = "Get Cashu by Lightining Address payment"
bot.owner = "SatsContact"
bot.after_help = "help"

""" redis initialization """
from db import *

