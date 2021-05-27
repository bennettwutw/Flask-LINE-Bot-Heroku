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
    
    city_dic = {"基隆市":"c", "臺北市":"a", "新北市":"f", "桃園市":"h", "新竹市":"o", "新竹縣":"j", "苗栗縣":"k", "臺中市":"b", "南投縣":"m", 
               "彰化縣":"n", "雲林縣":"p", "嘉義市":"i", "嘉義縣":"q", "臺南市":"d", "高雄市":"e", "屏東縣":"t", "宜蘭縣":"g", "花蓮縣":"u", 
                "臺東縣":"v", "澎湖縣":"x", "金門縣":"w", "連江縣":"z"}
    if get_message[0:3] in city_dic:
        csv_name = city_dic[get_message[0:3]]+"_lvr_land_a.csv"
    else:
        reply = TextSendMessage(text="系統查無該縣市資料，請再確認。") 
        line_bot_api.reply_message(event.reply_token, reply)
        #break
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
        with open('./data/'+year+'/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[2] not in temp_dict: 
                    try:
                        temp_dict[row[2]] = int(row[22])
                    except:
                        continue
                else:
                    try:
                        temp_dict[row[2]+"_"+str(num)] = int(row[22])
                        num += 1
                    except:
                        continue
#########
    
    input_address = get_message

    if '段' in input_address:
        road_address = input_address.split('段')
        road_address[0] = road_address[0]+'段'
    elif '路' in input_address:
        road_address = input_address.split('路')
        road_address[0] = road_address[0]+'路'
    elif '街' in input_address:
        road_address = input_address.split('街')
        road_address[0] = road_address[0]+'街'
    elif '大道' in input_address:
        road_address = input_address.split('大道')
        road_address[0] = road_address[0]+'大道'
    else:
        reply = TextSendMessage(text="您輸入的地址有誤或尚未開放查詢，請再確認。") 
        line_bot_api.reply_message(event.reply_token, reply)
        #break
#只要路名相同的門牌都列入，抓取其單價

    target = road_address[0]
    price = []

    for key in temp_dict:
        if key[0:len(target)] == target:
            price.append(temp_dict[key])

#排除上下10%  #比例可再調整

    object_number = len(price)
    exclude = object_number // 10

    if object_number < 3:
        reply = TextSendMessage(text="查無相關房價或資料筆數不足3筆。") 
        line_bot_api.reply_message(event.reply_token, reply)
        #break
    
    sorted_price = sorted(price)
    average = sum(sorted_price[exclude:(object_number - exclude)]) / (object_number - 2*exclude)
    average_pin = int(average*3.3058)   #把平均單價轉成以每坪表示


    if object_number < 1:
        reply = TextSendMessage(text="查無相關房價。") 
        line_bot_api.reply_message(event.reply_token, reply)
    else:  
        reply = TextSendMessage(text=str(target) + '的平均價格為每坪' + str(average_pin) + '元。')   
        line_bot_api.reply_message(event.reply_token, reply)
