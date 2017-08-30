# -*- coding: utf-8 -*-
'''
Script:
    myrss.py
Description:
    Telegram Bot that let you subscribe and follow customs RSS, CDF and ATOM Feeds.
Author:
    Jose Rios Rubio
Creation date:
    23/08/2017
Last modified date:
    30/08/2017
Version:
    0.5.0
'''

####################################################################################################

### Imported modules ###
from os import path
from time import sleep
from threading import Thread, Lock
from collections import OrderedDict
from feedparser import parse
from telegram import MessageEntity, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, \
                         ConversationHandler, CallbackQueryHandler

import TSjson
from constants import CONST, TEXT

####################################################################################################

### Globals ###
threads = []
threads_lock = Lock()

####################################################################################################

### Class for chats FeedReader threads ###
class CchatFeed(Thread):
    '''Threaded chat feed class to manage each chat feedparser'''
    def __init__(self, args):
        ''' Class constructor'''
        Thread.__init__(self)
        self.chat_id = args[0]
        self.bot = args[1]
        self.end = False
        self.lock = Lock()

    def get_id(self):
        '''Get thread ID (chat ID)'''
        return self.chat_id

    def finish(self):
        '''Set to finish the thread and kill it (from TLG /disable command)'''
        self.lock.acquire()
        self.end = True
        self.lock.release()

    def run(self):
        '''thread method that run when the thread is launched (thread.start() is call)'''
        # Read all feeds urls of chat file (by chat_id)
        last_feeds = {'Title': '', 'Subtitle' : '', 'Link' : '', 'Entries' : []}
        actual_feeds = {'Title': '', 'Subtitle' : '', 'Link' : '', 'Entries' : []}
        fjson_chat_feeds = TSjson.TSjson('{}/{}.json'.format(CONST['CHATS_DIR'], self.chat_id))
        feeds_urls = fjson_chat_feeds.read_content()
        feeds_urls = feeds_urls[0]['Feeds']
        # For each feed url
        for url in feeds_urls:
            # Parse and get feed data
            feedparse = parse(url)
            actual_feeds['Title'] = feedparse['feed']['title']
            #actual_feeds['Subtitle'] = feedparse['feed']['subtitle']
            actual_feeds['Link'] = feedparse['feed']['link']
            # Determine number of entries to show
            #for i in range(0, len(feedparse['entries']), 1):
            if len(feedparse['entries']) >= CONST['NUM_SHOW_ENTRIES']:
                entries_to_show = CONST['NUM_SHOW_ENTRIES']
            else:
                entries_to_show = len(feedparse['entries'])
            # If any entry
            if entries_to_show:
                # For entries to show, get entry data
                for i in range(entries_to_show-1, -1, -1):
                    entry = {'Title': '', 'Published' : '', 'Summary' : '', 'Link' : ''}
                    entry['Title'] = feedparse['entries'][i]['title']
                    entry['Published'] = feedparse['entries'][i]['published']
                    entry['Summary'] = feedparse['entries'][i]['summary']
                    entry['Link'] = feedparse['entries'][i]['link']
                    # Truncate entry summary if it is more than MAX_ENTRY_SUMMARY chars
                    if len(entry['Summary']) > CONST['MAX_ENTRY_SUMMARY']:
                        entry['Summary'] = entry['Summary'][0:CONST['MAX_ENTRY_SUMMARY']]
                        entry['Summary'] = '{}...'.format(entry['Summary'])
                    # Add feed entry data to actual feeds variable
                    actual_feeds['Entries'].append(entry)
                # Send the telegram message/s
                last_entry = actual_feeds['Entries'][entries_to_show-1]
                bot_msg = 'Feed:\n{}{}Link:\n{}{}\nLast entry:\n\n{}\n{}\n\n{}\n\n{}'.format( \
                        actual_feeds['Title'], TEXT['LINE'], actual_feeds['Link'], TEXT['LINE'], \
                        last_entry['Title'], last_entry['Published'], last_entry['Summary'], \
                        last_entry['Link'])
                bot_msg = split_tlg_msgs(bot_msg)
                for msg in bot_msg:
                    self.bot.sendMessage(chat_id=self.chat_id, text=msg)
            # Add all feed data to last feeds variable
            last_feeds = actual_feeds.copy()
        # While not end the thread (finish() method call from /disable command)
        while(not self.end):
            # Read the actual feeds urls of chat file (by chat_id), searching for changes
            actual_feeds = {'Title': '', 'Subtitle' : '', 'Link' : '', 'Entries' : []}
            feeds_urls = fjson_chat_feeds.read_content()
            feeds_urls = feeds_urls[0]['Feeds']
            # For each feed url
            for url in feeds_urls:
                # Parse and get feed data and entries data
                feedparse = parse(url)
                actual_feeds['Title'] = feedparse['feed']['title']
                # Determine number of entries to show
                #for i in range(0, len(feedparse['entries']), 1):
                if len(feedparse['entries']) >= CONST['NUM_SHOW_ENTRIES']:
                    entries_to_show = CONST['NUM_SHOW_ENTRIES']
                else:
                    entries_to_show = len(feedparse['entries'])
                # If any entry (not 0)
                if entries_to_show:
                    # For entries to show, get entry data
                    for i in range(entries_to_show-1, -1, -1):
                        entry = {'Title': '', 'Published' : '', 'Summary' : '', 'Link' : ''}
                        entry['Title'] = feedparse['entries'][i]['title']
                        entry['Published'] = feedparse['entries'][i]['published']
                        entry['Summary'] = feedparse['entries'][i]['summary']
                        entry['Link'] = feedparse['entries'][i]['link']
                        # Truncate entry summary if it is more than MAX_ENTRY_SUMMARY chars
                        if len(entry['Summary']) > CONST['MAX_ENTRY_SUMMARY']:
                            entry['Summary'] = entry['Summary'][0:CONST['MAX_ENTRY_SUMMARY']]
                            entry['Summary'] = '{}...'.format(entry['Summary'])
                        # Add feed entry data to actual feeds variable
                        actual_feeds['Entries'].append(entry)
                        # If it is a new entry
                        if entry not in last_feeds['Entries']:
                            # Send the telegram message/s
                            bot_msg = '{}{}{}\n{}\n\n{}\n\n{}' \
                                    .format(actual_feeds['Title'], TEXT['LINE'], entry['Title'], \
                                    entry['Published'], entry['Summary'], \
                                    entry['Link'])
                            bot_msg = split_tlg_msgs(bot_msg)
                            for msg in bot_msg:
                                self.bot.sendMessage(chat_id=self.chat_id, text=msg)
            # Add all feed data to last feeds variable
            last_feeds = actual_feeds.copy()
            sleep(CONST['T_USER_FEEDS'])

