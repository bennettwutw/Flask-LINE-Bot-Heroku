import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))



@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    
    #　運　算　式
    final = int(f"{get_message}")+5
    # Send To Line
    if  len(get_message) < 5:
        reply = TextSendMessage(text=str(final))
        line_bot_api.reply_message(event.reply_token, reply)
    else :
        ##資料匯入##
        import numpy as np
        import pandas as pd
        data = pd.DataFrame(
    {"name":["前田敦子", "大島優子", "篠田麻里子", "渡邊麻友", 
             "高橋南", "小嶋陽菜", "板野友美"],
     "生日":["1991-7-10", "1988-10-17", "1986-3-11", 
                 "1994-3-26", "1991-4-8", 
                 "1988-4-19", "1991-7-3"],
     "結婚":[True, False, True, False, 
                 False, False, False],
     "身高":[161, 152, 168, 156, 148, np.nan, 154],
     "組別":["A", "K", "A", "B", "A", "A", "K"]})
        output = data.iloc[0, 4]
        #######
        reply = TextSendMessage(text=str(output))
        line_bot_api.reply_message(event.reply_token, reply)
