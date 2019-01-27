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