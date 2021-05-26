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
    
    #縣市對應代碼
    city_dic = {"基隆市":"c", "臺北市":"a", "新北市":"f", "桃園市":"h", "新竹市":"o", "新竹縣":"j", "苗栗縣":"k", "臺中市":"b", "南投縣":"m", 
               "彰化縣":"n", "雲林縣":"p", "嘉義市":"i", "嘉義縣":"q", "臺南市":"d", "高雄市":"e", "屏東縣":"t", "宜蘭縣":"g", "花蓮縣":"u", 
                "臺東縣":"v", "澎湖縣":"x", "金門縣":"w", "連江縣":"z"}
    if get_message[0:2] in city_dic:
        csv_name = city_dic[get_message[0:2]]+"_lvr_land_a.csv"
    
    #讀取CSV
    years = ["real_estate1071","real_estate1072","real_estate1073","real_estate1074","real_estate1081","real_estate1082","real_estate1083",
             "real_estate1084","real_estate1091","real_estate1092","real_estate1093"]
    #暫存字典
    temp_dict = {}
    #後面數字
    num = 0
    import os
    import csv
    #建立該縣市各年度資料字典
    for year in years:
        with open('./data/'+'year/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[2] not in temp_dict: 
                    temp_dict[row[2]] = int(row[22])
                else:
                    temp_dict[row[2]+"_"+str(num)] = int(row[22])
                    num += 1
    #針對輸入資料解析
    count = 0 #可用資料筆數
    money = 0 #金額總數
    for data in temp_dict:
        if get_message in data:
            count += 1
            money += int(temp_dict[data])
        else:
            continue
    average = money / count
    reply = TextSendMessage(text=str(average))
        line_bot_api.reply_message(event.reply_token, reply)

