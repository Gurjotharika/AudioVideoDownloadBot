from email import message
import pip._vendor.requests 
from telegram import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import os
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, Filters

PORT = int(os.environ.get('PORT', 8443))

def get_Download_URL_From_API(url):
    API_URL = "https://getvideo.p.rapidapi.com/"
    querystring = {"url": f"{url}"}


    headers = {
        'x-rapidapi-host': "getvideo.p.rapidapi.com",
        'x-rapidapi-key': "f46d0d682dmsh95ed9f4dc7225e2p146570jsn1d8f86b7de46"
    }

    response = pip._vendor.requests.request("GET", API_URL, headers=headers, params=querystring)
    data = response.json()
    return data['streams'][0]['url']

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Hello, I am Audio Video Downloader Bot.\nSend the link of video/audio that you want to download')

def textHandler(update: Update, context: CallbackContext) -> None:
    user_message = str(update.message.text)
    
    if update.message.parse_entities(types = MessageEntity.URL):
        download_url = get_Download_URL_From_API(user_message)

        keyboard = [[InlineKeyboardButton("Download", url=download_url)], [InlineKeyboardButton("Support", url='https://www.buymeacoffee.com/gurjots')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(text=f'Click here for download', reply_markup=reply_markup)
        #main()
    else :        
        update.message.reply_text(text=f'Please Enter Vaild Url')

def main():
    TOKEN = "5247525812:AAFn8W_PFEodFXGUPVK7liZoB_d6fRj8MuA"
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, textHandler, run_async=True))
    #updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                      port= int(PORT),
                      url_path = TOKEN,
                      webhook_url = 'https://avdownloader.herokuapp.com/' + TOKEN)
    #updater.idle()

main()
