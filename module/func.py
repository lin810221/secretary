from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage                  # 發送文字訊息
from linebot.models import ImageSendMessage                 # 發送圖片訊息
from linebot.models import StickerSendMessage               # 發送貼圖訊息
from linebot.models import LocationSendMessage              # 發送位置訊息
from linebot.models import QuickReply                       # 快速回覆功能，用於在訊息中提供快速回覆選項
from linebot.models import QuickReplyButton                 # 快速回覆按鈕，用於快速回覆中的選項
from linebot.models import MessageAction                    # 訊息動作，用於快速回覆按鈕中的動作
from linebot.models import TemplateSendMessage              # 模板訊息，用於發送包含樣式化內容的訊息
from linebot.models import CarouselTemplate                 # 輪播模板，用於在訊息中顯示多個選項，可以左右滑動
from linebot.models import CarouselColumn                   # 輪播模板中的一列
from linebot.models import MessageTemplateAction            # 模板訊息中的訊息動作
from linebot.models import URITemplateAction                # 模板訊息中的URI動作，用於開啟網頁
from linebot.models import PostbackTemplateAction           # 用於模板訊息中，可用於按鈕模板等場景
from linebot.models import PostbackAction                   # 模板訊息中的 Postback 動作，用於觸發後端處理
from linebot.models import CameraAction                     # 相機動作，用於啟動用戶端相機
from linebot.models import CameraRollAction                 # 相機捲動動作，用於啟動用戶端相機捲動功能
from linebot.models import LocationAction                   # 位置動作，用於在地圖中選擇位置
from linebot.models import ImageCarouselTemplate            # 圖片輪播模板，與輪播模板類似，但是每個選項都是圖片
from linebot.models import ImageCarouselColumn              # 圖片輪播模板中的一列
from linebot.models import ImagemapSendMessage              # 圖像地圖訊息，用於發送包含可點擊區域的圖像
from linebot.models import BaseSize                         # 圖像地圖區域的基本大小
from linebot.models import MessageImagemapAction            # 圖像地圖動作，用於在圖像地圖中觸發訊息動作
from linebot.models import ImagemapArea                     # 圖像地圖區域，用於定義可點擊區域
from linebot.models import URIImagemapAction                # 圖像地圖動作，用於在圖像地圖中開啟 URI
from linebot.models import ButtonsTemplate                  # 按鈕模板，用於在訊息中顯示包含按鈕的樣式化內容
from linebot.models import DatetimePickerTemplateAction     # 日期時間選擇器模板動作，用於在按鈕模板中提供日期時間選擇功能
                            
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)




" 木馬轉盤 "
def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤起動囉',
            template=CarouselTemplate(
                columns=[
                    # 天氣資訊
                    CarouselColumn(  
                        thumbnail_image_url = 'https://www.crazybackground.com/wp-content/uploads/2019/12/vector-chinese-clouds.jpg',
                        title = '天氣資訊',
                        text = 'Temperature and Humidity',
                        actions = [
                            PostbackTemplateAction(
                                label = '溫度分布圖',
                                data='action=溫度分布圖'
                            ),
                            PostbackTemplateAction(
                                label='累積雨量',
                                data='action=累積雨量'
                            ),
                            PostbackTemplateAction(
                                label = '紫外線觀測',
                                data='action=紫外線觀測'
                            ),
                        ]
                    ),
                    # 台灣水庫即時水情
                    CarouselColumn(  
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
                                label = '雷達回波',
                                data='action=雷達回波'
                            ),
                        ]
                    ),
                    # 油價資訊
                    CarouselColumn(  
                        thumbnail_image_url = 'https://n.sinaimg.cn/sinanews/transform/162/w550h412/20220228/5dfa-9a1f68359a23d76140e75f4ddceea77f.jpg',
                        title = '油價資訊',
                        text = 'Oil',
                        actions = [
                            PostbackTemplateAction(
                                label='國際原油價格',
                                data='action=國際原油價格'
                            ),
                            PostbackTemplateAction(
                                label = '匯率',
                                data='action=匯率'
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






