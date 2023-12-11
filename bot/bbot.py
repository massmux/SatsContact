from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Chat
from telebot import formatting
import time, threading, schedule
from functools import wraps
import pprint
import re
from telebot import apihelper, util

apihelper.ENABLE_MIDDLEWARE = True

pp = pprint.PrettyPrinter(indent=4)

class BBot(TeleBot):
    """ Wrapper class of the old botogram library with the new TeleBot/pyTelegramBotAPI """

    def command(self, name, hidden=True):
        """ Wrapper decorator @bot.command """
        return super(BBot, self).message_handler(commands=[name])
    
    def callback(self, name):
        """ Wrapper decorator @bot.callback 
        The Lamda function recall a filter based on a filter of the button data. Check the first part
        of the button against the parameter passed on the callback itself as name """
        return self.callback_query_handler(func=lambda call: call.data if (name == call.data.split(":")[0]) else None)
    
    def timer(self, seconds):
        """ New decorator @bot.timer(s)
        Based upon https://www.geeksforgeeks.org/decorators-with-parameters-in-python/ """
        def wrapper(func):
            def inner_wrapper(bot):
                func(bot)
            schedule.every(seconds).seconds.do(inner_wrapper, self)
            return inner_wrapper
        return wrapper
    
    def chat(self, chat_to_specific_users_ids = []):
        """ New method to send a message to a specific user
        Should be used as `chat = bot.chat(userid)` because it return the object itself in order to allow the method
        `bot.send()` next """
        return Chat(self, chat_to_specific_users_ids)

class ButtonsRow:
    """ Wrapper class of the old botogram ButtonsRow object, recreated with the new TeleBot/pyTelegramBotAPI """

    def __init__(self):
        self._content = []

    def url(self, label, url):
        """ Url Buttons """
        self._content.append(InlineKeyboardButton(label, url=url))

    def callback(self, label, callback, data=None):
        """ Callback Buttons """
        def generate_callback_data():
            """ Create the callback button with a string with the fields `callback_actions_name:buttons_data`
            The `callback_actions_name` parts will be used to filter the callback to call, and the second one `buttons_data` is the 
            data that will be passed to the function decorated """
            return InlineKeyboardButton(label, callback_data=str(callback) + ":" + str(data))
        self._content.append(generate_callback_data())

    def getrow(self, i):
        """ Return the line content """
        return self._content[i]

class Buttons:
    """ Wrapper class of the old botogram Buttons object, recreated with the new TeleBot/pyTelegramBotAPI """

    def __init__(self):
        self._rows = {}
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 3

    def __getitem__(self, index):
        """ This is needed in order to setup the button row before to render it """
        if index not in self._rows:
            self._rows[index] = ButtonsRow()
        return self._rows[index]

    def getbuttons(self, chat=None):
        """ This is needed in order get the buttons created and attach if on the markup """
        for i, value in self._rows.items():
            rows = []
            for r in range(self.markup.row_width):
                try:
                    rows.append(value.getrow(r))
                except IndexError:
                    pass
            self.markup.add(*rows)
        return self.markup

