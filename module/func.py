from django.conf import settings
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
import requests, datetime, statistics, time, pyimgur
from lxml import etree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


" Covid-19 "
def Covid19(event): 
    " 輸入網址 "
    url = "https://covid-19.nchc.org.tw/"
    
    " 模擬瀏覽器 "
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"}
    
    " 取得網頁回應 "
    response = requests.get(url, verify=False)
    #time.sleep(7)
    
    " 讀取網頁程式碼 "
    html_str = response.content.decode()
    
    " 解析處理requests取得的數據 "
    html = etree.HTML(html_str)
    
    " 擷取網站標題 "
    Title = html.xpath("//h3/text()")
    
    " 擷取網站病情數據 "
    Data = html.xpath("//h1/text()")
    Data1 = html.xpath("//p/span/small/text()")
    
    " 確診、死亡、解除隔離、疫苗接種 "
    A = Data[0]   # 累積確診
    B = Data[1]   # 新增確診
    C = Data[2]   # 累計死亡
    D = Data[3]   # 疫苗接種
    E = Data1[1].split(" ")[1]  # 本土新增
    Dead = html.xpath("//p/span/text()")    # 新增死亡
    
    " 更新時間 "
    Updat_Time = html.xpath("//section[1]/div[1]/div/div/div/p/span[3]/text()")
    Updat_Time = Updat_Time[0].split()
    Updat_Time = ' '.join(Updat_Time)
    
    " 訊息總整理 "
    content = (Title[0] + 
       "\n本土新增：" + E +        
       "\n新增確診：" + B +
       "\n累計確診：" + A + 
       "\n新增死亡：" + Dead[4] +
       "\n累計死亡：" + C +  
       "\n疫苗接種：" + D + "\n" +
       Updat_Time
       )

    try:
        message = TextSendMessage(  
            text = content
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" Covid19 - 地區數據 "
def Covid19_land(event):
    " 輸入網址 "
    url = "https://covid-19.nchc.org.tw/"
    
    " 模擬瀏覽器 "
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"}
    
    " 取得網頁回應 "
    response = requests.get(url, verify=False)
    #time.sleep(7)
    
    " 讀取網頁程式碼 "
    html_str = response.content.decode()
    
    " 解析處理requests取得的數據 "
    html = etree.HTML(html_str)
    
    " 擷取網站標題 "
    Title = html.xpath("//h3/text()")
    
    " 更新時間 "
    Updat_Time = html.xpath("//section[1]/div[1]/div/div/div/p/span[3]/text()")
    Updat_Time = Updat_Time[0].split()
    Updat_Time = ' '.join(Updat_Time)
    
    " 地區資料處理 "
    land = html.xpath("//a/span[@style=\"font-size: 1em;\"]/text()")
    land_1 = html.xpath("//a//span[@style=\"font-size: 1.0em;\"]/text()")
    
    table = dict(zip(land, land_1))
    context = Title[1] + "\n"
    for i in range(len(land_1)):
        if land_1[i] != '\xa0':
            context += land[i].split(" ")[0] + ":" + land_1[i].split()[0] + "\n"
    context = (context + Updat_Time)   
    try:
        message = TextSendMessage(  
            text = context
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


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
        message = TextSendMessage(  
            text = content
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 天氣資訊 "
def Weathers(event): 
    content = ''
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-8A0972E4-E510-4619-8762-191D601E832D&downloadType=WEB&format=JSON'
    response = requests.get(url)
    data = response.json()
    location = data['cwbopendata']['dataset']['location']
    for i in location:
        city = i['locationName']    # 縣市名稱
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
        maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最低溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最高溫
        ci8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']    # 舒適度
        pop8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']   # 降雨機率
        content += f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %\n\n'


    try:
        message = TextSendMessage(  
            text = content
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 天氣雷達與溫度分布 "
def WeathersRadar(event): 
    "天氣雷達"
    radar_url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0058-003?Authorization=rdec-key-123-45678-011121314&format=JSON'
    radar = requests.get(radar_url)        # 爬取資料
    radar_json = radar.json()              # 使用 JSON 格式
    radar_img = radar_json['cwbopendata']['dataset']['resource']['uri']  # 取得圖片網址

    "溫度分布"
    timeString = time.strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
    t1 = time.strftime("%Y-%m-%d")
    t2 = time.strftime("%H")
    t = 'https://www.cwb.gov.tw/Data/temperature/' + t1 + '_' + t2 + '00.GTP8w.jpg'
    text = '溫度分布圖\n' + timeString

    try:
        message = [
            TextSendMessage(  #傳送文字
                '雷達合成回波圖\n' + timeString
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = radar_img,
                preview_image_url = radar_img
                ),
            TextSendMessage(  #傳送文字
                text
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = t,
                preview_image_url = t
                )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" AQI圖表 "
def AQI_char(event): 
    # 資料參考：https://airtw.epa.gov.tw/ModelSimulate/20220529/output_AQI_20220529150000.png
    time_stamp = time.time() # 設定timeStamp
    struct_time = time.localtime(time_stamp) # 轉成時間元組
    timeString = time.strftime("%Y-%m-%d %H:%M:%S") # 轉成字串
    t = time.strftime("%Y%m%d%H")
    t ='https://airtw.epa.gov.tw/ModelSimulate/' + t[:8] + '/output_AQI_' + t + '0000.png'
    text = '全國空氣品質指標\n' + timeString

    try:
        message = [
            TextSendMessage(  #傳送y文字
                text
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = t,
                preview_image_url = t
                )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 空氣品質指標 "
def AQI(event): 
    address = event.message.address
    city_list, site_list ={}, {}
    msg = '找不到空氣品質資訊。'

    url = 'https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json'
    a_data = requests.get(url)             # 使用 get 方法透過空氣品質指標 API 取得內容
    a_data_json = a_data.json()            # json 格式化訊息內容
    for i in a_data_json['records']:       # 依序取出 records 內容的每個項目
        city = i['County']                 # 取出縣市名稱
        if city not in city_list:
            city_list[city]=[]             # 以縣市名稱為 key，準備存入串列資料
        site = i['SiteName']               # 取出鄉鎮區域名稱
        if i['AQI'] == '':
            aqi = 0
        else:
            aqi = int(i['AQI'])                 # 取得 AQI 數值
        status = i['Status']               # 取得空氣品質狀態
        site_list[site] = {'aqi':aqi, 'status':status}  # 記錄鄉鎮區域空氣品質
        city_list[city].append(aqi)        # 將各個縣市裡的鄉鎮區域空氣 aqi 數值，以串列方式放入縣市名稱的變數裡


    for i in city_list:
        if i in address: # 如果地址裡包含縣市名稱的 key，就直接使用對應的內容
            # 參考 https://airtw.epa.gov.tw/cht/Information/Standard/AirQualityIndicator.aspx
            aqi_val = round(statistics.mean(city_list[i]),0)  # 計算平均數值，如果找不到鄉鎮區域，就使用縣市的平均值
            aqi_status = ''  # 手動判斷對應的空氣品質說明文字
            if aqi == 0: aqi_status = '資訊有誤'
            elif aqi_val<=50: aqi_status = '良好'
            elif aqi_val>50 and aqi_val<=100: aqi_status = '普通'
            elif aqi_val>100 and aqi_val<=150: aqi_status = '對敏感族群不健康'
            elif aqi_val>150 and aqi_val<=200: aqi_status = '對所有族群不健康'
            elif aqi_val>200 and aqi_val<=300: aqi_status = '非常不健康'
            else: aqi_status = '危害'
            msg = f'空氣品質{aqi_status} ( AQI {aqi_val} )。' # 定義回傳的訊息
            break
        
    for i in site_list:
        if i in address:  # 如果地址裡包含鄉鎮區域名稱的 key，就直接使用對應的內容
            msg = f'空氣品質{site_list[i]["status"]} ( AQI {site_list[i]["aqi"]} )。'
      
    try:
        message = TextSendMessage(  
            text = address + '\n' + msg
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 油價相關資訊 "
def Oil(event): 
    url = 'https://toolboxtw.com/zh-TW/detector/gasoline_price'
    response = requests.get(url, verify=False)
    html_str = response.content.decode()
    html = etree.HTML(html_str)

    title = html.xpath('//*[@id="content"]/div/div/div[2]/div[5]/table/thead/tr/th/text()')
    date = html.xpath('//table[@class="table table-bordered table-hover price_table"]/tbody/tr/th/text()')
    data = html.xpath('//table[@class="table table-bordered table-hover price_table"]/tbody/tr/td/text()')

    a = np.array(data)
    col = 4
    row = int(len(a) / col)
    data = a.reshape((row, col))

    for i in range(row):
        for j in range(col):
            data[i][j] = data[i][j].split('元')[0]
            
    plt.rcParams['font.sans-serif'] = 'SimHei'
    df = pd.DataFrame(data)
    df.index = date
    #df.columns = title[1:]
    df.columns = ['92 無鉛', '95 無鉛', '98 無鉛', '超級柴油']

    df = df.astype(float)

    df = df.sort_index(level=title[1], ascending=True)
    
    df.plot.line(linestyle = '--', grid = True)
    
    content = ('【最新調價日期】：' + str(df.index[0]) + 
               '\n  92無鉛：' + str(df.iloc[0, 0]) + 
               '\n  95無鉛：' + str(df.iloc[0, 1]) + 
               '\n  98無鉛：' + str(df.iloc[0, 2]) + 
               '\n  超級柴油：' + str(df.iloc[0, 3]))
    
    '圖片上傳至imgur'
    plt.savefig('send-1.png')
    CLIENT_ID = "fa7ce9e1978a941"
    PATH = "send-1.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    img_url_1 = uploaded_image.link
    
    df.plot.line(subplots=True)
    #plt.plot(df[list(df)[0]])
    
    '圖片上傳至imgur'
    plt.savefig('send-2.png')
    CLIENT_ID = "fa7ce9e1978a941"
    PATH = "send-2.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    img_url_2 = uploaded_image.link

    try:
        message = [
            TextSendMessage(  #傳送文字
                text = content
            ),            
            TextSendMessage(  #傳送文字
                text = '中油油價歷史資訊'
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = img_url_1,
                preview_image_url = img_url_1
            ),
            ImageSendMessage(  #傳送圖片
                original_content_url = img_url_2,
                preview_image_url = img_url_2
            )
        ]
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
                    CarouselColumn(  # Covid-19
                        thumbnail_image_url='https://i.imgur.com/Pzt0EJ7.jpeg',
                        title = 'COVID-19',
                        text = '每天鎖定下午2點更新最新資訊',
                        actions = [
                            PostbackTemplateAction(
                                label = '最新資訊',
                                data = 'action=covid19'
                            ),
                            PostbackTemplateAction(
                                label = '病例分佈',
                                data = 'action=covid19-land'
                            ),
                            URITemplateAction(
                                label = '資料來源',
                                uri='https://covid-19.nchc.org.tw/'
                            )
                        ]
                    ),
                    CarouselColumn(  # 指數、資金
                        thumbnail_image_url = 'https://i.imgur.com/AcKdYwc.jpg',
                        title = '股市指數資訊',
                        text = '加權、電子、半導體、航運、鋼鐵指數，以及資訊走向',
                        actions = [
                            PostbackTemplateAction(
                                label = '加權指數',
                                data='action=加權指數'
                            ),
                            PostbackTemplateAction(
                                label='各類指數',
                                data='action=各類指數'
                            ),
                            PostbackTemplateAction(
                                label = '資金走向',
                                data='action=資金走向'
                            ),
                        ]
                    ),
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
                                label = '未開發',
                                data='action=NA'
                            ),
                            PostbackTemplateAction(
                                label = '未開發',
                                data='action=NA'
                            ),
                        ]
                    ),
                    CarouselColumn(  # 天氣資訊
                        thumbnail_image_url = 'https://www.crazybackground.com/wp-content/uploads/2019/12/vector-chinese-clouds.jpg',
                        title = '天氣資訊',
                        text = 'Temperature and Humidity',
                        actions = [
                            PostbackTemplateAction(
                                label = '天氣預報',
                                data='action=天氣預報'
                            ),
                            PostbackTemplateAction(
                                label='天氣雷達與溫度分布',
                                data='action=天氣雷達與溫度分布'
                            ),
                            PostbackTemplateAction(
                                label = '空氣品質指標',
                                data='action=空氣品質指標'
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
                    CarouselColumn(  # 聯合新聞網
                        thumbnail_image_url = 'https://udn.com/static/img/logo.svg?2020020601.jpg',
                        title = '聯合新聞網',
                        text = '讓你不漏掉任何資訊',
                        actions = [
                            URITemplateAction(
                                label = '新聞網站',
                                uri='https://udn.com/news/index'
                            ),
                            PostbackTemplateAction(
                                label='及時新聞',
                                data='action=及時新聞'
                            ),
                            PostbackTemplateAction(
                                label = '熱門新聞',
                                data='action=熱門新聞'
                            ),
                        ]
                    ),
 
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 聯合新聞網 "
def udn_news(event, x):
    url = "https://udn.com/news/index"
    response = requests.get(url)
    
    html_str = response.content.decode()
    html = etree.HTML(html_str)
    
    # 及時新聞
    Con1 = html.xpath("//div[1]/div/a/span[2]/text()")
    Web1 = html.xpath("//div[7]/div[1]/div/a/@href")
    # 熱門新聞
    Con2 = html.xpath("//div[2]/div/a/span[2]/text()")
    Web2 = html.xpath("//section[3]/div[7]/div[2]/div/a/@href")
    
    if x == 0:        
        content = ""
        for i in range(len(Con1)):
            content += Con1[i] + "\n"
            content += Web1[i] + "\n" 
    else:
        content = ""
        for i in range(len(Con1)):
            content += Con2[i] + "\n"
            content += Web2[i] + "\n" 

    try:
        message = TextSendMessage(  
            text = content
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

" 查詢股票指令教學 (目前無使用) "
def sendBack_StockText (event, backdata):  #處理Postback
    try:
        text1 = '查詢股市 = 股市 XXXX.YY'
        text1 += '\nXXXX為股市代碼'
        text1 += '\nYY為分類 (上市、上櫃)'
        text1 += '\n上市為TW'
        text1 += '\n上櫃為TWO'
        text1 += '\n例如：股市 2330.TW'
        text1 += '\n\n另外指數通常為 <^代號>'
        text1 += '\n例如道瓊指：股市 ^DJI'        
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

" 練習 - 圖片轉盤 "
def sendImgCarousel(event):  #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/YhJKwZh.jpeg',
                        action=URITemplateAction(
                            label='工具和計算器',
                            uri='https://miniwebtool.com/zh-tw/'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/CUG0Aof.jpeg',
                        action=PostbackTemplateAction(
                            label='購買餐點',
                            data='action=buy'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


" 練習 - 圖片地圖"
def sendImgmap(event):  #圖片地圖
    try:
        image_url = 'https://i.imgur.com/Yz2yzve.jpg'  #圖片位址
        imgwidth = 1040  #原始圖片寛度一定要1040
        imgheight = 300
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text="圖片地圖範例",
            base_size=BaseSize(height=imgheight, width=imgwidth),  #圖片寬及高
            actions=[
                MessageImagemapAction(  #顯示文字訊息
                    text='你點選了紅色區塊！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=0, 
                        y=0, 
                        width=imgwidth*0.25, 
                        height=imgheight  
                    )
                ),
                URIImagemapAction(  #開啟網頁
                    link_uri='https://imgur.com/gallery/CnJ0r',
                    area=ImagemapArea(  #右方1/4區域(藍色1)
                        x=imgwidth*0.75, 
                        y=0, 
                        width=imgwidth*0.25, 
                        height=imgheight  
                    )
                ),
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 練習 - 日期時間"
def sendDatetime(event):  #日期時間
    try:
        message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",  #觸發postback事件
                        mode="date",  #選取日期
                        initial="2019-06-01",  #顯示初始日期
                        min="2019-01-01",  #最小日期
                        max="2020-12-31"  #最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell&mode=time",
                        mode="time",  #選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell&mode=datetime",
                        mode="datetime",  #選取日期時間
                        initial="2019-06-01T10:00",
                        min="2019-01-01T00:00",
                        max="2020-12-31T23:59"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

" 練習 - 日期時間觸發 "
def sendData_sell(event, backdata):  #Postback,顯示日期時間
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')  #讀取日期
        elif backdata.get('mode') == 'time':
            dt = '時間為：' + event.postback.params.get('time')  #讀取時間
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')  #讀取日期時間
            dt = dt.strftime('{d}%Y-%m-%d, {t}%H:%M').format(d='日期為：', t='時間為：')  #轉為字串
        message = TextSendMessage(
            text=dt
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
