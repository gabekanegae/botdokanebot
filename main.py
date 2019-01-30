from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random as rd
from time import time

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
        "ai tem mais uns outros q falam mais merda tambem\n",
        "eh isso porra o q mais vc quer",
        "\n",
        ]

    s = "".join(h)
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def bcc(bot, update): # /bcc
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    s = ""
    tries = 0
    while ((s == "") or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_SIZE):
        tries += 1
        s = rd.choice(bccList)

    if tries >= MAX_SIZE:
        print("No unique phrases to show. Showing whatever...")
    memory[s] = now

    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def bbc(bot, update): # /bbc
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    s = ""
    tries = 0
    while ((s == "") or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_SIZE):
        tries += 1
        s = rd.choice(bbcList)

    if tries >= MAX_SIZE:
        print("No unique phrases to show. Showing whatever...")
    memory[s] = now
    
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def filme(bot, update): # /filme
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    s = ""
    tries = 0
    while ((s == "") or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_SIZE):
        tries += 1
    
        rPalavras = rd.randint(0, len(palavrasM) + len(palavrasF) - 1)
        if rPalavras < len(palavrasM):
            s = rd.choice(filmeMList).format(word=palavrasM[rPalavras])
            s = s.replace('ânuss', 'ânus')
        else:
            rPalavras -= len(palavrasM)
            s = rd.choice(filmeFList).format(word=palavrasF[rPalavras])

        if tries >= MAX_SIZE:
            print("No unique phrases to show. Showing whatever...")
    memory[s] = now

    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")

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
    # dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    print("Bot running...")

    updater.idle()

if __name__ == "__main__":
    bbcList = loadFile("bbc.txt")
    bccList = loadFile("bcc.txt")

    filmeMList = loadFile("filmeM.txt")
    filmeFList = loadFile("filmeF.txt")
    palavrasM = ['cu', 'pinto', 'ânus', 'pipi', 'temer', 'caralho', 'talkei']
    palavrasF = ['rola', 'vagina', 'dilma', 'jeba', 'mamata', 'puta']

    MEMORY_TIMEOUT = 5*60 # 5 min
    MAX_SIZE = len(bbcList) + len(bccList) + len(filmeMList)*len(palavrasM) + len(filmeFList)*len(palavrasF)
    memory = {}

    main()