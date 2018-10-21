@bot.on(events.NewMessage(incoming=True))
async def mention_afk(e):
    global COUNT_MSG
    global USERS
    global ISAFK
    if e.message.mentioned:
        if ISAFK:
            if e.chat_id not in USERS:
                  await e.reply("I am away from keyboard due to: ```"+AFKREASON+"```")
                  USERS.update({e.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
            elif e.chat_id in USERS:
                 if USERS[e.chat_id] % 5 == 0:
                      await e.reply("I am away from keyboard due to: ```"+AFKREASON+"```")
                      USERS[e.chat_id]=USERS[e.chat_id]+1
                      COUNT_MSG=COUNT_MSG+1
                 else:
                   USERS[e.chat_id]=USERS[e.chat_id]+1
                   COUNT_MSG=COUNT_MSG+1
@bot.on(events.NewMessage(incoming=True))
async def afk_on_pm(e):
    global ISAFK
    global USERS
    global COUNT_MSG
    if e.is_private:
        if ISAFK:
            if e.chat_id not in USERS:
                  await e.reply("I am away from keyboard due to: ```"+AFKREASON+"```")
                  USERS.update({e.chat_id:1})
                  COUNT_MSG=COUNT_MSG+1
            elif   e.chat_id in USERS:
                   if USERS[e.chat_id] % 5 == 0:
                     await e.reply("I am away from keyboard due to: ```"+AFKREASON+"```")
                     USERS[e.chat_id]=USERS[e.chat_id]+1
                     COUNT_MSG=COUNT_MSG+1
                   else:
                    USERS[e.chat_id]=USERS[e.chat_id]+1
                    COUNT_MSG=COUNT_MSG+1
@bot.on(events.NewMessage(outgoing=True,pattern='.notafk'))
@bot.on(events.MessageEdited(outgoing=True,pattern='.notafk'))
async def not_afk(e):
        global ISAFK
        global COUNT_MSG
        global USERS
        global AFKREASON
        ISAFK=False
        await e.edit("Returned.")
        await e.respond("`You recieved "+str(COUNT_MSG)+" messages while you were away. Check log for more details.`")
        await bot.send_message(LOGGER_GROUP,"You recieved "+str(COUNT_MSG)+" messages from "+str(len(USERS))+" chats while you were away")
        for i in USERS:
              await bot.send_message(LOGGER_GROUP,str(i)+" sent you "+"`"+str(USERS[i])+" messages`")
        COUNT_MSG=0
        USERS={}
        AFKREASON="No reason"
@bot.on(events.NewMessage(outgoing=True, pattern='.iamafk'))
@bot.on(events.MessageEdited(outgoing=True, pattern='.iamafk'))
async def set_afk(e):
            message=e.text
            string = str(message[8:])
            global ISAFK
            global AFKREASON
            ISAFK=True
            await e.edit("I am away from keyboard.")
            if string!="":
                AFKREASON=string
            await bot.send_message(LOGGER_GROUP,"You went away from keyboard.")
