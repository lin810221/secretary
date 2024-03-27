from django.conf import settings
import requests
import time
from datetime import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models import ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def send_message(event, message):
    try:
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))



" 水庫即時水情 "
def waters(event): 
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


" 溫度分布圖 "
def tempw(event):
    img_url = 'https://www.cwa.gov.tw/Data/temperature/tempw.jpg'
    text = '溫度分布圖'
    message = [TextSendMessage(text),
               ImageSendMessage(original_content_url = img_url, preview_image_url = img_url)]
    send_message(event, message)

" 累積雨量 "
def rainfall(event):
    date = time.strftime("%Y-%m-%d")
    hour = time.strftime("%H")
    rainfall_url = f'https://www.cwa.gov.tw/Data/rainfall/{date}_{hour}00.QZJ8.jpg'
    message = [
            TextSendMessage('累積雨量'),
            ImageSendMessage(original_content_url = rainfall_url, preview_image_url = rainfall_url)
            ]
    send_message(event, message)

" 紫外線觀測 "
def UVI(event):
    # 即時觀測
    real_time_url = 'https://www.cwa.gov.tw/Data/UVI/UVI_CWB.png'
    
    # 今日最大值
    maximum_value_url = 'https://www.cwa.gov.tw/Data/UVI/UVI_Max_CWB.png'
    
    message = [
            TextSendMessage('即時觀測'),
            ImageSendMessage(original_content_url = real_time_url, preview_image_url = real_time_url),
            TextSendMessage('今日最大值'),
            ImageSendMessage(original_content_url = maximum_value_url, preview_image_url = maximum_value_url)
            ]
    send_message(event, message)



" 雷達回波 "
def obs_radar(event):
    radar_url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0058-003?Authorization=rdec-key-123-45678-011121314&format=JSON'
    radar = requests.get(radar_url)        # 爬取資料
    radar_json = radar.json()              # 使用 JSON 格式
    radar_img = radar_json['cwaopendata']['dataset']['resource']['ProductURL']  # 取得圖片網址
    rader_des = radar_json['cwaopendata']['dataset']['resource']['resourceDesc']
    rader_date = radar_json['cwaopendata']['sent']
    rader_date = datetime.fromisoformat(rader_date).strftime('%Y-%m-%d %H:%M:%S')

    try:
        message = [
            TextSendMessage(f'{rader_des}\n{rader_date}'),
            ImageSendMessage(original_content_url = radar_img, preview_image_url = radar_img),
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