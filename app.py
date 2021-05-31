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
    
    trans_dic = {"台北市":"臺北市", "台中市":"臺中市", "台南市":"臺南市", "台東縣":"臺東縣"}
    if get_message[0:3] in trans_dic:
        get_message = trans_dic[get_message[0:3]]+get_message[3:]    
    
    city_dic = {"基隆市":"c", "臺北市":"a", "新北市":"f", "桃園市":"h", "新竹市":"o", "新竹縣":"j", "苗栗縣":"k", "臺中市":"b", "南投縣":"m", 
               "彰化縣":"n", "雲林縣":"p", "嘉義市":"i", "嘉義縣":"q", "臺南市":"d", "高雄市":"e", "屏東縣":"t", "宜蘭縣":"g", "花蓮縣":"u", 
                "臺東縣":"v", "澎湖縣":"x", "金門縣":"w", "連江縣":"z"}
    if get_message[0:3] in city_dic:
        csv_name = city_dic[get_message[0:3]]+"_lvr_land_a.csv"
    else:
        reply = TextSendMessage(text="系統查無該縣市資料，請再確認。") 
        line_bot_api.reply_message(event.reply_token, reply)
        #break

    #讀取CSV #最近一年 1092、1093、1094、1101
    years = ["real_estate1092","real_estate1093"]
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
########
#讀入1094、1101

    #讀取CSV
    years_2 = ["real_estate1094","real_estate1101"]

    #建立該縣市各年度資料字典
    for year in years_2:
        with open('./data/'+year+'/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                new_row_2 = get_message[0:3] + row[0] + row[2]
                if new_row_2 not in temp_dict: 
                    try:
                        temp_dict[new_row_2 ] = int(row[22])
                    except:
                        continue
                else:
                    try:
                        temp_dict[new_row_2 +"_"+str(num)] = int(row[22])
                        num += 1
                    except:
                        continue


###讀取CSV #2020年 1091、1092、1093、1094(要拆兩次讀取)

    year_2020 = ["real_estate1091","real_estate1092","real_estate1093"]
    #暫存字典
    2020temp_dict = {}
    #後面數字
    num = 0
    import os
    import csv
    #建立該縣市各年度資料字典
    for year in years_2020:
        with open('./data/'+year+'/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[2] not in 2020temp_dict: 
                    try:
                        2020temp_dict[row[2]] = int(row[22])
                    except:
                        continue
                else:
                    try:
                        2020temp_dict[row[2]+"_"+str(num)] = int(row[22])
                        num += 1
                    except:
                        continue

#讀入1094

    #讀取CSV
    years_2020_2 = ["real_estate1094"]

    #建立該縣市各年度資料字典
    for year in years_2020_2:
        with open('./data/'+year+'/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                new_row_2 = get_message[0:3] + row[0] + row[2]
                if new_row_2 not in 2020temp_dict: 
                    try:
                        2020temp_dict[new_row_2 ] = int(row[22])
                    except:
                        continue
                else:
                    try:
                        2020temp_dict[new_row_2 +"_"+str(num)] = int(row[22])
                        num += 1
                    except:
                        continue



###讀取CSV #2019年 1081、1082、1083、1084

    year_2019 = ["real_estate1081","real_estate1082","real_estate1083","real_estate1084"]
    #暫存字典
    2019temp_dict = {}
    #後面數字
    num = 0
    import os
    import csv
    #建立該縣市各年度資料字典
    for year in years_2019:
        with open('./data/'+year+'/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[2] not in 2019temp_dict: 
                    try:
                        2019temp_dict[row[2]] = int(row[22])
                    except:
                        continue
                else:
                    try:
                        2019temp_dict[row[2]+"_"+str(num)] = int(row[22])
                        num += 1
                    except:
                        continue


###讀取CSV #2018年 1071、1072、1073、1074

    year_2018 = ["real_estate1071","real_estate1072","real_estate1073","real_estate1074"]
    #暫存字典
    2018temp_dict = {}
    #後面數字
    num = 0
    import os
    import csv
    #建立該縣市各年度資料字典
    for year in years_2018:
        with open('./data/'+year+'/'+csv_name , newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if row[2] not in 2018temp_dict: 
                    try:
                        2018temp_dict[row[2]] = int(row[22])
                    except:
                        continue
                else:
                    try:
                        2018temp_dict[row[2]+"_"+str(num)] = int(row[22])
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

    for key in temp_dict:  #近一年
        if key[0:len(target)] == target:
            price.append(temp_dict[key])

    2020price = []

    for key in 2020temp_dict:  #2020年
        if key[0:len(target)] == target:
            2020price.append(2020temp_dict[key])

    2019price = []

    for key in 2019temp_dict:  #2019年
        if key[0:len(target)] == target:
            2019price.append(2019temp_dict[key])

    2018price = []

    for key in 2018temp_dict:  #2018年
        if key[0:len(target)] == target:
            2018price.append(2018temp_dict[key])


#排除上下10%  #比例可再調整

    object_number = len(price)
    exclude = object_number // 10

    if object_number < 1:
        reply = TextSendMessage(text="查無相關房價或近一年資料筆數不足1筆。") 
        line_bot_api.reply_message(event.reply_token, reply)
        #break

    2020object_number = len(2020price)
    2020exclude = 2020object_number // 10

    if 2020object_number < 1:
        reply = TextSendMessage(text="查無相關房價或2020年資料筆數不足1筆。") 
        line_bot_api.reply_message(event.reply_token, reply)

    2019object_number = len(2019price)
    2019exclude = 2019object_number // 10

    if 2019object_number < 1:
        reply = TextSendMessage(text="查無相關房價或2019年資料筆數不足1筆。") 
        line_bot_api.reply_message(event.reply_token, reply)  

    2018object_number = len(2018price)
    2018exclude = 2018object_number // 10

    if 2018object_number < 1:
        reply = TextSendMessage(text="查無相關房價或2018年資料筆數不足1筆。") 
        line_bot_api.reply_message(event.reply_token, reply)


####
    
    sorted_price = sorted(price)
    average = sum(sorted_price[exclude:(object_number - exclude)]) / (object_number - 2*exclude)
    average_pin = int(average*3.3058)   #把平均單價轉成以每坪表示
    average_w = average_pin // 10000
    average_d = average_pin % 10000
  
    
    2020sorted_price = sorted(2020price)
    2020average = sum(2020sorted_price[2020exclude:(2020object_number - 2020exclude)]) / (2020object_number - 2*2020exclude)
    2020average_pin = int(2020average*3.3058)   #把平均單價轉成以每坪表示
    2020average_w = 2020average_pin // 10000
    2020average_d = 2020average_pin % 10000

    2019sorted_price = sorted(2019price)
    2019average = sum(2019sorted_price[2019exclude:(2019object_number - 2019exclude)]) / (2019object_number - 2*2019exclude)
    2019average_pin = int(2019average*3.3058)   #把平均單價轉成以每坪表示
    2019average_w = 2019average_pin // 10000
    2019average_d = 2019average_pin % 10000

    2018sorted_price = sorted(2018price)
    2018average = sum(2018sorted_price[2018exclude:(2018object_number - 2018exclude)]) / (2018object_number - 2*2018exclude)
    2018average_pin = int(2018average*3.3058)   #把平均單價轉成以每坪表示
    2018average_w = 2018average_pin // 10000
    2018average_d = 2018average_pin % 10000


    reply = TextSendMessage(text= str(target) + '最近一年的平均價格為每坪' + str(average_w) + '萬' + str(average_d) + '元。'
/n/n
str(target) + '2020年的平均價格為每坪' + str(2020average_w) + '萬' + str(2020average_d) + '元。'
/n
str(target) + '2019年的平均價格為每坪' + str(2019average_w) + '萬' + str(2019average_d) + '元。' 
/n
str(target) + '2018年的平均價格為每坪' + str(2018average_w) + '萬' + str(2018average_d) + '元。')   
    line_bot_api.reply_message(event.reply_token, reply)
