
#############以下先勿動#############
    
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
        data = pd.read_csv("./test_data.csv")
        output = data.iloc[1, 4]
        #######
        reply = TextSendMessage(text=str(output))
        line_bot_api.reply_message(event.reply_token, reply)
