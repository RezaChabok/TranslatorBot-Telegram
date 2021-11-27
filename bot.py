from flask import Flask, request
import telepot
from mtranslate import translate
import urllib3
import sys
from gtts import gTTS
import cv2
import pytesseract
def img_convertor(address):
    img = cv2.imread(address)
    text = pytesseract.image_to_string(img)
    return text
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
        
        elif content_type == 'photo' :
            try:
                bot.download_file(msg['photo'][-1]['file_id'], 'file.png')
                text = img_convertor('file.png')
                if language(text) == "english" :
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
            except :
                pass
        else :
            bot.sendMessage(chat_id,"ok")
            

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
