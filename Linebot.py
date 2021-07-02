from flask import Flask, request, abort
from model import selectdb , receipt , formrecognizer_by_url , formrecognizer_by_local
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage , ImageSendMessage
from linebot.exceptions import InvalidSignatureError
import json
import os 

file = os.path.dirname(os.path.realpath(__file__))
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


@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    print('123')
    if message_type =='image':
        message_id = event.message.id
        message_content = line_bot_api.get_message_content(message_id)
        fileName = message_id + '.jpg'

        with open(f'{file}/static/{fileName}' , 'wb')as f:
            a_list = []
            for chunk in message_content.iter_content():
                f.write(chunk)

        image_path = f'{file}/static/{fileName}'
        # image_path = f'https://{request.host}/static/{fileName}' #取得圖片本機網址
        print(image_path)

        number_id = formrecognizer_by_local.formrecognizer_by_local(image_path)
        # number_id = formrecognizer_by_url.formrecognizer_by_url(image_path)
        invoice_date = number_id['日期']     
        print(invoice_date)  
        invoice_number = number_id['發票號碼']  
        data = selectdb.Mongo_select(int(invoice_date))
        # print(data)
        ans = receipt.receipt_mechine([invoice_number] , data)
        # print(ans[0][0])


        if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='你的發票'+ans[0][0]+ans[0][1]+ans[0][2]))
            # line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_path ,preview_image_url=image_path))
            print('ok')

        # print(event.message.text) # 接收用戶訊息

    elif message_type== 'text':
        message = event.message.text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '請給我發票'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "error"))


if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)