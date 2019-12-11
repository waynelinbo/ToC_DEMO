import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_url

load_dotenv()


machine = TocMachine(
    states=["lobby","psw","A4B4", "lobby_help","psw_help","A4B4_help","psw_done","A4B4_done"],
    transitions=[
        {
            "trigger": "select_game",
            "source": "lobby",
            "dest": "psw",
            "conditions": "is_going_to_psw",
        },
        {
            "trigger": "select_game",
            "source": "lobby",
            "dest": "A4B4",
            "conditions": "is_going_to_A4B4",
        },
        {
            "trigger": "select_game",
            "source": "lobby",
            "dest": "lobby_help",
            "conditions": "is_going_to_lobby_help",
        },
        {
            "trigger": "lobby_help_back",
            "source": "lobby_help",
            "dest": "lobby",
        },
        {
            "trigger": "psw_check",
            "source": "psw",
            "dest": "psw",
            "conditions": "psw_maintain",
        },
        {
            "trigger": "psw_check",
            "source": "psw",
            "dest": "lobby",
            "conditions": "psw_go_back",
        },
        {
            "trigger": "psw_check",
            "source": "psw",
            "dest": "psw_done",
            "conditions": "psw_success",
        },
        {
            "trigger": "psw_check", 
            "source": "psw", 
            "dest": "psw_help",
            "conditions": "is_going_to_psw_help"
        },
        {
            "trigger": "psw_help_back", 
            "source": "psw_help", 
            "dest": "psw",
        },
        {
            "trigger": "psw_done_check",
            "source": "psw_done",
            "dest": "psw",
            "conditions": "psw_again",
        },
        {
            "trigger": "psw_done_check",
            "source": "psw_done",
            "dest": "lobby",
            "conditions": "psw_done_go_back",
        },
        {
            "trigger": "A4B4_check", 
            "source": "A4B4", 
            "dest": "A4B4",
            "conditions": "A4B4_maintain",
        },
        {
            "trigger": "A4B4_check",
            "source": "A4B4",
            "dest": "lobby",
            "conditions": "A4B4_go_back",
        },
        {
            "trigger": "A4B4_check", 
            "source": "A4B4", 
            "dest": "A4B4_done",
            "conditions": "A4B4_success",
        },
        {
            "trigger": "A4B4_check", 
            "source": "A4B4", 
            "dest": "A4B4_help",
            "conditions": "is_going_to_A4B4_help"
        },
        {
            "trigger": "A4B4_help_back", 
            "source": "A4B4_help", 
            "dest": "A4B4",
        },
        {
            "trigger": "A4B4_done_check", 
            "source": "A4B4_done", 
            "dest": "A4B4",
            "conditions": "A4B4_again",
        },
        {
            "trigger": "A4B4_done_check", 
            "source": "A4B4_done", 
            "dest": "lobby",
            "conditions": "A4B4_done_go_back",
        },
    ],
    initial="lobby",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        send_image_url(event.reply_token)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = False

        if machine.state == "lobby":
            response = machine.select_game(event)
        elif machine.state == "psw":
            response = machine.psw_check(event)
        elif machine.state == "A4B4":
            response = machine.A4B4_check(event)
        elif machine.state == "psw_done":
            response = machine.psw_done_check(event)
        elif machine.state == "A4B4_done":
            response = machine.A4B4_done_check(event)

        if response == False:
            send_image_url(event.reply_token, "https://i.imgur.com/crZm2NK.jpg")
            #send_text_message(event.reply_token, "not active instruction")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
