from django.conf import settings
import requests
import time
from lxml import etree
from linebot import LineBotApi
from linebot.models import TextSendMessage # 發送文字訊息
from linebot.models import ImageSendMessage # 發送圖片訊息
from linebot.models import StickerSendMessage # 發送貼圖訊息
from linebot.models import LocationSendMessage # 發送位置訊息
from linebot.models import QuickReply # 快速回覆功能，用於在訊息中提供快速回覆選項
from linebot.models import QuickReplyButton # 快速回覆按鈕，用於快速回覆中的選項
from linebot.models import MessageAction # 訊息動作，用於快速回覆按鈕中的動作
from linebot.models import TemplateSendMessage # 模板訊息，用於發送包含樣式化內容的訊息
from linebot.models import CarouselTemplate # 輪播模板，用於在訊息中顯示多個選項，可以左右滑動
from linebot.models import CarouselColumn # 輪播模板中的一列
from linebot.models import MessageTemplateAction # 模板訊息中的訊息動作
from linebot.models import URITemplateAction # 模板訊息中的URI動作，用於開啟網頁
from linebot.models import PostbackTemplateAction # 用於模板訊息中，可用於按鈕模板等場景
from linebot.models import PostbackAction # 模板訊息中的Postback動作，用於觸發後端處理
from linebot.models import CameraAction # 相機動作，用於啟動用戶端相機
from linebot.models import CameraRollAction # 相機捲動動作，用於啟動用戶端相機捲動功能
from linebot.models import LocationAction # 位置動作，用於在地圖中選擇位置
from linebot.models import ImageCarouselTemplate # 圖片輪播模板，與輪播模板類似，但是每個選項都是圖片
from linebot.models import ImageCarouselColumn # 圖片輪播模板中的一列
from linebot.models import ImagemapSendMessage # 圖像地圖訊息，用於發送包含可點擊區域的圖像
from linebot.models import BaseSize # 圖像地圖區域的基本大小
from linebot.models import MessageImagemapAction # 圖像地圖動作，用於在圖像地圖中觸發訊息動作
from linebot.models import ImagemapArea # 圖像地圖區域，用於定義可點擊區域
from linebot.models import URIImagemapAction # 圖像地圖動作，用於在圖像地圖中開啟URI
from linebot.models import ButtonsTemplate # 按鈕模板，用於在訊息中顯示包含按鈕的樣式化內容
from linebot.models import DatetimePickerTemplateAction # 日期時間選擇器模板動作，用於在按鈕模板中提供日期時間選擇功能
                            

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
                            ),
                            PostbackTemplateAction(
                                label = '未開發',
                                data='action=NA'
                            ),
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






