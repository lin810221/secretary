from django.conf import settings
import requests
import time
from lxml import etree
from linebot import LineBotApi
from linebot.models import (TextSendMessage, ImageSendMessage, StickerSendMessage,
                            LocationSendMessage, QuickReply, QuickReplyButton, 
                            MessageAction, TemplateSendMessage, CarouselTemplate,
                            CarouselColumn, MessageTemplateAction, URITemplateAction,
                            PostbackTemplateAction, QuickReplyButton, PostbackAction,
                            CameraAction, CameraRollAction, LocationAction,
                            ImageCarouselTemplate, ImageCarouselColumn,
                            ImagemapSendMessage, BaseSize, MessageImagemapAction,
                            ImagemapArea, URIImagemapAction, ButtonsTemplate,
                            DatetimePickerTemplateAction
                            )

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


"國際原油價格"
def NationalOil(event): 
    url = 'https://toolboxtw.com/zh-TW/detector/gasoline_price'
    response = requests.get(url, verify=False)
    html_str = response.content.decode()
    html = etree.HTML(html_str)

    T = html.xpath('//*[@id="content"]/div/div/div[2]/h2/text()')

    title = html.xpath('//*[@id="content"]/div/div/div[2]/div[4]/table/thead/tr/th/text()')

    data = html.xpath('//*[@id="content"]/div/div/div[2]/div[4]/table/tbody/tr/td/text()')

    content = (T[0] + '\n  ' + 
               title[1] + '：' + data[0] + '\n  ' +
               title[2] + '：' + data[1] + '\n  ' +
               title[3] + '：' + data[2] )

    try:
        message = [
            TextSendMessage(  #傳送文字
                text = content
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



" 木馬轉盤 "
def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤起動囉',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(  # 台灣水庫即時水情
                        thumbnail_image_url = 'https://static.vecteezy.com/system/resources/previews/000/119/586/original/free-effervescent-background-vector.jpg',
                        title = '台灣水庫即時水情',
                        text = '水夠用嗎?',
                        actions = [
                            PostbackTemplateAction(
                                label = '即時水情',
                                data='action=即時水情'
                            ),
                            PostbackTemplateAction(
                                label = '空氣品質指標',
                                data='action=空氣品質指標'
                            ),
                            PostbackTemplateAction(
                                label = '未開發',
                                data='action=NA'
                            ),
                        ]
                    ),
                    CarouselColumn(  # 油價資訊
                        thumbnail_image_url = 'https://n.sinaimg.cn/sinanews/transform/162/w550h412/20220228/5dfa-9a1f68359a23d76140e75f4ddceea77f.jpg',
                        title = '油價資訊',
                        text = 'Oil',
                        actions = [
                            PostbackTemplateAction(
                                label='國際原油價格',
                                data='action=國際原油價格'
                            ),
                            PostbackTemplateAction(
                                label = '中油油價歷史資訊',
                                data='action=中油油價歷史資訊'
                            ),
                            URITemplateAction(
                                label = '資料來源',
                                uri='https://toolboxtw.com/zh-TW/detector/gasoline_price'
                            )
                        ]
                    ),
 
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


" 購買 觸發 "
def sendBack_buy (event, backdata):  #處理Postback
    try:
        text1 = '感謝您的購買，' + backdata.get('action')
        text1 += '\n我們將盡快為您配送。'
        message = TextSendMessage(  #傳送文字
            text = text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


" 一般功能按鍵 "
def sendQuickreply (event):  
    try:
        message = TextSendMessage(
            text='請選擇功能',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=CameraAction(label="拍照")
                    ),
                    QuickReplyButton(
                        action=CameraRollAction(label="相簿")
                    ),
                    QuickReplyButton(
                        action=LocationAction(label="傳送位置")
                    ),                    
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))






