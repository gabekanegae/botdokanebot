from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random as rd

import auth # Telegram Bot Token
from utils import *

def start(bot, update): # /start
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    s = "ta rodando ja ue"
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def help(bot, update): # /help
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    h = [
        "`/help`\n",
        "> mostra isso aqui\n",
        "\n",
        "eh isso porra o q mais vc quer",
        "\n",
        ]

    s = "".join(h)
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def bcc(bot, update): # /bcc
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    s = rd.choice(bccList)
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def bbc(bot, update): # /bbc
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    s = rd.choice(bbcList)
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def filme(bot, update): # /filme
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    palavrasM = ['Cu', 'Pinto', 'Ânus', 'Pipi', 'Temer', 'Caralho', 'Talkei']
    palavrasF = ['Rola', 'Vagina', 'Dilma', 'Jeba', 'Mamata']

    rPalavras = rd.randint(0, len(palavrasM) + len(palavrasF) - 1)
    if rPalavras < len(palavrasM): # M
        s = rd.choice(filmeMList).format(word=palavrasM[rPalavras])
        s = s.replace('Ânuss', 'Ânus') # caso de borda
    else: # F
        rPalavras -= len(palavrasM)
        s = rd.choice(filmeFList).format(word=palavrasF[rPalavras])

    s = s.lower()
    bot.send_message(chat_id=update.message.chat_id, text=s)

def unknown(bot, update):
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    s = "eu n sei o q ele falo"
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    updater = Updater(token=auth.TOKEN)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('filme', filme))
    dp.add_handler(CommandHandler('bcc', bcc))
    dp.add_handler(CommandHandler('bbc', bbc))

    # Unknown command
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    print("Bot running...")

    updater.idle()

if __name__ == "__main__":
    bbcList = loadFile("bbc.txt")
    bccList = loadFile("bcc.txt")
    filmeMList = loadFile("filmeM.txt")
    filmeFList = loadFile("filmeF.txt")

    main()