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
import requests, datetime, statistics, time
from lxml import etree

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



" AQI圖表 "
def AQI_char(event): 
    # 資料參考：https://airtw.epa.gov.tw/ModelSimulate/20220529/output_AQI_20220529150000.png
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