####################################################################################################

### Functions ###
def split_tlg_msgs(text_in):
    '''Function for split a text in fragments of telegram allowed length message'''
    text_out = []
    num_char = len(text_in)
    # Just one fragment if the length of the message is less than max chars allowed per TLG message
    if num_char <= CONST['TLG_MSG_MAX_CHARS']:
        text_out.append(text_in)
    # Split the text in fragments if the length is higher than max chars allowed by TLG message
    else:
        # Determine the number of msgs to send and add 1 more msg if it is not an integer number
        num_msgs = num_char/float(CONST['TLG_MSG_MAX_CHARS'])
        #if isinstance(num_msgs, numbers.Integral) != True:
        if isinstance(num_msgs, int) != True:
            num_msgs = int(num_msgs) + 1
        fragment = 0
        # Create the output fragments list of messages
        for _ in range(0, num_msgs, 1):
            text_out.append(text_in[fragment:fragment+CONST['TLG_MSG_MAX_CHARS']])
            #text_out.append(text_in[fragment:fragment+CONST['TLG_MSG_MAX_CHARS']].decode('utf-8', \
            #        'ignore'))
            fragment = fragment + CONST['TLG_MSG_MAX_CHARS']
    # Return the result text/list-of-fragments
    return text_out


def signup_user(update):
    '''Function for sign-up a user in the system (add to users list file)'''
    # Initial user data for users list file
    usr_data = OrderedDict([])
    # Set user data for users list json file
    usr_data['Name'] = update.message.from_user.name
    usr_data['User_id'] = update.message.from_user.id
    usr_data['Sign_date'] = (update.message.date).now().strftime('%Y-%m-%d %H:%M:%S')
    usr_data['Chats'] = []
    # Create TSjson object for list of users and write on them the data
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
        fjson_chat_feeds = TSjson.TSjson(chat_file)
        subs_feeds = fjson_chat_feeds.read_content()
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
    fjson_chat_feeds = TSjson.TSjson('{}/{}.json'.format(CONST['CHATS_DIR'], chat_id))
    subs_feeds = fjson_chat_feeds.read_content()
    if subs_feeds:
        subs_feeds = subs_feeds[0]
        subs_feeds['Feeds'].append(feed_url)
        fjson_chat_feeds.update(subs_feeds, 'Chat_id')
    else:
        usr_feeds = OrderedDict([])
        usr_feeds['Chat_id'] = chat_id
        usr_feeds['Feeds'] = [feed_url]
        fjson_chat_feeds.write_content(usr_feeds)

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
                feed = parse(feed_url) # Get the feedparse of that feed url
                if feed['bozo'] == 0: # If valid feed
                    add_feed(user_id, chat_id, feed_url) # Add the feed url to the chat feeds file
                    bot_response = '{}{}'.format(TEXT['ADD_FEED'], feed_url) # Bot response
                else: # No valid feed
                    bot_response = TEXT['ADD_NO_ENTRIES'] # Bot response
            else: # Already subscribed to that feed
                bot_response = TEXT['ADD_ALREADY_FEED'] # Bot reply
        else: # No argument or more than 1 argument provided
            bot_response = TEXT['ADD_NOT_ARG'] # Bot reply
    else: # The user is not allowed (needs to sign-up)
        bot_response = TEXT['CMD_NOT_ALLOW'] # Bot reply
    update.message.reply_text(bot_response) # Bot reply


