from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from sys import argv, stdout
import requests
import logging
import praw
import markovify
import random as rd
from time import time, strftime, gmtime

import auth # Telegram Bot Token
from utils import *

def start(bot, update):
    logMessageReceived(bot, update, logger)

    s = "ta rodando ja ue"
    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)

def help(bot, update):
    logMessageReceived(bot, update, logger)

    h = [
        "pra ver os comando digita / no chat e ve qq aparece ali\n",
        "\n",
        "vamo ajuda a faze o bot kkkkk\n",
        "https://github.com/KanegaeGabriel/botdokanebot/\n"
        ]

    s = "".join(h)
    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)

def _getRandomFromFile(bot, update, file):
    logMessageReceived(bot, update, logger)

    now = int(time())
    s = None
    tries = 0
    while ((not s) or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_TRIES):
        tries += 1
        s = rd.choice(file)

    memory[s] = now

    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)
    logger.info("    --> {} tries | Mem size: {}".format(tries, len(memory)))

def bcc(bot, update): _getRandomFromFile(bot, update, bccList)
def bbc(bot, update): _getRandomFromFile(bot, update, bbcList)
def icmc(bot, update): _getRandomFromFile(bot, update, icmcList)

def carluxo(bot, update):
    text = carluxoMarkov.make_short_sentence(140)
    bot.send_message(chat_id=update.message.chat_id, text=text)

def filme(bot, update):
    logMessageReceived(bot, update, logger)

    now = int(time())
    s = None
    tries = 0
    while ((s == None) or (s in memory and now-memory[s] < MEMORY_TIMEOUT)) and (tries < MAX_TRIES):
        tries += 1
    
        rPalavras = rd.randint(0, len(palavrasM) + len(palavrasF) - 1)
        pick = rd.choice(filmeList)

        if rPalavras < len(palavrasM):
            s = parseGender(pick, "male").format(word=palavrasM[rPalavras])
            s = s.replace("ânuss", "ânus")
        else:
            rPalavras -= len(palavrasM)
            s = parseGender(pick, "female").format(word=palavrasF[rPalavras])

    memory[s] = now
    
    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)
    logger.info("    --> {} tries | Mem size: {}".format(tries, len(memory)))

def fwd(bot, update):
    logMessageReceived(bot, update, logger)

    now = int(time())
    tries = 0
    while True:
        messageID = rd.randint(0, MAX_FWD_ID)
        try:
            tries += 1
            s = "fwd#" + str(messageID)
            if s not in memory or now-memory[s] >= MEMORY_TIMEOUT or tries >= MAX_TRIES:
                bot.forwardMessage(update.message.chat_id, "@ofwdnovo", messageID)
                
                memory[s] = now
                break
        except:
            pass

    logMessageSent(bot, update, logger, "FWD", str(messageID), origID=messageID, origChannel="@ofwdnovo")
    logger.info("    --> {} tries | Mem size: {}".format(tries, len(memory)))

def joegs(bot, update, args):
    logMessageReceived(bot, update, logger)
    
    origMsg = update.message.reply_to_message

    queryText = None
    if origMsg and origMsg.text:
        queryText = origMsg.text
    else:
        s = "manda o comando respondendo a alguma msg pfvr"

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

    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)

def zapzap(bot, update, args):
    logMessageReceived(bot, update, logger)

    origMsg = update.message.reply_to_message

    queryText = None
    if origMsg and origMsg.text:
        queryText = origMsg.text
    else:
        s = "manda o comando respondendo a alguma msg pfvr\n\nopções: angry/happy/sad/sassy/sick"

    if queryText:
        mood = "happy"
        if len(args) != 0:
            userMood = args[0].lower()

            if userMood in moodAngry: mood = "angry"
            elif userMood in moodHappy: mood = "happy"
            elif userMood in moodSad: mood = "sad"
            elif userMood in moodSassy: mood = "sassy"
            elif userMood in moodSick: mood = "sick"

        origMsgWords = len(origMsg.text.split())
        if origMsgWords <= 5:
            rate = "1.0"
        elif origMsgWords <= 15:
            rate = "0.8"
        else:
            rate = "0.6"

        body = {"zap": queryText, "mood": mood, "strength": "3", "rate": rate, "tweet": "false"}

        try:
            r = requests.post(url=FLIPPER_URL, data=body).json()

            if r["zap"]: s = r["zap"]
        except:
            s = "puta merda chama o flipper que deu ruim aqui"

    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)

