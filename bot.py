from flask import Flask, request
import telepot
from mtranslate import translate
import urllib3
import sys
from gtts import gTTS
def language (pm):#Automatically detects whether the language of the submitted text is Persian or English
            if pm[0] in alphEn:
                  return 'english'
            return 'farsi'
welcome="welcome text when users send /start to bot"
Help="help text how to use bot"
try:

    alphEn=['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']
    proxy_url= "http://proxy.server:3128"
    telepot.api._pools = {
        'default': urllib3.ProxyManager(proxy_url= proxy_url, num_pools=3,maxsize=10, retries = False, timeout= 30),
    }
    telepot.api._onetime_pool_spec =(urllib3.ProxyManager, dict(proxy_url= proxy_url, num_pools=1, maxsize=1,retries=False , timeout=30))
    secret="bot"
    bot = telepot.Bot('Token')
    bot.setWebhook("domain/{}".format(secret), max_connections =1)
    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
                text=msg["text"]
                if text == "/start" :
                    bot.sendMessage(chat_id,welcome)
                elif text[0:4] == '/say':#chat with users 
                    if chat_id == admin_chat_id:
                        u_id=''
                        textlen=0
                        for i in text[5:20]:
                            textlen += 1
                            if i != '|':
                                u_id += i
                            if i == '|':
                                break
                        u_id=int(u_id)
                        bot.sendMessage(u_id,text[5 + textlen:])
                        bot.sendMessage('admin_chat_id',text[5 + textlen:]+"  was sent.")#for example admin send /say user_id |hi and bot send hi to user_id.
                        
                elif text == "/help" :
                    bot.sendMessage(chat_id,Help)
                elif language(text) == "english" :
                    bot.sendMessage(chat_id,translate(text,"fa","en"))
                    speech = gTTS(text)
                    speech.save("hi.ogg")
                    bot.sendAudio(chat_id, open('hi.ogg', 'rb'), title="")
                else :
                    txt=translate(text,"en","fa")
                    bot.sendMessage(chat_id,txt)
                    speech = gTTS(txt)
                    speech.save("hi.ogg")
                    bot.sendAudio(chat_id, open('hi.ogg', 'rb'), title="")
                bot.forwardMessage('admin_chat_id', msg['chat']['id'], msg['message_id'])
                mention="tg://openmessage?user_id={}".format(chat_id)#send to admin users requests with their chat_id mention
                bot.sendMessage('admin_chat_id',mention)
        else :
            mention="tg://openmessage?user_id={}".format(chat_id)
            bot.sendMessage('admin_chat_id',mention)
            bot.sendMessage(chat_id,"ok")
            bot.forwardMessage('admin_chat_id', msg['chat']['id'], msg['message_id'])


    app = Flask(__name__)
    @app.route('/{}'.format(secret),methods = ["POST"])
    def telegram_webhook():
        update = request.get_json()
        if "message" in update :
            handle(update['message'])
        return "ok"
except:
    e = sys.exc_info()[0]
    print(  e )
