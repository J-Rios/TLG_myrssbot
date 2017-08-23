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
    23/08/2017
Version:
    0.1.0
'''

####################################################################################################

### Imported modules ###
from constants import CONST, TEXT
from telegram import MessageEntity, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, \
                         ConversationHandler, CallbackQueryHandler

####################################################################################################

### Globals ###
# To-Do: Use files to store registration users
user = {
    'NAME' : 'Nobody', # User name
    'ID' : '0000', # User ID
    'SIGNUP_DATE' : '00/00/0000' # Sign-up date
}

####################################################################################################

### Functions ###


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
    if update.message.from_user.id != user['ID']: # If the user is not signed-up
        if len(args) == 1: # If 1 argument has been provided
            key_provided = args[0] # Get the key provided (argument)
            if key_provided == CONST['REG_KEY']: # If Key provided is the correct and actual one
                # To-Do: Registration of user in file if It does not exists yet
                user['NAME'] = update.message.from_user.name
                user['ID'] = update.message.from_user.id
                user['SIGNUP_DATE'] = (update.message.date).now().strftime('%Y-%m-%d %H:%M:%S')
                update.message.reply_text(TEXT['SIGNUP_SUCCESS']) # Bot reply
            else: # Wrong Key provided
                update.message.reply_text(TEXT['SIGNUP_FAIL']) # Bot reply
        else: # No argument or more than 1 argument provided
            update.message.reply_text(TEXT['SIGNUP_NOT_ARG']) # Bot reply
    else: # The user is alredy signed-up
        update.message.reply_text(TEXT['SIGNUP_EXIST_USER']) # Bot reply


def add(bot, update, args):
    '''/add command handler'''
    if update.message.from_user.id == user['ID']: # If the user is sign-up
        if len(args) == 1: # If 1 argument has been provided
            feed_url = args[0] # Get the feed url provided (argument)
            # To-Do: Add the feed to the user data file, if it is not alredy subscribed to that feed
            bot_response = '{}{}'.format(TEXT['ADD_FEED'], feed_url)
            update.message.reply_text(bot_response) # Bot reply
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
    disp.add_handler(CommandHandler("add", add, pass_args=True))

    # Start the Bot polling ignoring pending messages (clean=True)
    updater.start_polling(clean=True)

    # Set the bot to idle (actual main-thread stops and wait for incoming messages for the handlers)
    updater.idle()


####################################################################################################

### Execute the main function if the file is not an imported module ###
if __name__ == '__main__':
    main()
