import logging
import os

import telegram as tg
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import wikipedia


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    reply_keyboard = [['Done']]
    markup = tg.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Бот-гид по Википедии', reply_markup=markup)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def button(bot, update):
    query = update.callback_query
    print('query', query, 'update', update)
    bot.send_chat_action(chat_id=query.message.chat_id, action=tg.ChatAction.TYPING)
    text, markup = prepare_search(query.data)
    if not text:
        bot.send_message(chat_id=query.message.chat_id, text=f'Не найдено ({query.data})')
        return
    bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                          text=text, parse_mode=tg.ParseMode.MARKDOWN)
    bot.send_message(chat_id=query.message.chat_id, text='Другие варианты:', reply_markup=markup)
    # update.message.reply_text(text="Selected option: {}".format(query.data))


def search(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=tg.ChatAction.TYPING)
    text, markup = prepare_search(update.message.text)
    if not text:
        bot.send_message(chat_id=update.message.chat_id, text='Не найдено')
        return
    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=tg.ParseMode.MARKDOWN)
    bot.send_message(chat_id=update.message.chat_id, text='Другие варианты:', reply_markup=markup)


def handle_suggestion(pageid, lang='ru'):
    res, sugs = wikipedia.get_page_data(pageid, lang)
    if not res:
        return False, None
    keyboard = [[tg.InlineKeyboardButton(one.text, callback_data=one.pageid) for one in sugs]]
    markup = tg.InlineKeyboardMarkup(keyboard)
    text = f'*{res.title}*\n{res.text}\n\n[Wikipedia]({res.url})'
    return text, markup


def prepare_search(search_term, lang='ru'):
    res, sugs = wikipedia.search(search_term, lang)
    if not res:
        return False, None
    keyboard = [[tg.InlineKeyboardButton(one[0], callback_data=one[1]) for one in sugs]]
    markup = tg.InlineKeyboardMarkup(keyboard)
    text = f'*{res.title}*\n{res.text}\n\n[Wikipedia]({res.url})'
    return text, markup


def main():
    # token = os.environ['TOKEN']
    token = '661552335:AAFayyfheskU2pBhdtQ0g3m0A2CqByUYFkI'
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, search))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
