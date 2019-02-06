from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests, praw
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
        "tbm tem `/bcc`, `/bbc`, `/filme`, `/fwd` e mais outras merdas\n"
        ]

    s = "".join(h)
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def bcc(bot, update): # /bcc
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    s = ""
    tries = 0
    while ((s == "") or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_TRIES):
        tries += 1
        s = rd.choice(bccList)

    memory[s] = now
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def bbc(bot, update): # /bbc
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    s = ""
    tries = 0
    while ((s == "") or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_TRIES):
        tries += 1
        s = rd.choice(bbcList)

    memory[s] = now
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def filme(bot, update): # /filme
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    s = ""
    tries = 0
    while ((s == "") or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_TRIES):
        tries += 1
    
        rPalavras = rd.randint(0, len(palavrasM) + len(palavrasF) - 1)
        if rPalavras < len(palavrasM):
            s = rd.choice(filmeMList).format(word=palavrasM[rPalavras])
            s = s.replace('ânuss', 'ânus')
        else:
            rPalavras -= len(palavrasM)
            s = rd.choice(filmeFList).format(word=palavrasF[rPalavras])

    memory[s] = now
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def fwd(bot, update): # /fwd
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    now = int(time())
    tries = 0
    while True:
        messageID = rd.randint(0, MAX_FWD_ID)
        try:
            tries += 1
            s = "fwd#" + str(messageID)
            if s not in memory or now-memory[s] >= MEMORY_TIMEOUT or tries >= MAX_TRIES:
                bot.forwardMessage(chatID, '@ofwdnovo', messageID)
                memory[s] = now
                break
        except:
            pass

def joegs(bot, update, args): # /joegs
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    origMsg = update.message.reply_to_message

    queryText = None
    if len(args) != 0:
        queryText = " ".join(args)
    elif origMsg and origMsg.text:
        queryText = origMsg.text
    else:
        s = "manda alguma coisa porra"

    if queryText:
        body = {"text": queryText, "model": "pos"}

        try:
            r = requests.post(url=JOEGS_URL, data=body).json()

            if r["result"] == "REAL":
                s = "hmmm acho q eh vdd"
            else:
                s = "sei nao hein, se pa eh fake"
        except:
            s = "caraio o joegs fudeu o role, alguem chama ele"

    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def foodporn(bot, update): # /foodporn
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    try:
        imgDesc, imgUrl = getRandomImageSubreddit(reddit, "shittyfoodporn")
        assert(imgDesc.endswith(".jpg") or imgDesc.endswith(".png"))

        bot.send_photo(chat_id=chatID, photo=imgUrl, caption=imgDesc)
    except:
        s = "carai capotei o corsa, pera ai"
        bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def shittyfoodporn(bot, update): # /shittyfoodporn
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    try:
        imgDesc, imgUrl = getRandomImageSubreddit(reddit, "foodporn")
        assert(imgDesc.endswith(".jpg") or imgDesc.endswith(".png"))

        bot.send_photo(chat_id=chatID, photo=imgUrl, caption=imgDesc)
    except:
        s = "carai capotei o corsa, pera ai"
        bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def unknown(bot, update):
    printCommandExecution(bot, update)
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    s = "eu n sei o q ele falo"
    bot.send_message(chat_id=chatID, text=s, parse_mode="Markdown")

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    updater = Updater(token=auth.PROD_TOKEN)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('filme', filme))
    dp.add_handler(CommandHandler('bcc', bcc))
    dp.add_handler(CommandHandler('bbc', bbc))
    dp.add_handler(CommandHandler('fwd', fwd))
    dp.add_handler(CommandHandler('joegs', joegs, pass_args=True))
    dp.add_handler(CommandHandler('semtompero', foodporn))
    dp.add_handler(CommandHandler('comtompero', shittyfoodporn))

    # Unknown command
    # dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    print("Bot running...")

    updater.idle()

if __name__ == "__main__":
    JOEGS_URL = "http://nilc-fakenews.herokuapp.com/ajax/check/"

    bbcList = loadFile("bbc.txt")
    bccList = loadFile("bcc.txt")

    filmeMList = loadFile("filmeM.txt")
    filmeFList = loadFile("filmeF.txt")
    palavrasM = ['cu', 'pinto', 'ânus', 'pipi', 'temer', 'caralho', 'talkei', 'furico']
    palavrasF = ['rola', 'vagina', 'dilma', 'jeba', 'mamata', 'puta', 'champola']

    MEMORY_TIMEOUT = 5*60 # doesnt repeat messages shown within last X seconds
    MAX_FWD_ID = 500 # fwd channel has less than X messages
    MAX_TRIES = 500 # will try showing unique msg X times before giving up
    
    memory = {}

    reddit = praw.Reddit(client_id=auth.REDDIT_CID,
                         client_secret=auth.REDDIT_CSECRET,
                         user_agent=auth.REDDIT_UA)

    main()