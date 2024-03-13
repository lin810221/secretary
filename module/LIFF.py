from django.conf import settings
from linebot import LineBotApi
from linebot.models import (TextSendMessage, MessageAction,
                            BubbleContainer, ImageComponent, BoxComponent, 
                            TextComponent, IconComponent, ButtonComponent, 
                            SeparatorComponent, FlexSendMessage, URIAction,
                            CarouselContainer, PostbackAction
                            )

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

" 練習 - LIFF "
def sendFlex(event):  #彈性配置
    try:
        bubble = BubbleContainer(
            direction='ltr',  #項目由左向右排列

            hero=ImageComponent(  #主圖片
                url='https://i.imgur.com/Pzt0EJ7.jpeg',
                size='full',
                aspect_ratio='792:550',  #長寬比例
                aspect_mode='cover',
            ),
            body=BoxComponent(  #主要內容
                layout='vertical',
                contents=[
                    TextComponent(text='COVID-19', size='md'),

                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='每天鎖定下午2點更新最新資訊', color='#aaaaaa', size='sm', flex=2)
                                ],
                            ),
                            SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="10:00 - 23:00", color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],
                    ),
                    BoxComponent(  
                        layout='vertical',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=PostbackAction(label='最新資訊', data = 'action=covid19'),
                            ),
                            ButtonComponent(
                                style='link',
                                height='sm',
                                action=PostbackAction(label='病例分佈', data = 'action=covid19-land')
                            ),
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                color = '#00CACA',
                                action=URIAction(label='資料來源', uri='https://covid-19.nchc.org.tw/')
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(  #底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@IanLin 2022', color='#888888', size='sm', align='center'),
                ]
            ),
        )

        stock = BubbleContainer(
            direction='ltr',  #項目由左向右排列

            hero=ImageComponent(  #主圖片
                url='https://i.imgur.com/AcKdYwc.jpg',
                size='full',
                aspect_ratio='792:550',  #長寬比例
                aspect_mode='cover',
            ),
            body=BoxComponent(  #主要內容
                layout='vertical',
                contents=[
                    TextComponent(text='股市指數資訊', size='md'),

                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='加權、電子、半導體、航運、鋼鐵指數，以及資訊走向', color='#aaaaaa', size='sm', flex=2)
                                ],
                            ),
                            #SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="10:00 - 23:00", color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],
                    ),
                    BoxComponent(  
                        layout='vertical',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                color = '#CE0000',
                                action=PostbackAction(label='加權指數', data='action=加權指數'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                color = '#5B5B5B',
                                action=PostbackAction(label = '各類指數', data='action=各類指數')
                            ),
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                color = '#938953',
                                action=PostbackAction(label = '資金走向', data='action=資金走向')
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(  #底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@IanLin 2022', color='#888888', size='sm', align='center'),
                ]
            ),
        )

        carousel_template = CarouselContainer(contents=[bubble, stock])
        message = FlexSendMessage(alt_text="彈性配置範例", contents=carousel_template)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



def contact(event):  #彈性配置
    try:
        bubble = BubbleContainer(
            direction='ltr',  #項目由左向右排列

            hero=ImageComponent(  #主圖片
                url='https://i.imgur.com/9PZ3ZlP.jpg',
                size='full',
                aspect_ratio='792:555',  #長寬比例
                aspect_mode='cover',
            ),
            body=BoxComponent(  #主要內容
                layout='vertical',
                contents=[
                    TextComponent(text='聯絡我', size='md'),
                    BoxComponent(
                        layout='baseline',  #水平排列
                        margin='md',
                        contents=[
                            IconComponent(size='lg', url='https://cdn-icons-png.flaticon.com/512/25/25231.png'),
                            TextComponent(text='25', size='sm', color='#999999', flex=0),
                            IconComponent(size='lg', url='https://i.imgur.com/sJPhtB3.png'),
                            TextComponent(text='14', size='sm', color='#999999', flex=0),
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    IconComponent(size='sm', url='https://i.imgur.com/sJPhtB3.png'),
                                    TextComponent(text='Email:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='lin810221@gmail.com', color='#666666', size='sm', flex=5)
                                ],
                            ),
                            SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="9:00 - 18:00", color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],
                    ),
                    BoxComponent(  
                        layout='horizontal',
                        margin='xs',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:0987654321'),
                            ),
                            ButtonComponent(
                                style='primary',
                                margin = 'xs',
                                height='sm',
                                color = '#00CACA',
                                action=MessageAction(label='E-mail', text='Hello')
                            ),
                        ]
                    ),
                    BoxComponent(  
                        layout='horizontal',
                        margin='xs',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='Github', uri="https://github.com/lin810221"),
                            ),
                            ButtonComponent(
                                style='secondary',
                                margin = 'xs',
                                height='sm',
                                color = '#00CACA',
                                action=URIAction(label='Linkedin', uri="https://www.linkedin.com/in/ian-lin-257b921aa/")
                            )
                        ]
                    ),
                ],
            ),
            footer=BoxComponent(  #底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright © 2021-2022 IanLin', color='#888888', size='sm', align='center'),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="彈性配置範例", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))





" 練習-網站 "
def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        text1 = '姓名：' + flist[0] + '\n'
        text1 += '日期：' + flist[1] + '\n'
        text1 += '包廂：' + flist[2]
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


