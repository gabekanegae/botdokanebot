import requests
import praw
import random as rd

def getMsgAttributes(bot, update):
    myself = str(update.message.from_user.username)
    myselfID = str(update.message.from_user.id)
    text = str(update.message.text)
    
    isGroup = str(update.message.chat.type) == "group"
    chatID = str(update.message.chat_id)
    chatName = str(update.message.chat.title if isGroup else update.message.chat.username)

    cm = bot.getChatMember(chatID, int(myselfID))
    isAdmin = cm.status == "creator" or cm.status == "administrator"
    canRunAdmin = not isGroup or update.message.chat.all_members_are_administrators or isAdmin

    return (myself, text, isGroup, chatID, chatName, canRunAdmin)

def printCommandExecution(bot, update):
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    print("{{{}}}@{} in {}[{}]: \"{}\"".format("A" if canRunAdmin else "U", myself, chatName, chatID, text))

def loadFile(filename):
    with open(filename) as f:
        content = [l.strip() for l in f]

    return content

def getRandomImageSubreddit(reddit, subreddit, l=100):
    sub = reddit.subreddit(subreddit)
    posts = [post for post in sub.hot(limit=l)]

    randomPost = rd.choice(posts)
    return randomPost.title, randomPost.url

def DEPRECATED_getRandomImageSubreddit(subreddit):
    URL = "https://www.reddit.com/r/" + subreddit + "/random.json"
    r = requests.get(URL, headers={'User-agent': 'telegram:@botdokanebot:v1.1 (by /u/Kanegae)'}).json()

    imgUrl = r[0]["data"]["children"][0]["data"]["url"]
    return imgUrl