#Special module to block pms automatically
from telethon.tl.functions.contacts import BlockRequest
import sqlite3
@bot.on(events.NewMessage(incoming=True))
async def permitpm(e):
  if PM_AUTO_BAN:
    global COUNT_PM
    if e.is_private:
       db=sqlite3.connect("pmpermit.db")
       cursor=db.cursor()
       cursor.execute('''SELECT * FROM APPROVED''')
       all_rows = cursor.fetchall()
       PERMITTED_USERS=[]
       for i in all_rows:
           PERMITTED_USERS.append(i[0])
       if not int(e.chat_id) in PERMITTED_USERS:
           await e.reply("`This is bot replying you, you are not permitted to PM. Wait for him to approve you! You will be reported if sent 4 messages without permission.`")
           if e.chat_id not in COUNT_PM:
              COUNT_PM.update({e.chat_id:1})
           else:
              COUNT_PM[e.chat_id]=COUNT_PM[e.chat_id]+1
           if COUNT_PM[e.chat_id]>4:
               await e.respond('`Imma reporting you! Bye.`')
               del COUNT_PM[e.chat_id]
               await bot(BlockRequest(e.chat_id))
               if LOGGER:
                   await bot.send_message(LOGGER_GROUP,str(e.chat_id)+" was just another retarded nibba")
@bot.on(events.NewMessage(outgoing=True,pattern='.approvepm'))
@bot.on(events.MessageEdited(outgoing=True,pattern=".approvepm"))
async def approvepm(e):
    db=sqlite3.connect("pmpermit.db")
    cursor=db.cursor()
    cursor.execute('''INSERT INTO APPROVED VALUES(?)''',(int((await e.get_reply_message()).sender_id),))
    db.commit()
    db.close()
    await e.edit("`Approved to PM!`")
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,str(e.chat_id)+" was approved to PM you.")
