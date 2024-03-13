from django.conf import settings

from linebot import LineBotApi
from linebot.models import (TextSendMessage, ImageSendMessage, StickerSendMessage,
                            LocationSendMessage, QuickReply, QuickReplyButton, 
                            MessageAction)
import datetime 
import yfinance as yf
import matplotlib.pyplot as plt
import pyimgur
import mpl_finance as mpf

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

" 運用 yfinance 做股市K線圖 "
def sendMulti(event, mtext):
    stock_number = mtext.split(" ")[1]
    start = (datetime.datetime.now() +
             datetime.timedelta(days=-30)).strftime("%Y-%m-%d")
    end = (datetime.datetime.now() +
           datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    df = yf.download(stock_number,
                     start = start,
                     end = end)
    #df = df.reset_index()


    Data_Open = df.iat[-1,-6]
    Data_High = df.iat[-1,-5]
    Data_Low = df.iat[-1,-4]
    Data_Close = df.iat[-1,-3]
    Data_Adj = df.iat[-1,-2]
    
    content = (str(end) + "\n最高價：" + str (round(Data_High, 2)) + 
               "\n最低價：" + str (round(Data_Low, 2)) +
               "\n開盤價：" + str (round(Data_Open, 2)) + 
               "\n收盤價：" + str (round(Data_Close, 2)) +
               "\n調整收盤價：" + str (round(Data_Adj, 2)))
    
    df.index = df.index.format (formatter = lambda x: x.strftime ('%Y-%m-%d')) 
    
    '畫圖'
    fig = plt.figure(figsize=(6, 6))
    fig.suptitle(stock_number,  fontsize = 20, fontweight="bold")
    
    AX1 = fig.add_axes([0, 0.0, 1, 0.4])
    AX2 = fig.add_axes([0, 0.5, 1, 0.4])

    'K線圖'
    AX2.set_xticks (range (0, len(df.index),5))
    AX2.set_xticklabels(df.index[::5])
    mpf.candlestick2_ochl (AX2, df['Open'], df['Close'], df['High'], df['Low'], 
                           width = 1, colorup = 'r', colordown = 'g', alpha = 1)
    '成交量'
    mpf.volume_overlay(AX1, df.Open, df.Close, df.Volume, 
                       colorup = 'r', colordown = 'g', 
                       width = 1, alpha=0.9)
    AX1.set_xticks (range (0, len(df.index),5))
    AX1.set_xticklabels(df.index[::5])


    '圖片上傳至imgur'
    plt.savefig('send.png')
    CLIENT_ID = "fa7ce9e1978a941"
    PATH = "send.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    img_url = uploaded_image.link

  
    try:
        message = [
            TextSendMessage(  #傳送y文字
                text = content
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = img_url,
                preview_image_url = img_url
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