class Chat:
    """ Wrapper class of the old botogram Chat object, recreated with the new TeleBot/pyTelegramBotAPI """

    def __init__(self, bot, chat):
        """ You can add here additional attributes used for botogram compatibility """
        self.bot = bot
        self.chat = chat

    def __getattr__(self, name):
        """ This magic method return all the others attributes of the Chat object from TeleBot/pyTelegramBotAPI """
        try:
            if ( (type(self.chat) != list) and (type(self.chat) != int) ):
                return getattr(self.chat, name)
        except AttributeError as e:
            raise AttributeError("Child' object has no attribute '%s'" % name)
    
    def send(self, label, preview=False, attach=None, syntax="markdown"):
        """ New method to send a message. Should be used as `chat.send(...)`
        If a list is passed as parameter of send() method, we sent the message only to the first element, as 
        did before. Obviously if we want to send the message to all the elements of the list we need to cycle over it and 
        choose what return
        """
        parse_mode = None
        reply_markup = None
        if (syntax == "markdown"):
            label = formatting.format_text(label)
            parse_mode = 'Markdown'
        if attach is not None:
            reply_markup = attach.getbuttons()
        if (type(self.chat) == list):
            to = self.chat[0]
        elif (type(self.chat) == int or type(self.chat) == str):
            to = self.chat
        else:
            to = self.chat.id            
        return Message(self.bot, self.bot.send_message(to, label, parse_mode=parse_mode, reply_markup=reply_markup))

    def send_photo(self, image, caption=None, syntax=None):
        """ New method to send a photo. Should be used as `chat.send_photo(...)`
        If a list is passed as parameter of send_photo() method, we sent the message only to the first element, as 
        did before. Obviously if we want to send the message to all the elements of the list we need to cycle over it and 
        choose what return
        """
        parse_mode = None
        if (syntax == "markdown"):
            caption = formatting.format_text(caption)
            parse_mode = 'Markdown'
        if type(self.chat) == list:
            to = self.chat[0]
        elif (type(self.chat) == int or type(self.chat) == str):
            to = self.chat
        else:
            to = self.chat.id
        return self.bot.send_photo(to, photo=open(image, 'rb'), caption=caption, parse_mode=parse_mode)
    
    def send_file(self, doc, caption=None, syntax=None):
        """ New method to send a generic file. Should be used as `chat.send_file(...)`
        If a list is passed as parameter of send_file() method, we sent the message only to the first element, as 
        did before. Obviously if we want to send the message to all the elements of the list we need to cycle over it and 
        choose what return
        """
        parse_mode = None
        if (syntax == "markdown"):
            caption = formatting.format_text(caption)
            parse_mode = 'Markdown'
        if type(self.chat) == list:
            to = self.chat[0]
        elif (type(self.chat) == int or type(self.chat) == str):
            to = self.chat
        else:
            to = self.chat.id
        return self.bot.send_document(to, document=open(doc, 'rb'), caption=caption, parse_mode=parse_mode)

class Message:
    """ Wrapper class of the old botogram Message object, recreated with the new TeleBot/pyTelegramBotAPI """

    def __init__(self, bot, message):
        """ You can add here additional attributes used for botogram compatibility """
        self.bot = bot
        self.message = message
        self.id = message.message_id
        self.sender = message.from_user
        self.username = message.from_user.username
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name

    def __getattr__(self, name):
        """ This magic method return all the others attributes of the Message object from TeleBot/pyTelegramBotAPI """
        try:
            return getattr(self.message, name)
        except AttributeError as e:
            raise AttributeError("Child' object has no attribute '%s'" % name)

    def edit(self, new_text, syntax=None):
        """ New method to edit a message should be used as message.edit() """
        parse_mode = None
        if (syntax=="markdown"):
            new_text = formatting.format_text(new_text)
            parse_mode = 'Markdown'
        return self.bot.edit_message_text(chat_id = self.message.chat.id, message_id = self.message.id, text=new_text, parse_mode=parse_mode)
    
    def delete(self):
        """ New method to delete a message should be used as message.delete() """
        return self.bot.delete_message(self.message.chat.id,self.message_id)

class Args:
    """ This class is used to retrieve args passed to a command. """

    def __init__(self, message):
        self.args = util.extract_arguments(message.text)
        self.message = message

    def GetArgs(self):
        """ This is the method that retrieve arguments from a command send on chat. By default check with the argument separated by space.
        If found retrieve an array of this values. Otherwise if the command start with /cmd_ split the arguments with the `_` delimiter
        and retrive an array of this values on the same way
        """
        if (self.args != "" and self.args != None):
            return self.args.split()
        elif( self.message.text.startswith("/cmd_") ):            
            return self.message.text.split("_")[2:]        
        else:
            return []

class Data:
    """ This class is used to retrieve `data` passed with a callback. """

    def __init__(self, data):
        self.data = data
    def GetData(self):
        """ Tihs is the method that return the specific data passed from a button of the callback """ 
        if (self.data != "" and self.data != None):
            return self.data.split(":")[-1]
        else:
            return ""


