from flask import Flask, request, abort
from model import selectdb , receipt
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import json

app = Flask(__name__)

# secretFile = json.load(open("secretFile.txt",'r'))
channelAccessToken = "kjBsbF2p0gYruS/TejEcGgfKn/dL6MgDQSvXP5G0pT09Jm/bLlPbbE3XEovqI5/2MqX4s4A/SAw3/uduRQ7MtzDrsm7Kd+bFi9EIGzCBLmdx+ykt/+R2aqG/a3bAbhO2qp3qfWmuUk8izMMusJcVJAdB04t89/1O/w1cDnyilFU="
channelSecret = "5734e0bf3fbca2b8ab26972585c039a7"

line_bot_api = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)

@app.route('/')
def index():
    return 'hellos man'

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    data = selectdb.Mongo_select(int(event.message.text))
    print(data)
    ans = receipt.receipt_mechine(['46658489'] , data)
    print(ans[0][0])
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='你的發票'+ans[0][0]+ans[0][1]+ans[0][2]))
        print('ok')

        # print(event.message.text) # 接收用戶訊息

if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)