def cmd_enable(bot, update):
    '''/enable command handler'''
    global threads # Use global variable for active threads
    global threads_lock # Use the global lock for active threads
    thr_actives_id = [] # Initial list of active threads IDs empty
    chat_id = update.message.chat_id # Get the chat id
    for thr_feed in threads: # For each active thread
        thr_actives_id.append(thr_feed.get_id()) # Get the active thread ID
    if chat_id not in thr_actives_id: # If the actual chat is not in the active threads
        thr_feed = CchatFeed(args=(chat_id, bot)) # Create and launch actual chat feeds threads
        #thr_feed.setDaemon(True) # Set the thread as daemon
        if not thr_feed.isAlive(): # Make sure that the thread is really active
            threads_lock.acquire() # Lock the active threads variable
            threads.append(thr_feed) # Add actual thread to the active threads variable
            threads_lock.release() # Release the active threads variable lock
            thr_feed.start() # Launch the thread
            bot_response = TEXT['ENA_ENABLED'] # Bot response
    else: # Actual chat feeds thread currently running
        bot_response = TEXT['ENA_NOT_DISABLED'] # Bot response
    update.message.reply_text(bot_response) # Bot reply


def cmd_disable(bot, update):
    global threads # Use global variable for active threads
    global threads_lock # Use the global lock for active threads
    thr_actives_id = [] # Initial list of active threads IDs empty
    chat_id = update.message.chat_id # Get the chat id
    bot_response = TEXT['DIS_NOT_ENABLED'] # Bot response
    for thr_feed in threads: # For each active thread
        thr_actives_id.append(thr_feed.get_id()) # Get the active thread ID
    if chat_id in thr_actives_id: # If the actual chat is in the active threads
        if thr_feed.isAlive(): # Make sure that the thread is really active
            thr_feed.finish() # Finish the thread
            threads_lock.acquire() # Lock the active threads variable
            threads.remove(thr_feed) # Remove actual thread from the active threads variable
            threads_lock.release() # Release the active threads variable lock
            bot_response = TEXT['DIS_DISABLED'] # Bot response
    update.message.reply_text(bot_response) # Bot reply

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
    disp.add_handler(CommandHandler("enable", cmd_enable))
    disp.add_handler(CommandHandler("disable", cmd_disable))
    # Start the Bot polling ignoring pending messages (clean=True)
    updater.start_polling(clean=True)
    # Set the bot to idle (actual main-thread stops and wait for incoming messages for the handlers)
    updater.idle()

####################################################################################################

### Execute the main function if the file is not an imported module ###
if __name__ == '__main__':
    main()
