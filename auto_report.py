from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import yaml
import datetime
import os
app = Flask(__name__)

assert os.path.isfile("token.yml")

with open("token.yml") as f:
    temp = yaml.safe_load(f)
    token = temp["millitary_auto_report"]["token"]
    secret = temp["millitary_auto_report"]["secret"]

# Channel Access Token
line_bot_api = LineBotApi(token) # Line token
# Channel Secret
handler = WebhookHandler(secret) # Line secret

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



@app.route('/hello')
def hello():
    return 'Hello, World!'


CONSTANT_TIME = {
    "morning": {
        "start":datetime.time(7,0), 
        "end": datetime.time(13, 30)
    },
    "night": {
        "start":datetime.time(14,0),
        "end": datetime.time(22, 0)
    }
}


def isTimeInTimePeriod(startTime, endTime, _time): 
    if startTime < endTime: 
        return _time >= startTime and _time <= endTime 
    else: 
        #Over midnight: 
        return _time >= startTime or _time <= endTime 

def getTimeMode(_time):
    mode = "other"
    if isTimeInTimePeriod(CONSTANT_TIME["morning"]["start"], CONSTANT_TIME["morning"]["end"], _time.time()):
        mode = "morning"
    elif isTimeInTimePeriod(CONSTANT_TIME["night"]["start"], CONSTANT_TIME["night"]["end"], _time.time()):
        mode = "night"
    else:
        mode = "other"
    return mode



REPORT = {
    "morning": "學號姓名：50090-陳昱名\n人員現況：在家\n健康狀況：正常\n有無飲酒：無\n有無與境外人士接觸：無\n聯絡電話：0937211100",
    "night" : "學號姓名：50090-陳昱名\n人員現況：在家用電腦\n健康狀況：正常\n有無飲酒：無\n有無與境外人士接觸：無\n2200後動態：在家\n明日行程：在家用電腦\n聯絡電話：0937211100",
    "return": "學號姓名：50090-陳昱名\n人員現況：出發吃午餐\n健康狀況：正常\n有無飲酒：無\n有無與境外人士接觸：無\n聯絡電話：0937211100\n返營方式：專車"
}



report_history = {
    "morning": datetime.datetime(2021,1,1,12,1),
    "night": datetime.datetime(2021,1,1,12,1),
    "return": datetime.datetime(2021,1,1,12,1)
}
# 處理訊息
report_count = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global report_count
    group_id = None
    text = None

    
    if event.source.type != "group":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="抱歉，本服務目前僅提供給群組使用，請先邀請我到群組"))
        return
    else:
        # print(event.source)
        group_id = event.source.group_id
    
    
    text = event.message.text

    
    if "學號姓名" in text:
        report_count += 1
        now = datetime.datetime.now()
        if report_count >=2:
            
            if "返營方式" in text:
                mode = "return"
            else:
                mode = getTimeMode(now)
            
            
            if mode == "other":
                #TODO push message to admin
                pass
            else:
                if report_history.get(mode, datetime.datetime(2021,1,1,12,1)).date() != now.date():
                    print(report_history.get(mode, datetime.datetime(2021,1,1,12,1)), now.date())
                    report_history[mode] = now
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=REPORT[mode]))
                report_count = 0
                
            return

import os
if __name__ == "__main__":

    # if os.path.isfile("data.yml"):
    #     with open("data.yml") as f:
    #         data = yaml.safe_load(f)
        
    # else:
    #     os.mknod("data.yml")
    #     data = {}
    #     with open("data.yml", "w") as f:
    #         yaml.dump(data, f, default_flow_style=False, Loader=yaml.FullLoader)

    # if os.path.isfile("id_name_table.yml"):
    #     with open("id_name_table.yml") as f:
    #         id_name_table = yaml.safe_load(f)

    # else:

    #     os.mknod("id_name_table.yml")
    #     id_name_table = {}
    #     with open("id_name_table.yml", "w") as f:
    #         # yaml.dump(id_name_table, f, default_flow_style=False, Loader=yaml.FullLoader)
    #         yaml.dump(id_name_table, f, default_flow_style=False)



    port = int(os.environ.get('PORT', 5050))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port, ssl_context=('/home/archsearch/ssl_csr/nginx_bundle_d40133d96d13.crt', '/home/archsearch/ssl_csr/moana.210206.key'))
    # return app