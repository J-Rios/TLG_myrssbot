# -*- coding: utf-8 -*-
'''
Script:
    constants.py
Description:
    Constants values for myrssbot.py.
Author:
    Jose Rios Rubio
Creation date:
    23/08/2017
Last modified date:
    25/08/2017
Version:
    0.2.0
'''

####################################################################################################

### Constants ###
CONST = {
    'DEVELOPER' : '@JoseTLG', # Developer Telegram contact
    'DATE' : '25/08/2017', # Last modified date
    'VERSION' : '0.2.0', # Actual version
    'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', # Bot Token (get it from @BotFather)
    'REG_KEY' : 'registrationKey1234', # User registration Key (for signup and let use the Bot)
    'DATA_USERS_DIR' : './data/users', # Path of users data directory
    'USERS_LIST_FILE' : './data/users_list.json' # Json file of signed-up users list
}

TEXT = {
    'START' : \
        'I am a feed parser Bot, that let you subscribe to multiple feeds contents and handles ' \
        'RSS, CDF and ATOM formats. I will notify you when a new feed comes out.\n' \
        '\n' \
        'Check the /help command for get usefull information about my use.',

    'HELP' : \
        'I am open source and completely free, but you need to know the actual registration key ' \
        'for sign-up your telegram user and get access to add feeds and manage yours ' \
        'subscriptions.',

    'SIGNUP_NOT_ARG' : \
        'The command needs a registration key for signup your user.\n' \
        '\n' \
        'Example:\n' \
        '/signup registrationKey1234',

    'SIGNUP_FAIL' : \
        'Sign-up fail. Wrong or out-dated registration key?\n' \
        '\n' \
        'Ask the owner about the key.',

    'SIGNUP_EXIST_USER' : \
        'You alredy have an account in the Bot system. If you want to create a new one, first ' \
        'you need to remove your old account with the /signdown command.',

    'SIGNUP_SUCCESS' : \
        'Sign-up success. Created an account for your user, now you are free to use all the ' \
        'commands, enjoy!',

    'CMD_NOT_ALLOW' : \
        'You are not allowed to use this command. First you need to get access, signing up in ' \
        'the Bot data base to create an account of your user. You can da that with the /signup ' \
        'command and using the registration Key provided by the owner.',

    'ADD_NOT_ARG' : \
        'The command needs a feed url.\n' \
        '\n' \
        'Example:\n' \
        '/add https://www.kickstarter.com/projects/feed.atom',

    'ADD_ALREADY_FEED' : \
        'You are already subscribed to that feed',

    'ADD_FEED' : \
        'Feed added. Now you are subscribed to:\n'
}
