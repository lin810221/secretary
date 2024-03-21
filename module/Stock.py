from django.conf import settings

from linebot import LineBotApi
from linebot.models import (TextSendMessage, ImageSendMessage, StickerSendMessage,
                            LocationSendMessage, QuickReply, QuickReplyButton, 
                            MessageAction)
from io import BytesIO
import base64
import pandas as pd

import matplotlib.pyplot as plt
import requests
import pyimgur
import json
from lxml import etree
import numpy as np

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

" 爬蟲 - 加權指數 "
def sendMulti(event, backdata):
    df = pd.DataFrame()
    url = "https://www.twse.com.tw/exchangeReport/MI_5MINS_INDEX?response=json&date=&_=" 
    res = requests.get(url)
    stock_json = res.json()
    Title = stock_json['title']
    stock_df = pd.DataFrame.from_dict(stock_json['data'])
    df = pd.concat([df, stock_df], ignore_index=True)
    df.columns = stock_json['fields']
    
    ind = ['發行量加權股價指數',
           '紡織纖維類指數',
           '生技醫療類指數',
           '造紙類指數',
           '鋼鐵類指數',
           '電子類指數',
           '半導體類指數',
           '航運類指數'
           ]
    
    option = 0
        
    stock_daily = df[['時間', ind[option]]]
    for row in range(stock_daily.shape[0]):
        stock_daily.iloc[row, 1] = float(stock_daily.iloc[row, 1].replace(',', ''))
    
    fig = plt.figure(figsize = (10, 10))
    plt.plot(stock_daily[ind[option]], 'r')
    plt.title(stock_json['date'] + "  " + "POW00")
    
    # 保存圖片到 BytesIO 對象中
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # 將 BytesIO 對象轉換為 base64 編碼
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # 圖片上傳至imgur
    CLIENT_ID = "fa7ce9e1978a941"
    im = pyimgur.Imgur(CLIENT_ID)
    
    # 上傳圖片到 Imgur
    CLIENT_ID = "fa7ce9e1978a941"
    headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
    data = {'image': image_base64}
    response = requests.post('https://api.imgur.com/3/image', headers=headers, data=data)
    
    # 打印上傳的圖片連結
    if response.status_code == 200:
        img_url = response.json()['data']['link']
        print("圖片已上傳至 Imgur:", img_url)
    else:
        print("圖片上傳失敗:", response.text)
    
    try:
        message = [
            TextSendMessage(  #傳送y文字
                text = '看屁看'
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = img_url,
                preview_image_url = img_url
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 爬蟲 - 電子、半導體、航運、剛鐵指數 "
def sendMulti_1(event, backdata):
    df = pd.DataFrame()
    url = "https://www.twse.com.tw/exchangeReport/MI_5MINS_INDEX?response=json&date=&_=" 
    res = requests.get(url)
    stock_json = res.json()
    Title = stock_json['title']
    stock_df = pd.DataFrame.from_dict(stock_json['data'])
    
    df = df.append(stock_df, ignore_index=True)
    df.columns = stock_json['fields']    
    ind = ['電子類指數',
           '半導體類指數',
           '航運類指數',
           '鋼鐵類指數'
           ]
    
    option = 0
    f, AX = plt.subplots(2,2, sharex='col')
         
    for option in range(0, len(ind)):
        stock_daily = df[['時間', ind[option]]]    
        for row in range(stock_daily.shape[0]):
            stock_daily.iloc[row, 1] = float(stock_daily.iloc[row, 1].replace(',', ''))
    
        if option == 0:
            AX[0,0].plot(stock_daily[ind[option]], 'r')
            AX[0,0].set_title("Electronics")
        
        elif option == 1:
            AX[0,1].plot(stock_daily[ind[option]], 'g')
            AX[0,1].set_title("Semiconductor")            
    
            
        elif option == 2:
            AX[1,0].plot(stock_daily[ind[option]], 'b')
            AX[1,0].set_title("Shipping") 
        
        elif option == 3:
            AX[1,1].plot(stock_daily[ind[option]], 'y')
            AX[1,1].set_title("Steel")


    
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
                text = "各類指數"
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = img_url,
                preview_image_url = img_url
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


" 爬蟲 - 資金比重 "
def sendMulti_2(event, backdata):
    url = "https://ww2.money-link.com.tw/TWStock/TWStockMarket.aspx?mainOptionType=2&optionType=2" 
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"}
    response = requests.get(url, headers = headers, verify=False)
    html_str = response.content.decode()
    html = etree.HTML(html_str)
    
    " 標題 "
    a = html.xpath("//th[@id=\"HEAD1\"]/text()")
    b = html.xpath("//th[@id=\"HEAD1\"]/span/text()")
    Title = a[0]+b[1]+a[1]
    " 產業 "
    Com = html.xpath("//tr/td[@id=\"acenter\"]/text()")
    Pro = html.xpath("//tr/td[@id=\"aright\"]/text()")
    Pro = list(np.float_(Pro))
    dic = dict(zip(Com, Pro))
    df = pd.DataFrame(list(dic.items()), columns = ["Com", "Pro"])
    df = df.sort_values(by=['Pro'], ascending = False)
    content = Title + " \n【前6名】：\n"
    content += "\n" + df.iloc[0, 0] + "\t" + str (df.iloc[0, 1]) + " %"
    content += "\n" + df.iloc[1, 0] + "\t" + str (df.iloc[1, 1]) + " %"
    content += "\n" + df.iloc[2, 0] + "\t" + str (df.iloc[2, 1]) + " %"
    content += "\n" + df.iloc[3, 0] + "\t" + str (df.iloc[3, 1]) + " %"
    content += "\n" + df.iloc[4, 0] + "\t" + str (df.iloc[4, 1]) + " %"
    content += "\n" + df.iloc[5, 0] + "\t" + str (df.iloc[5, 1]) + " %"
    try:
        message = [
            TextSendMessage(  #傳送y文字
                text = content
            ),
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
