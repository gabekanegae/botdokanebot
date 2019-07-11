import requests
import logging
import praw
import random as rd

def logMessageReceived(bot, update, logger):
    user = str(update.message.from_user.username)
    userID = str(update.message.from_user.id)
    text = str(update.message.text)

    isGroup = str(update.message.chat.type) == "group"
    chatName = str(update.message.chat.title) if isGroup else "PRIV"
    chatID = "(" + str(update.message.chat_id) + ")" if isGroup else ""

    text = "\\n".join(text.split("\n"))

    logger.info("RX @{}({}) @ {}{}: \"{}\"".format(user, userID, chatName, chatID, text))
    if update.message.reply_to_message:
        origText = str(update.message.reply_to_message.text)
        origText = "\\n".join(origText.split("\n"))

        logger.info("    --> As reply to: \"{}\"".format(origText))

def logMessageSent(bot, update, logger, msgType, msg, **kwargs):
    user = str(update.message.from_user.username)
    userID = str(update.message.from_user.id)

    isGroup = str(update.message.chat.type) == "group"
    chatName = str(update.message.chat.title) if isGroup else "PRIV"
    chatID = "(" + str(update.message.chat_id) + ")" if isGroup else ""

    msg = "\\n".join(str(msg).split("\n"))

    if msgType == "TXT":
        logger.info("TX @{}({}) @ {}{} (TXT): \"{}\""
                    .format(user, userID, chatName, chatID, msg))
    elif msgType == "IMG":
        logger.info("TX @{}({}) @ {}{} (IMG): {} -- \"{}\""
                     .format(user, userID, chatName, chatID, kwargs["url"], msg))
    elif msgType == "FWD":
        logger.info("TX @{}({}) @ {}{} (FWD): #{}({}) -- \"{}\""
                     .format(user, userID, chatName, chatID, kwargs["origID"], kwargs["origChannel"], msg))

def loadFile(filename):
    with open(filename, encoding="UTF-8") as f:
        content = [l.strip() for l in f]

    return content

def parseGender(filme, gender):
    words = filme.split()

    if gender == "male":
        for i in range(len(words)):
            if words[i].startswith("["):
                s = words[i].index("[")+1
                e = words[i].index("|")
                words[i] = words[i][s:e]
    else: # female
        for i in range(len(words)):
            if words[i].startswith("["):
                s = words[i].index("|")+1
                e = words[i].index("]")
                words[i] = words[i][s:e]

    return " ".join(words)

def getRandomImageReddit(reddit, subreddit, user=None, l=50):
    if not user:
        sub = reddit.subreddit(subreddit)
    else:
        sub = reddit.multireddit(user, subreddit)
    
    posts = [post for post in sub.hot(limit=l)]

    randomPost = None
    isImage = False
    while not isImage and posts:
        randomPost = rd.choice(posts)
        isImage = randomPost.url.endswith(".jpg") or randomPost.url.endswith(".png") or randomPost.url.endswith(".jpeg")
        if not isImage: posts.remove(randomPost)

    if randomPost:
        return randomPost.title, randomPost.url
    else:
        return None, None