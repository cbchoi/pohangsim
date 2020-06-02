import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from instance import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


from pathlib import Path

cur_dir = Path(".")
cur_dir = cur_dir.resolve()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    print(update.message.chat_id)
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def _list(update, context):
    global cur_dir
    lst = [str(x) for x in cur_dir.iterdir()]
    lst = "\n".join(lst)
    update.message.reply_text(lst)

def _parent(update, context):
    global cur_dir
    cur_dir = cur_dir.parent
    _list(update, context)

def _select(update, context):
    global cur_dir
    fpath = str(update.message.text).split()
    # fpath[0] : /select
    # fpath[1] : destination
    flist = [str(x) for x in cur_dir.iterdir() if x.is_dir()]

    for item in flist:
        if fpath[1] in item:
            cur_dir = Path(item)
            cur_dir = cur_dir.resolve()
            break

def _send(update, context):
    global cur_dir
    fpath = str(update.message.text).split()
    # fpath[0] : /send
    # fpath[1] : target file
    flist = [str(x) for x in cur_dir.iterdir() if not x.is_dir()]

    for item in flist:
        if fpath[1] in item:
            f = open(item, "rb")
            context.bot.send_document(chat_id=update.message.chat_id, document=f)
            break
def scenario(update,context):
    update.message.reply_text("Entered Scneario Editor")
    #print("Entered Scneario Editor")
    pass
def simulate(update,context):
    update.message.reply_text("Entered Simulation Mode")
    #print("Entered Simulation Mode")
    pass    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELGERAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("scenario", scenario))
    dp.add_handler(CommandHandler("simulate", simulate))

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", _list))
    dp.add_handler(CommandHandler("parent", _parent))
    dp.add_handler(CommandHandler("select", _select))
    dp.add_handler(CommandHandler("send", _send))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()