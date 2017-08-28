# -*- coding: utf-8 -*-
'''
Script:
    myrss.py
Description:
    Telegram Bot that let you subscribe and follow customs RSS Feeds.
Author:
    Jose Rios Rubio
Creation date:
    23/08/2017
Last modified date:
    28/08/2017
Version:
    0.3.0
'''

####################################################################################################

### Imported modules ###
from os import path
from collections import OrderedDict
from telegram import MessageEntity, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, \
                         ConversationHandler, CallbackQueryHandler

import TSjson
from constants import CONST, TEXT

####################################################################################################

### Globals ###


####################################################################################################

### Functions ###
def signup_user(update):
    '''Function for sign-up a user in the system (add to users list file)'''
    # Initial user data for users list file and chat feeds file
    usr_data = OrderedDict([])
    # Set user data for users list json file
    usr_data['Name'] = update.message.from_user.name
    usr_data['User_id'] = update.message.from_user.id
    usr_data['Sign_date'] = (update.message.date).now().strftime('%Y-%m-%d %H:%M:%S')
    usr_data['Chats'] = []
    # Create TSjson object for each file (list of users and chat feeds) and write on them the data
    fjson_usr_list = TSjson.TSjson(CONST['USERS_LIST_FILE'])
    fjson_usr_list.write_content(usr_data)


def user_is_signedup(user_id):
    '''Function to check if a user is signed-up in the system (if exist in the user list file)'''
    # If users list file exists, search for the user by ID and return if the user is in the file
    signedup = False
    if path.exists(CONST['USERS_LIST_FILE']):
        fjson_usr_list = TSjson.TSjson(CONST['USERS_LIST_FILE'])
        search_result = fjson_usr_list.search_by_uide(user_id, 'User_id')
        if search_result['found']:
            signedup = True
    return signedup


def subscribed(chat_id, feed_url):
    '''Function to check if a chat is already subscribed to the provided feed'''
    # Search for the feed url in chat feeds file and return if the url is in the file
    _subscribed = False
    chat_file = '{}/{}.json'.format(CONST['CHATS_DIR'], chat_id)
    if path.exists(chat_file):
        fjson_usr_feeds = TSjson.TSjson(chat_file)
        subs_feeds = fjson_usr_feeds.read_content()
        if subs_feeds:
            subs_feeds = subs_feeds[0]
            for feed in subs_feeds['Feeds']:
                if feed_url == feed:
                    _subscribed = True
    return _subscribed


def add_feed(user_id, chat_id, feed_url):
    '''Function to add (subscribe) a new url feed to the chat feeds file'''
    # Read user chats and add the actual chat to it
    fjson_usr_list = TSjson.TSjson(CONST['USERS_LIST_FILE'])
    usr_list = fjson_usr_list.read_content()
    for usr in usr_list:
        if usr['User_id'] == user_id:
            usr_chats = usr['Chats']
            if chat_id not in usr_chats:
                usr['Chats'].append(chat_id)
                fjson_usr_list.update(usr, 'User_id')
    # Read chat feeds file and add the new feed url to it
    fjson_usr_feeds = TSjson.TSjson('{}/{}.json'.format(CONST['CHATS_DIR'], chat_id))
    subs_feeds = fjson_usr_feeds.read_content()
    if subs_feeds:
        subs_feeds = subs_feeds[0]
        subs_feeds['Feeds'].append(feed_url)
        fjson_usr_feeds.update(subs_feeds, 'Chat_id')
    else:
        usr_feeds = OrderedDict([])
        usr_feeds['Chat_id'] = chat_id
        usr_feeds['Feeds'] = [feed_url]
        fjson_usr_feeds.write_content(usr_feeds)

####################################################################################################

### Received commands handlers ###
def cmd_start(bot, update):
    '''/start command handler'''
    update.message.reply_text(TEXT['START']) # Bot reply


def cmd_help(bot, update):
    '''/help command handler'''
    update.message.reply_text(TEXT['HELP']) # Bot reply


def cmd_signup(bot, update, args):
    '''/signup command handler'''
    if len(args) == 1: # If 1 argument has been provided
        if not user_is_signedup(update.message.from_user.id): # If the user is not signed-up
            key_provided = args[0] # Get the key provided (argument)
            if key_provided == CONST['REG_KEY']: # If Key provided is the correct and actual one
                signup_user(update) # Sign-up the user (add-to/create json file)
                update.message.reply_text(TEXT['SIGNUP_SUCCESS']) # Bot reply
            else: # Wrong Key provided
                update.message.reply_text(TEXT['SIGNUP_FAIL']) # Bot reply
        else: # The user is alredy signed-up
            update.message.reply_text(TEXT['SIGNUP_EXIST_USER']) # Bot reply
    else: # No argument or more than 1 argument provided
        update.message.reply_text(TEXT['SIGNUP_NOT_ARG']) # Bot reply


def cmd_add(bot, update, args):
    '''/add command handler'''
    user_id = update.message.from_user.id # Get the user id
    chat_id = update.message.chat_id # Get the chat id
    if user_is_signedup(user_id): # If the user is sign-up
        if len(args) == 1: # If 1 argument has been provided
            feed_url = args[0] # Get the feed url provided (argument)
            if not subscribed(chat_id, feed_url): # If user is not already subscribed to that feed
                feed = feedparser.parse(feed_url) # Get the feedparse of that feed url
                if feed['entries']: # If any entry
                    add_feed(user_id, chat_id, feed_url) # Add the feed url to the chat feeds file
                    bot_response = '{}{}'.format(TEXT['ADD_FEED'], feed_url) # Bot response
                else: # No entries in that feed
                    bot_response = '{}'.format(TEXT['ADD_NO_ENTRIES']) # Bot response
                update.message.reply_text(bot_response) # Bot reply
            else: # Already subscribed to that feed
                update.message.reply_text(TEXT['ADD_ALREADY_FEED']) # Bot reply
        else: # No argument or more than 1 argument provided
            update.message.reply_text(TEXT['ADD_NOT_ARG']) # Bot reply
    else: # The user is not allowed (needs to sign-up)
        update.message.reply_text(TEXT['CMD_NOT_ALLOW']) # Bot reply

####################################################################################################

### Main function ###
def main():
    ''' Main Function'''
    # Create Bot event handler and get the dispatcher
    updater = Updater(CONST['TOKEN'])
    disp = updater.dispatcher
    # Set the received commands handlers into the dispatcher
    disp.add_handler(CommandHandler("start", cmd_start))
    disp.add_handler(CommandHandler("help", cmd_help))
    disp.add_handler(CommandHandler("signup", cmd_signup, pass_args=True))
    disp.add_handler(CommandHandler("add", cmd_add, pass_args=True))
    # Start the Bot polling ignoring pending messages (clean=True)
    updater.start_polling(clean=True)
    # Set the bot to idle (actual main-thread stops and wait for incoming messages for the handlers)
    updater.idle()

####################################################################################################

### Execute the main function if the file is not an imported module ###
if __name__ == '__main__':
    main()
