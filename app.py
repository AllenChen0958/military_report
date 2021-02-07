from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import yaml

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('nR+N0rlAHNQYmeGxkTEgaMmMN0Wc4Tos2PveR3VxrfqJijzG75a4w7gVlcIq/Lkz8OjbhdUfjZLKCx6uxtGkRcfLHy4iKQddGLYwPF9HQZMAXNkD2BnBq2v0zCEd90IgWk8jNcDtgayy6Ai7eQFnVwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e53bdc0200da932a63dfb19753a7df56')

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


# TODO: 
"""


{
    group_id:
        85:
            {
                
                morning: {
                    timestamp:
                    content:
                },
                afternoon: {
                        
                }
            }
        86:
        87:
        88:
        ....
        ....
    
    


}


step0. check key word (report, ID name)

step1. 
    search by group id

step2. 
    check id 


step3 
    check date


step4 
    check time
"""


import datetime
data = {}

# MORNING_START = datetime.time(7,0)
# MORNING_END = datetime.time(13, 30)

# NIGHT_START = datetime.time(14,0)
# NIGHT_END = datetime.time(22, 0)

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


def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):


    # text = event.message.text
    # if "學號姓名" in text:
    #     text = "yoyoyo"
    # message = TextSendMessage(text=text)
    
    
    # line_bot_api.reply_message(event.reply_token, message)



    # print(event.source)
    # line_bot_api.reply_message(event.reply_token, message)
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="test"))

    # try:
    #     if event.type != "group":
    #         error_msg = "抱歉，本服務目前僅提供給群組使用，不開放個別用戶使用"
    #         raise NotImplmentedError

    # except NotImplmentedError:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_msg))
    #     return


    error_msg = "Sorry, some kind of error has occurred. Please contact the administrater."
    # check type
    
    # nonlocal data
    print(data)
    group_id = None
    text = None

    
    if event.source.type != "group":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="抱歉，本服務目前僅提供給群組使用，不開放個別用戶使用"))
        return
    else:
        print(event.source)
        group_id = event.source.group_id
    
    
    text = event.message.text
    if "學號姓名" in text:
        group_data = data.get(group_id, {})
        now = datetime.datetime.now()
        if isNowInTimePeriod(CONSTANT_TIME["morning"]["start"], CONSTANT_TIME["morning"]["end"], now.time()) and False:
            pass
        elif isNowInTimePeriod(CONSTANT_TIME["night"]["start"], CONSTANT_TIME["night"]["end"], now.time()) and False:
            pass
        else:
            message = """抱歉，現在非回報時間\n早上回報請於{morning_start} - {morning_end},\n晚上回報請於{night_start} - {night_end}, \n謝謝""".format(
            morning_start = CONSTANT_TIME["morning"]["start"].strftime("%H:%M"), 
            morning_end = CONSTANT_TIME["morning"]["end"].strftime("%H:%M"), 
            night_start=CONSTANT_TIME["night"]["start"].strftime("%H:%M"), 
            night_end=CONSTANT_TIME["night"]["end"].strftime("%H:%M"))

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    elif "統整回報" in text:
        pass
    elif "新年快樂" in text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="妳各位新年快樂"))




import os
if __name__ == "__main__":

    if os.path.isfile("data.yml"):
        with open("data.yml") as f:
            data = yaml.safe_load(f)
    else:
        os.mknod("data.yml")
        data = {}
        with open("data.yml", "w") as f:
            yaml.dump(data, f, default_flow_style=False)
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port, ssl_context=('/home/archsearch/ssl_csr/nginx_bundle_d40133d96d13.crt', '/home/archsearch/ssl_csr/moana.210206.key'))
    # return app