def _getRandomFromReddit(bot, update, subreddit, user=None):
    logMessageReceived(bot, update, logger)

    now = int(time())
    tries = 0
    while True:
        try:
            tries += 1
            imgDesc, imgUrl = getRandomImageReddit(reddit, subreddit, user)
            
            s = subreddit + "#" + imgUrl
            if imgUrl and (s not in memory or now-memory[s] >= MEMORY_TIMEOUT or tries >= MAX_TRIES):
                memory[s] = now
                break
        except:
            pass

    bot.send_photo(chat_id=update.message.chat_id, photo=imgUrl, caption=imgDesc)
    logMessageSent(bot, update, logger, "IMG", imgDesc, url=imgUrl)
    logger.info("    --> {} tries | Mem size: {}".format(tries, len(memory)))

def foodporn(bot, update): _getRandomFromReddit(bot, update, "foodporn")
def shittyfoodporn(bot, update): _getRandomFromReddit(bot, update, "shittyfoodporn")
def superaww(bot, update): _getRandomFromReddit(bot, update, "superaww", "316nuts")
def programmerhumor(bot, update): _getRandomFromReddit(bot, update, "programmerhumor")

def bandeco(bot, update):
    logMessageReceived(bot, update, logger)

    r = rd.randint(0, 1)
    if r == 0:
        bot.forwardMessage(update.message.chat_id, "@ofwdnovo", 301)
        logMessageSent(bot, update, logger, "FWD", "301", origID=301, origChannel="@ofwdnovo")

        bot.forwardMessage(update.message.chat_id, "@ofwdnovo", 302)
        logMessageSent(bot, update, logger, "FWD", "302", origID=302, origChannel="@ofwdnovo")
    else:
        bot.forwardMessage(update.message.chat_id, "@ofwdnovo", 326)
        logMessageSent(bot, update, logger, "FWD", "326", origID=326, origChannel="@ofwdnovo")

        bot.forwardMessage(update.message.chat_id, "@ofwdnovo", 327)
        logMessageSent(bot, update, logger, "FWD", "327", origID=327, origChannel="@ofwdnovo")

def toschi(bot, update):
    logMessageReceived(bot, update, logger)

    bot.forwardMessage(update.message.chat_id, "@ofwdnovo", 362)
    logMessageSent(bot, update, logger, "FWD", "362", origID=362, origChannel="@ofwdnovo")

    bot.forwardMessage(update.message.chat_id, "@ofwdnovo", 363)
    logMessageSent(bot, update, logger, "FWD", "363", origID=363, origChannel="@ofwdnovo")

def proximo(bot, update, option=None):
    logMessageReceived(bot, update, logger)
    
    m, d, A, H = strftime("%m %d %A %H", gmtime(time()-3*60*60)).split()
    H = int(H)
    weekdays = {"Monday": "Segunda", "Tuesday": "Terça",
                "Wednesday": "Quarta", "Thursday": "Quinta",
                "Friday": "Sexta", "Saturday": "Sábado",
                "Sunday": "Domingo"}

    if not option:
        if H <= 13:
            mealTime = "☀ Almoço"
        elif H >= 19:
            mealTime = "☀ Almoço"
            m, d, A, H = strftime("%m %d %A %H", gmtime(time()-3*60*60+5*60*60)).split()
            H = int(H)
        else:
            mealTime = "🌙 Jantar"
    elif option == "almoco":
        mealTime = "☀ Almoço"
    else:
        mealTime = "🌙 Jantar"
    
    weekday = weekdays[A]
    day = d + "/" + m

    if weekday == "Domingo" or (weekday == "Sábado" and mealTime == "🌙 Jantar"):
        s = "*🏫 São Carlos, Área 1 🍽\n{} de {} ({}):*\nFechado"
        s = s.format(mealTime, weekday, day)
        bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
        return

    mealKey = "cardapio#" + day + mealTime[2]
    if mealKey in memory:
        s = memory[mealKey]

        bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
        return

    calories = 550 + rd.randint(0, 800)

    s, c = cardapio.index("SALADAS")+1, cardapio.index("CARNES")+1
    v, m = cardapio.index("VEGS")+1, cardapio.index("MISTURAS")+1
    d, f = cardapio.index("DOCES")+1, cardapio.index("FRUTAS")+1
    p, b = cardapio.index("PAES")+1, cardapio.index("BEBIDAS")+1

    salada = rd.choice(cardapio[s:c-2])
    carne = rd.choice(cardapio[c:v-2])
    veg = rd.choice(cardapio[v:m-2])
    mistura = rd.choice(cardapio[m:d-2])
    doce = rd.choice(cardapio[d:f-2])
    fruta = rd.choice(cardapio[f:p-2])
    pao = rd.choice(cardapio[p:b-2])
    bebida = rd.choice(cardapio[b:])

    s = "*🏫 São Carlos, Área 1 🍽\n{} de {} ({}):*\n"
    s += "Arroz/Feijão/Arroz Integral/\n{}/\n{}\n"
    s += "Opção Vegetariana: {}/\n{}/\nSobremesa: {}\n{}/\n"
    s += "{}\n{}\n\n_Valor energético médio: ⚡ {}Kcal_"

    s = s.format(mealTime, weekday, day, salada, carne, veg, mistura, doce, fruta, pao, bebida, calories)

    memory[mealKey] = s
    bot.send_message(chat_id=update.message.chat_id, text=s, parse_mode="Markdown")
    logMessageSent(bot, update, logger, "TXT", s)

