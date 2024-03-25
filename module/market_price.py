from django.conf import settings
import requests
from lxml import etree
from linebot import LineBotApi
from linebot.models import TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

"國際原油價格"
def national_oil(event): 
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