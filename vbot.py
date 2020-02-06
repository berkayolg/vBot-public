from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging, os, datetime

from parseIMDB import getRand, initMovies, initShows, initShowGenres, initMovieGenres, writeRecords, showGenres, movieGenres

TOKEN = 'REPLACED BY TOKEN IN LIVE VERSION'
PORT = os.environ.get('PORT')
NAME = 'v-teleg'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
jQ = updater.job_queue

#Welcoming and start commands
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''Welcome to the channel, this bot recommends you some shows and movies.\nList of Commands:\n1.Tell me a movie /movie\n2.Tell me a show /show\n3.To take a genre specified recommendation use /movie <genre> like /movie action\n4.To see available genres for movies and shows type /help''')

#Echo may replaced with a better smart chat
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#Showing available genres to ask the bot
def helpcmd(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Show genre commands:\n"+', '.join(map(str,showGenres()))+'\n\n'+"Movie genre commands:\n"+', '.join(map(str,showGenres()))+'\n\n')

#Handles unknown commands
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Sorry I'm unable to do that command now :(")

#Recommends a show, if a genre specified takes from top 50 of that genre, default is top 250 tv shows on the site.
def recommendShow(update, context):
    try:
        cmd = context.args
        recommended = getRand(showFlag=True, genre=cmd)
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Here is a wonderful show for you!\n%s'%recommended)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=recommended.image, caption=recommended.caption())
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Looks like you misstyped the command, have a look at /help section.")
        print('User entered an invalid command')

def recommendMovie(update, context):
    try:
        cmd = context.args
        recommended = getRand(movieFlag=True, genre=cmd)
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'Here is a wonderful movie for you!\n%s'%recommended)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=recommended.image, caption=recommended.caption())
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Looks like you misstyped the command, have a look at /help section.")
        print('User entered an invalid command')

#Initializing command handlers for telegram bot
def initHandlers(dispatcher):
    handlers = [CommandHandler('start',start), MessageHandler(Filters.text,echo),
                CommandHandler('show',recommendShow), CommandHandler('movie',recommendMovie),
                CommandHandler('help', helpcmd), 
                MessageHandler(Filters.command,unknown)]
    for handler in handlers:
        dispatcher.add_handler(handler)

def checkDateLog(filePath):
    monthNow = datetime.datetime.now().month

    try:
        file = open(filePath, 'r')
        lastUpdated = file.read()
        file.seek(0)

        #Not up-to date
        if int(lastUpdated) != int(monthNow):
            print(lastUpdated, ' ', monthNow)
            return False

    except:
        print("Date log file doesn't exist.")
        return False
    return True

def updateLog():
    print("Updating date log file.")
    monthNow = datetime.datetime.now().month
    file = open("./data/date_log.txt", "w+")
    file.write(str(monthNow))
    file.close()

def initLists():
    #Checking log date file whether it is updated this month.
    upToDate = checkDateLog('./data/date_log.txt')

    if not upToDate:
        updateLog()

        movieList = initMovies()
        showList = initShows()
        showGenresDict = initShowGenres()
        movieGenresDict= initMovieGenres()
        writeRecords(movieList, showList, showGenresDict, movieGenresDict)
    else:
        print('Files are up to date.')
    print("Bot is ready.")

def run():
    initHandlers(dispatcher)
    initLists()
    
    if os.environ.get('PORT') is not None:
        updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
        updater.idle()
    else:
        updater.start_polling()
run()