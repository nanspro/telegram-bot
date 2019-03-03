import logging, requests
import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot aims to provide tokens from faucet to users requesting it. Just request the bot for tokens specifying your wallet address')

def request_eth(bot, update):
    update.message.reply_text('Enter Your address below')

def is_requesting(text):
    words = text.split(' ')
    address = 'nope'
    for word in words:
        if len(word) > 2:
            if word[0] == '0' and word[1] == 'x':
                address = word
                break
    return address

def call_faucet(address):
    response = requests.post('http://localhost:3001/faucet', data = {"address": address, "agent": "telegram"})
    return response

def respond(bot, update):
    """Echo the user message."""
    text = update.message.text
    response = "I don't understand. Please enter /help to see my available commands"
    address = is_requesting(text)
    if address != 'nope':
        response = call_faucet(address)
        if response == 200:
            response = ' x tokens have been transferred to your account'
        elif response == 503:
            response = ' you’ve already requested for tokens in the last 24 hrs' + ' Only one transfer in 24 hours is allowed'
        elif response == 404:
            response = ' something went wrong and we couldn’t transfer tokens to your wallet address.' +  ' Please check address provided and try again later'
    update.message.reply_text(response)

def main():
    token = config.TOKEN
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("requestETH", request_eth))

    dp.add_handler(MessageHandler(Filters.text, respond))

    # Start the Bot
    updater.start_polling()

if __name__ == '__main__':
    main()