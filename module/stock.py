from django.conf import settings
import datetime
import requests
import pytz
from linebot import LineBotApi
from linebot.models import TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def exchange_rate(event):
    # 取得資料
    response = requests.get('https://tw.rter.info/capi.php')
    data = response.json().get('USDTWD')
    
    # 取得台灣時間
    tw_timezone = pytz.timezone('Asia/Taipei')
    utc_time = datetime.datetime.strptime(data.get('UTC'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
    tw_time = utc_time.astimezone(tw_timezone)
    tw_time_str = tw_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # 印出結果
    content = f'美金對台幣：{data.get("Exrate")}\n台灣時間：{tw_time_str}'

    try:
        message = [
            TextSendMessage(text = content)
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))