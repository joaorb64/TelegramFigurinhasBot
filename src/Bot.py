#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import Database
import Sticker

updater = Updater(token='')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

NONE, MINE, OTHER = range(3)

def start(bot, update):
    db = Database.Database()
    db.addUser(update.message.from_user.id)
    bot.send_message(chat_id=update.message.chat_id, text="Oi!")
    reply_keyboard = [[u'Listar minhas', u'Listar repetidas',u'Atualizar meus dados'], [u'Comparar com dados de outro']]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text(
        'O que deseja fazer?',
        reply_markup=markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

def mensagem(bot, update):
    db = Database.Database()
    userData = db.getData(update.message.from_user.id)

    #bot.send_message(chat_id=update.message.chat_id, text=">"+update.message.from_user.first_name)
    if(userData["mode"] == MINE):
        if(update.message.text.startswith(u"Minhas figurinhas do álbum da copa 2018 que eu tenho")):
            db.setStickers(update.message.from_user.id, Sticker.getStickers(update.message.text))
        elif(update.message.text.startswith(u"Minhas figurinhas do álbum da copa 2018 repetidas")):
            db.setStickersRepeat(update.message.from_user.id, Sticker.getStickers(update.message.text))
        elif(update.message.text.startswith(u"Minhas figurinhas do álbum da copa 2018 que me faltam")):
            db.setStickers(update.message.from_user.id, Sticker.getStickersComplement(update.message.text))
        bot.send_message(chat_id=update.message.chat_id, text=u"Pronto!")
        db.setMode(update.message.from_user.id, NONE)

    elif(userData["mode"] == OTHER):
        if(update.message.text.startswith(u"Minhas figurinhas do álbum da copa 2018 que eu tenho")):
            bot.send_message(chat_id=update.message.chat_id, text=u"Você pode oferecer a essa pessoa: \n"+Sticker.compareStickers(userData["stickersRepeat"], Sticker.getStickers(update.message.text)))
        elif(update.message.text.startswith(u"Minhas figurinhas do álbum da copa 2018 repetidas")):
            bot.send_message(chat_id=update.message.chat_id, text=u"Você pode conseguir com essa pessoa: \n"+Sticker.compareStickers(Sticker.getStickers(update.message.text), userData["stickers"]))
        elif(update.message.text.startswith(u"Minhas figurinhas do álbum da copa 2018 que me faltam")):
            bot.send_message(chat_id=update.message.chat_id, text=u"Você pode oferecer a essa pessoa: \n"+Sticker.compareStickers(userData["stickersRepeat"], Sticker.getStickersComplement(update.message.text)))
        db.setMode(update.message.from_user.id, NONE)
        
    elif(userData["mode"] == NONE):
        if(update.message.text=='Listar minhas'):
            bot.send_message(chat_id=update.message.chat_id, text=u"Suas figurinhas:\n"+userData["stickers"])
        elif(update.message.text=='Listar repetidas'):
            bot.send_message(chat_id=update.message.chat_id, text=u"Suas figurinhas repetidas:\n"+userData["stickersRepeat"])
        elif(update.message.text=="Atualizar meus dados"):
            bot.send_message(chat_id=update.message.chat_id, text=u"Aguardando por mensagem com as figurinhas que você tem ou que te faltam")
            db.setMode(update.message.from_user.id, MINE)
        elif(update.message.text=="Comparar com dados de outro"):
            bot.send_message(chat_id=update.message.chat_id, text=u"Aguardando por mensagem com as figurinhas de seu amigo")
            db.setMode(update.message.from_user.id, OTHER)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=u"Não entendo... ou comando não programado ainda!")
    
    userData = db.getData(update.message.from_user.id)
    if(userData["mode"] == NONE):
        reply_keyboard = [[u'Listar minhas', u'Listar repetidas',u'Atualizar meus dados'], [u'Comparar com dados de outro']]
        markup = ReplyKeyboardMarkup(reply_keyboard)
        update.message.reply_text(
            'O que deseja fazer?',
            reply_markup=markup)


mensagem_handler = MessageHandler(Filters.text, mensagem)
dispatcher.add_handler(mensagem_handler)

updater.start_polling()
updater.idle()