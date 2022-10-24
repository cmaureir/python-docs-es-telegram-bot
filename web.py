import configparser
import hashlib
import hmac
import urllib.parse

import requests
from emoji import emojize
from flask import Flask, Response, abort, request

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config["DEFAULT"]["arigato"]
SECRET = config["DEFAULT"]["shhh"]
CHAT_ID = config["DEFAULT"]["donde"]


def opened_pr_msg(pr):
    mega = emojize(":mega:", use_aliases=True)
    relax = emojize(":relaxed:", use_aliases=True)
    login = pr["user"]["login"]
    msg = (
        f"Nuevo *Pull-Request*! {mega}\n"
        f"-> [{pr['title']}]({pr['html_url']})\n"
        f"Gracias [{login}](https://github.com/{login}) {relax}"
    )
    return msg


def merged_pr_msg(pr):
    docs_url = "https://python-docs-es.readthedocs.io/es/3.8/CONTRIBUTING.html"
    twit_msg = (
        f"Acabo de contribuir a Python con una traducción al español"
        f" del archivo: {pr['html_url']} #PythonDocsEs ¡Únete a la iniciativa! {docs_url}"
    )
    base_url = "https://twitter.com/intent/tweet?text="
    url_twit = f"{base_url}{urllib.parse.quote(twit_msg)}"
    clap = emojize(":clap:", use_aliases=True)
    tada = emojize(":tada:", use_aliases=True)
    login = pr["user"]["login"]
    msg = (
        f"Nuevo *merge*! {tada}{tada}{tada}\n"
        f"-> [{pr['title']}]({pr['html_url']})\n"
        f"Gracias [{login}](https://github.com/{login}) {clap}{clap}{clap} "
        f"puedes [compartirlo en Twitter!]({url_twit})"
    )
    return msg


def process_data(data):
    action = data["action"]
    pr = data["pull_request"]
    try:
        if action == "opened" and not pr["merged"]:
            return opened_pr_msg(pr)
        elif action == "closed" and pr["merged"]:
            return merged_pr_msg(pr)
    except BaseException as e:
        print("Unexpected exception", e)
        return ""


def send_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown", "no_webpage": 1}
    print(requests.post(url, data).json())


@app.route("/webhook", methods=["POST"])
def respond():
    signature = request.headers.get("X-Hub-Signature")
    if not signature or not signature.startswith("sha1="):
        abort(400, "X-Hub-Signature required")

    digest = hmac.new(SECRET.encode("utf-8"), request.data, hashlib.sha1).hexdigest()

    if not hmac.compare_digest(signature, f"sha1={digest}"):
        abort(400, "Invalid Signature")

    data = request.json
    msg = process_data(data)
    print(msg)
    if msg:
        status = send_message(msg)

    return Response(status=200)


if __name__ == "__main__":
    if TOKEN and SECRET and CHAT_ID:
        app.run()
    else:
        print("Error: problem with the configuration")
