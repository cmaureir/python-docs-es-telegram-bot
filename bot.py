import os
import re
import logging
import configparser

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from lib.web import get_progress, get_progress_details
from lib.ghub import get_prs, get_prs_details
from lib.common import clean

from emoji import emojize
from pprint import pprint


def control_test(update, context):
    chat_id = str(update.effective_chat.id).replace("-", "\-")
    pprint(update)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"It's working [123](https://google.de)\nID:{chat_id}",
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

def control_tutoriales(update, context):
    chat_id = str(update.effective_chat.id).replace("-", "\-")
    pprint(update)
    tv = emojize(":tv:", use_aliases=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(f"Video tutoriales {tv}:"
               "\n ▸ [Fork y primeros pasos](https://www.youtube.com/watch?v=OgJQJXrWuu0)"
               "\n ▸ [Creando un Pull\-request](https://www.youtube.com/watch?v=hbHNTIrxSzk)"
               "\n ▸ [Revisando Pull\-request](https://www.youtube.com/watch?v=uIaQMTuwtoU)"
               "\n ▸ [Revisando comentarios en un Pull\-request](https://www.youtube.com/watch?v=SH8HGBPASYY)"
               ),
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
    )

def control_help(update, context):
    msg = (f"Usage:"
           f"\n\t/progress : resumen general"
           f"\n\t/progress <section> : resumen de una <section>\n"
           f"\n\t/prs : lista de todos los PRs abiertos"
           f"\n\t/prs <ID> : detalles de un PR determinado por <ID>"
           f"\n\t/tutoriales : lista de video tutoriales")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=clean(msg),
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )


def get_progress_message(update, context):
    try:
        arg = context.args[0]
    except IndexError:
        arg = ""

    if arg == "":
        msg = get_progress()
    elif arg == "help":
        msg = (f"usage:"
               f"\n\t/progress : to get a general summary"
               f"\n\t/progress <section> : to get the details of the <section>")
    else:
        msg = get_progress_details(arg)

    return msg

def control_progress(update, context):
    msg = get_progress_message(update, context)
    # In case the message is too long
    if len(msg) >= 3000:
        new_msg = ""
        for i in msg.split("\n"):
            new_msg += i + "\n"
            if len(new_msg) > 3000:
                break
        msg = new_msg[:]
        msg += "\n```\n mensaje cortado debido a ser muy largo"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
    )

def get_prs_message(update, context):
    update_msg = (f"Usage:"
                  f"\n\t/prs : to get a list of the open PRs"
                  f"\n\t/prs <ID> : to get the details of the Pull-request <ID>")
    try:
        arg = context.args[0]
    except IndexError:
        arg = ""

    if arg == "":
        msg = get_prs()
    elif arg == "help":
        msg = update_msg
    else:
        try:
            msg = get_prs_details(int(arg))
        except:
            msg = f"Invalid Pull\-request ID: *{arg}*"

    return msg

def control_prs(update, context):
    msg = get_prs_message(update, context)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
    )

def welcome(update, context):
    for new_user_obj in update.message.new_chat_members:
        chat_id = update.message.chat.id
        new_user = ""

        try:
            new_user = "@" + new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name'];

        party = emojize(":tada:", use_aliases=True)
        confetti = emojize(":confetti_ball:", use_aliases=True)
        urldocs = "https://python-docs-es.readthedocs.io/es/3.10/CONTRIBUTING.html"
        msg = (f"Yay! se nos une una nueva persona al grupo {party}\n"
               f"{new_user} recuerda mirar la página para comenzar: {urldocs}\n"
               f"y espera la bienvenida de los miembros actuales! {confetti}")

        context.bot.send_message(chat_id=chat_id,
                                 text=msg,
                                 parse_mode='HTML')


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)

    config = configparser.ConfigParser()
    config.read("config.ini")

    TOKEN = config["DEFAULT"]["Token"]

    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    test_handler = CommandHandler("test", control_test)
    dispatcher.add_handler(test_handler)

    help_handler = CommandHandler("help", control_help)
    dispatcher.add_handler(help_handler)

    progress_handler = CommandHandler("progress", control_progress, pass_args=True)
    dispatcher.add_handler(progress_handler)

    prs_handler = CommandHandler("prs", control_prs, pass_args=True)
    dispatcher.add_handler(prs_handler)

    tutoriales_handler = CommandHandler("tutoriales", control_tutoriales, pass_args=True)
    dispatcher.add_handler(tutoriales_handler)

    welcome_handler = MessageHandler(Filters.status_update.new_chat_members, welcome)
    dispatcher.add_handler(welcome_handler)

    updater.start_polling()