def almoco(bot, update): proximo(bot, update, "almoco")
def jantar(bot, update): proximo(bot, update, "jantar")

def main():
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("filme", filme))
    dp.add_handler(CommandHandler("bcc", bcc))
    dp.add_handler(CommandHandler("bbc", bbc))
    dp.add_handler(CommandHandler("icmc", icmc))
    dp.add_handler(CommandHandler("carluxo", carluxo))
    dp.add_handler(CommandHandler("fwd", fwd))
    dp.add_handler(CommandHandler("joegs", joegs, pass_args=True))
    dp.add_handler(CommandHandler("zapzap", zapzap, pass_args=True))
    dp.add_handler(CommandHandler("comtompero", foodporn))
    dp.add_handler(CommandHandler("semtompero", shittyfoodporn))
    dp.add_handler(CommandHandler("itimalia", superaww))
    dp.add_handler(CommandHandler("computaria", programmerhumor))
    dp.add_handler(CommandHandler("almoco", almoco))
    dp.add_handler(CommandHandler("jantar", jantar))
    dp.add_handler(CommandHandler("proximo", proximo))
    dp.add_handler(CommandHandler("bandeco", bandeco))
    dp.add_handler(CommandHandler("toschi", toschi))

    updater.start_polling()
    logging.info("=== Bot running! ===")

    updater.idle()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler("bot.log", "a", "UTF-8"), logging.StreamHandler()])

    JOEGS_URL = "http://nilc-fakenews.herokuapp.com/ajax/check/"
    FLIPPER_URL = "http://vemdezapbe.be/api/v1.0/zap/"

    bccList = loadFile("bcc.txt")
    bbcList = loadFile("bbc.txt")
    icmcList = loadFile("icmc.txt")
    carluxoMarkov = markovify.Text("\n".join(loadFile("carluxo.txt")))

    filmeList = loadFile("filme.txt")
    palavrasM = ["cu", "pinto", "ânus", "pipi", "temer", "caralho", "talkei", "furico"]
    palavrasF = ["rola", "vagina", "dilma", "jeba", "mamata", "puta", "champola", "bunda"]

    cardapio = loadFile("cardapio.txt")

    emojiAngry = "😡😠🤬😤😣"
    emojiHappy = "😀😃😄😁😆😅🤣😂🙂🙃😊😇🥰😍🤩☺😋😛😜🤪😝🤑🤗🤭🤔😬😌😪🤤😴🤠🥳😎🤓🧐"
    emojiSad = "🤐🤫🤨😐😑😶😒🙄😔🤥😕😟🙁☹😮😯😲😳🥺😦😧😨😰😥😢😭😱😖😞😓😩😫"
    emojiSassy = "😏😚😙😉😘😗😈👿"
    emojiSick = "😷🤒🤕🤢🤮🤧🥵🥶🥴😵🤯"

    moodAngry = set(["angry", "bravo", "brabo", "puto"] + list(emojiAngry))
    moodHappy = set(["happy", "feliz"] + list(emojiHappy))
    moodSad = set(["sad", "triste"] + list(emojiSad))
    moodSassy = set(["sassy", "tarado", "safado"] + list(emojiSassy))
    moodSick = set(["sick", "doente"] + list(emojiSick))

    MEMORY_TIMEOUT = 5*60 # Doesn't repeat messages shown within the last X seconds
    MAX_FWD_ID = 600 # FWD channel has less than X messages
    MAX_TRIES = 100 # Will try showing an unique message X times before giving up
    
    reddit = praw.Reddit(client_id=auth.REDDIT_CID,
                         client_secret=auth.REDDIT_CSECRET,
                         user_agent=auth.REDDIT_UA)

    memory = {}

    TOKEN = auth.TEST_TOKEN if "test" in argv else auth.PROD_TOKEN
    main()
    logging.info("=== Bot shutting down! ===")
