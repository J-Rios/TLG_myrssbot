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
    31/08/2017
Version:
    0.7.0
'''

####################################################################################################

### Constants ###
CONST = {
    'DEVELOPER' : '@JoseTLG', # Developer Telegram contact
    'DATE' : '31/08/2017', # Last modified date
    'VERSION' : '0.7.0', # Actual version
    'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', # Bot Token (get it from @BotFather)
    'REG_KEY' : 'registrationKey1234', # User registration Key (for signup and let use the Bot)
    'CHATS_DIR' : './data/chats', # Path of chats data directory
    'USERS_LIST_FILE' : './data/users_list.json', # Json file of signed-up users list
    'TLG_MSG_MAX_CHARS' : 4095, # Max number of characters per message allowed by Telegram
    'MAX_ENTRY_SUMMARY' : 500, # Max number of characters in entry summary (description)
    'NUM_SHOW_ENTRIES' : 5, # Number of max entries to monitorize and show
    'T_USER_FEEDS' : 10 # User time between feeds check (600s -> 10m)
}

TEXT = {
    'START' : \
        'I am a feed parser Bot, that let you subscribe to multiple feeds contents, handles ' \
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

    'SIGNDOWN_SURE' : \
        'The /signdown command will delete your account, all the feeds that you have added ' \
        'will be lose. If you are sure to do this, you have to use the next statement:\n' \
        '\n' \
        '/signdown iamsuretoremovemyaccount',

    'NO_EXIST_USER' : \
        'You does not have an account yet.',

    'SIGNDOWN_CONFIRM_INVALID' : \
        'Invalid confirmation. If you are sure to do this, you have to use the next statement:\n' \
        '\n' \
        '/signdown iamsuretoremovemyaccount',

    'SIGNDOWN_SUCCESS' : \
        'Sign-down success. Now you can create and start a new account with new feeds.',

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
        'You are already subscribed to that feed.',

    'ADD_NO_ENTRIES' : \
        'Invalid URL (no entries found in that feed).',

    'ADD_FEED' : \
        'Feed added. Now you are subscribed to:\n',

    'RM_NOT_ARG' : \
        'The command needs a feed url.\n' \
        '\n' \
        'Example:\n' \
        '/remove https://www.kickstarter.com/projects/feed.atom',

    'RM_NOT_SUBS' : \
        'The chat does not have that feed added.',

    'RM_FEED' : \
        'Feed successfull removed.',

    'NO_ENTRIES' : \
        'There is no current entries in the feed:\n',

    'ENA_NOT_DISABLED' : \
        'I am already enabled.',

    'ENA_NOT_SUBS' : \
        'There is no feeds subscriptions yet.',

    'ENA_ENABLED' : \
        'Feeds notifications enabled. Stop It with /disable command when you want.',

    'DIS_NOT_ENABLED' : \
        'I am already disabled.',

    'DIS_DISABLED' : \
        'Feeds notifications disabled. Start It with /enable command when you want.',

    'FEEDREADER_ACTIVE' : \
        'The FeedReader is active, to use that command you need to disable it. Run the command ' \
        '/disable first.',

    'LINE' : \
        '\n———————————————————\n'
}
