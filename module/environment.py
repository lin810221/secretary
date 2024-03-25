from django.conf import settings
import requests
import time
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models import ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

" 水庫即時水情 "
def Waters(event): 
    url = 'https://www.taiwanstat.com/waters/latest'
    response = requests.get(url)
    data = response.json()
    data = data[0]
    content = ''
    
    for i in data:
        name = data[i]['name'] # 水庫名稱
        value = data[i]['volumn'] # 有效蓄水量
        perc = data[i]['percentage'] # 蓄水百分比
        updateTime = data[i]['updateAt'] # 更新時間
        content += f'水庫名稱：{name}\n有效蓄水量：{value}萬立方公尺\n蓄水百分比：{perc}%\n更新時間：{updateTime}\n\n'

    try:
        message = TextSendMessage(text = content)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" AQI圖表 "
def AQI_char(event): 
    # 資料參考：https://airtw.epa.gov.tw/ModelSimulate/20220529/output_AQI_20220529150000.png
    timeString = time.strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
    t = time.strftime("%Y%m%d%H")
    t ='https://airtw.epa.gov.tw/ModelSimulate/' + t[:8] + '/output_AQI_' + t + '0000.png'
    text = '全國空氣品質指標\n' + timeString

    try:
        message = [
            TextSendMessage(text),
            #傳送圖片
            ImageSendMessage(original_content_url = t, preview_image_url = t)
            ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 空氣品質指標 "
def AQI(event):       
    try:
        message = TextSendMessage(text = 'Page Not Found')
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))