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


def control_test(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="It's working [123](https://google.de)",
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

def control_help(update, context):
    msg = (f"Usage:"
           f"\n\t/progress : to get a general summary"
           f"\n\t/progress <section> : to get the details of the <section>\n"
           f"\n\t/prs : to get a list of the open PRs"
           f"\n\t/prs <ID> : to get the details of the Pull-request <ID>")
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

    updater.start_polling()
