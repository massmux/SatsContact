#!/usr/bin/env python

from commons import *
import schedule, threading
import time
from lnurlp import Lnurlp
from cashulib import GetCashu


@bot.command("version")
def version_command(handler):
    chat = bbot.Chat(bot, handler.chat)
    chat.send("SatsContact version 0.0.1 build 20231212")



@bot.command("help")
def help_command(handler):
    chat = bbot.Chat(bot, handler.chat)
    chat.send(f"🖖SatsContact Bot, Welcome"
              f"\n\nLightning Zaps to Cashu."
              f"\n\nCommands summary"
              f"\n/start 👉 Initialize your user or get details"
              f"\n/help 👉 This message",syntax="markdown")



@bot.command("start")
def start_command(handler):
    chat, message, args, btns = bbot.Chat(bot, handler.chat), bbot.Message(bot, handler), bbot.Args(handler).GetArgs(), bbot.Buttons()
    cur_user = message.sender.username.replace('_', '-').lower()
    print(f"Telegram user:{message.sender.username} lnaddressUser: {cur_user}")
    userdetails = get_obj_redis(cur_user)
    if userdetails:
        # returning user, nothing to do
        chat.send(f"😍*Returning user*"
                  f"\n\nHello {message.sender.username}, you are already setup to receive "
                  f"Zaps on the Lightning Address `{userdetails['lnaddress']}` or on "
                  f"the LNURL `{userdetails['lnurlp']}`"
                  f"\n\nEach Zap you receive will be converted in Cashu token and sent here on the Telegram chat 👍", syntax="markdown")
    else:
        newlnurlp = Lnurlp()
        user_to_create = message.sender.username.replace('_','-').lower()
        lnurlp_creation = newlnurlp.create_lnurlp(user_to_create)
        if lnurlp_creation.get('detail') is not None:
            detail = lnurlp_creation.get('detail').replace('_','-')
            chat.send(f"⚠️*Error*"
                      f"\n\nAn exception occurred, action aborted:"
                      f"\n\n{detail}", syntax="markdown")
            print(lnurlp_creation)
            return
        # Lightning Address successfully created
        print(f"new user: {lnurlp_creation}")
        lnaddress,lnurlp = f"{user_to_create}@{settings['lnbits']['lndomain']}", lnurlp_creation['lnurl']
        newuser = { 'username' : message.sender.username, 'userid': chat.id,
                    'lnaddress' : lnaddress,
                    'lnurlp' : lnurlp,
                    'lnaddress_user' : user_to_create,
                   }
        # save details in redis
        set_obj_redis(user_to_create, newuser)
        chat.send(f"❤️*New User*"
                  f"\n\nHello {message.sender.username}, Welcome as new user. You are now ready with the following details: "
                  f"\n\nLightning address: `{lnaddress}`"
                  f"\n\nLNURLp: `{lnurlp}`"
                  f"\n\nEach Zap you receive will be converted in Cashu token and sent here on the Telegram chat 👍"
                  f"\n\nPlease note that your Ligthning address may differ from your username, so be sure to copy it carefully", syntax="markdown")




def events_processor(bot):
    tobeprocessed = hkeys_redis('notifications')
    for i in tobeprocessed:
        current = i.decode('utf-8')
        payment_to_process = get_obj_redis(current)
        amount = payment_to_process['amount']
        print(f"Processing {current} {amount} Sats")
        user_details = get_obj_redis(payment_to_process['username'])
        # minting tokens
        tokenobj = GetCashu()
        minted = tokenobj.get_ecash(amount)
        print(f"Mint result: {minted}")
        bot.chat(user_details['userid']).send(f"🎉*Payment Received*"
                                        f"\n\nAmount: {amount} Sats"
                                        f"\npayment hash: {current}"
                                        f"\nLightning address: {user_details['lnaddress']}"
                                        f"\nToken"
                                        f"\n\n`{minted['ecash']}`", syntax="markdown")
        hdel_redis('notifications', current)


# events processor
schedule.every(30).seconds.do(events_processor, bot)

if __name__ == "__main__":
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)

