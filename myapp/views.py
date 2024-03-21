from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import func, Stock, LIFF
from urllib.parse import parse_qsl

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                # 處理位置
                if event.message.type == 'location':
                    func.AQI(event)
                
                # 處理文字訊息
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if (mtext == '轉盤' or mtext == "A"):
                        func.sendCarousel (event)
    
                    elif mtext == '功能':
                        func.sendQuickreply(event)
                    
                    elif mtext == "@COVID19":
                        func.Covid19(event)

                    elif mtext == 'B': # 練習
                        func.sendImgCarousel(event)

                    elif mtext == 'C':  # 練習
                        func.sendImgmap(event)
    
                    elif mtext == 'D':  # 練習
                        func.sendDatetime(event)
					
                    elif mtext == 'L':
                        LIFF.sendFlex(event)

                    elif mtext == '@contact':
                        LIFF.contact(event)
                    
            #PostbackTemplateAction觸發此事件
            if isinstance(event, PostbackEvent):
                #取得Postback資料
                backdata = dict(parse_qsl(event.postback.data))
                
                if backdata.get ('action') == 'buy':
                    func.sendBack_buy (event, backdata) 

                elif backdata.get ('action') == '加權指數':
                    Stock.sendMulti (event, backdata)

                elif backdata.get ('action') == '各類指數':
                    Stock.sendMulti_1 (event, backdata)
                
                elif backdata.get ('action') == '資金走向':
                    Stock.sendMulti_2 (event, backdata)

                elif backdata.get('action') == 'sell': # 練習
                    func.sendData_sell(event, backdata)
                
                elif backdata.get('action') == '即時水情':
                    func.Waters(event)
                
                elif backdata.get('action') == '空氣品質指標':
                    func.AQI_char(event)
                
                elif backdata.get('action') == '中油油價歷史資訊':
                    func.Oil(event)
                
                elif backdata.get('action') == '國際原油價格':
                    func.NationalOil(event)

    
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
