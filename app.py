from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import yaml
import random
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
                    text:
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
import re
data = {}
id_name_table = {}

CHINESE_NUM = ["零","一","二","三","四","五","六","七","八","九","十"]
SQUAD_NUM = 14 # 每班有幾人
MESSAGE_MAX_WORD = 900


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


# CONSTANT_TIME = {
#     "morning": {
#         "start":datetime.time(0,0), # TODO print
#         "end": datetime.time(2, 15)
#     },
#     "night": {
#         "start":datetime.time(2,16),
#         "end": datetime.time(4, 0)
#     }
# }


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


def timestamp2datetime(timestamp):
    # it could be change to other format (EX: real timestamp * remember to modify datetime2timestamp function too)
    return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
def datetime2timestamp(datetime_):
    return datetime_.strftime("%Y-%m-%d %H:%M")


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

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
        data[group_id] = data.get(group_id, {})

        now = datetime.datetime.now()

        report_mode = getTimeMode(now)
        
        if report_mode=="morning" or report_mode=="night":
            m = re.search("(?<=學號姓名[：:\ ])[0-9]*", text)
            if m:
                ID = m.group(0)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請確認回報格式(學號格式不正確)"))
                return

            ID_int = int(ID[-3:]) # "50090" => 90 or "090" => 90 or "90" => 90
            data[group_id][ID_int] = data[group_id].get(ID_int, {}) 
            data[group_id][ID_int][report_mode] = data[group_id][ID_int].get(report_mode, {"timestamp":"2021-01-01 00:01", "text":""})
            ori_datetime = timestamp2datetime(data[group_id][ID_int][report_mode]["timestamp"])
            
            data[group_id][ID_int][report_mode]["timestamp"] = datetime2timestamp(now)
            data[group_id][ID_int][report_mode]["text"] = text
            
            if ori_datetime.date() < now.date():
                reply_message = "{}-收到回報".format(ID[-3:])
            else:
                reply_message = "{}-已更新回報內容".format(ID[-3:])



            # TODO check format and reply message (low priority) 
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            return 

        else:
            message = """抱歉，現在非回報時間\n早上回報請於{morning_start} - {morning_end},\n晚上回報請於{night_start} - {night_end}, \n謝謝""".format(
            morning_start = CONSTANT_TIME["morning"]["start"].strftime("%H:%M"), 
            morning_end = CONSTANT_TIME["morning"]["end"].strftime("%H:%M"), 
            night_start=CONSTANT_TIME["night"]["start"].strftime("%H:%M"), 
            night_end=CONSTANT_TIME["night"]["end"].strftime("%H:%M"))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
            return
    elif "統整回報" == text:

        reply_messages = []
        now = datetime.datetime.now()
        report_mode = getTimeMode(now)
        if report_mode=="morning":
            reply_messages.append(TextSendMessage(text="早上回報統整"))
        elif report_mode == "night":
            reply_messages.append(TextSendMessage(text="晚上回報統整:"))
        if not data.get(group_id, {}):
            reply_messages.append(TextSendMessage(text="尚未有人回報"))
        else:
            squad = ((int(list(data[group_id].keys())[0])-1)//SQUAD_NUM) + 1
            report_text = []
            not_report_id = []
            text_count = 0
            start_key = (squad-1)*SQUAD_NUM+1
            for key in range((squad-1)*SQUAD_NUM+1, squad*SQUAD_NUM+1):
                if key in data[group_id] and (key==90 or timestamp2datetime(data[group_id][key].get(report_mode, {"timestamp":"2021-01-01 00:01"})["timestamp"]).date() == now.date()):
                    # print(text_count, len(data[group_id][key][report_mode]["text"]))
                    if text_count + len(data[group_id][key][report_mode]["text"]) > MESSAGE_MAX_WORD:
                        reply_messages.append(TextSendMessage(text="第{}班 ({:03d}-{:03d})\n".format(CHINESE_NUM[squad], start_key, key-1) + "\n\n".join(report_text)))
                        report_text = []
                        start_key = key
                        text_count = 0
                    report_text.append(data[group_id][key][report_mode]["text"])
                    text_count += len(data[group_id][key][report_mode]["text"])
                else:
                    not_report_id.append(str(key))
         
            if len(not_report_id)==SQUAD_NUM:
                reply_messages.append(TextSendMessage(text="尚未有人回報"))
            else:
                reply_messages.append(TextSendMessage(text="第{}班 ({:03d}-{:03d})\n".format(CHINESE_NUM[squad], start_key, key) + "\n\n".join(report_text)))
                if not_report_id:
                    reply_messages.append(TextSendMessage(text="尚未回報人員: {}".format(", ".join(not_report_id))))
                else:
                    reply_messages.append(TextSendMessage(text="全員皆已回報，可以貼到大群記事本囉"))
            
        line_bot_api.reply_message(event.reply_token, reply_messages)
    elif "清空回報" == text:
        if group_id in data:
            data[group_id] = {}
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已清空回報資料"))
    
    elif "說明" == text:
        reply_message = "使用說明:\n\n1. 送出回報後，回報小幫手會回復 \"收到回報\"。\n\n2.如果回報小幫手甚麼都沒說，可能是它在圍爐過年，請再貼一次回報看看，或通知 090-陳昱名\n\n3. 如果要更新回報資訊，再回報一次即可\n\n4. 要統整回報，請打 \"統整回報\"\n\nP.S. 回報時，學號請拜託千萬要打對"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    elif "新年快樂" in text:
        congrad = ["恭賀新年、祝福心想事成","新年快樂，祝賀佳節愉快","祝你新年萬事如意，闔家平安","祝您在未來的一年裏吉星高照","祝福你，新年吉祥如意、事業財源廣進、感情處處逢緣！","祝您萬事都順心，新年快樂！","祝您在新的一年，財旺人旺凡事旺，天泰地泰三陽泰，人和事和萬事和。","祝年終滿荷包，幸福永遠繞。"]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=random.choice(congrad)))
    else:
        user_id = event.source.user_id
        # name = id_name_table.get(user_id, None)
        name = user_id
        if not name:
            profile = line_bot_api.get_profile(user_id)
            name = id_name_table[user_id] = profile.display_name
        with open("log/{}.log".format(group_id),"a") as f:
            content  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " " + name + "\n" +  text + "\n\n"
            f.write(content)


import atexit

def exit_handler():
    # print(data)
    with open("data.yml", "w") as f:
        yaml.dump(data, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    with open("id_name_table.yml", "w") as f:
        yaml.dump(id_name_table, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)

atexit.register(exit_handler)


import os
if __name__ == "__main__":

    if os.path.isfile("data.yml"):
        with open("data.yml") as f:
            data = yaml.safe_load(f)
        
    else:
        os.mknod("data.yml")
        data = {}
        with open("data.yml", "w") as f:
            yaml.dump(data, f, default_flow_style=False, Loader=yaml.FullLoader)

    if os.path.isfile("id_name_table.yml"):
        with open("id_name_table.yml") as f:
            id_name_table = yaml.safe_load(f)

    else:

        os.mknod("id_name_table.yml")
        id_name_table = {}
        with open("id_name_table.yml", "w") as f:
            # yaml.dump(id_name_table, f, default_flow_style=False, Loader=yaml.FullLoader)
            yaml.dump(id_name_table, f, default_flow_style=False)



    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=port, ssl_context=('/home/archsearch/ssl_csr/nginx_bundle_d40133d96d13.crt', '/home/archsearch/ssl_csr/moana.210206.key'))
    # return app