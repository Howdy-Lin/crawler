# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:31:32 2024

@author: h6173
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:45:21 2024

@author: h6173
"""
import requests
import schedule
import time
import pandas as pd
import openpyxl
from datetime import datetime

# 已發送過的地震資訊時間列表
sent_times = []


def send_notification(msg, img):
    token = 'LINE Notify 權杖'
    headers = {
        'Authorization': 'Bearer ' + 'vWR32WsePFhq1X0qzVsBsJHRnwjNg7lD51h0IvHaGR9'
    }
    data = {
        'message': msg,
        'imageThumbnail': img,
        'imageFullsize': img
        # 'message':'測試一下！'     # 設定要發送的LINE文字訊息

    }
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)
    print(response.text)


def crawl_earthquake_info():
    # 取得中央氣象局會員API授權碼:CWA-EC693080-AFF8-4B5C-94F5-44DE876C0F80
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWA-EC693080-AFF8-4B5C-94F5-44DE876C0F80'  # 地震資訊JSON網址
    # 發送GET請求
    response = requests.get(url)
    # 獲取JSON數據
    data_json = response.json()
    # 轉換成json格式
    earthquake = data_json['records']['Earthquake']
    # 獲取今日日期
    today = datetime.now().date()

    return earthquake, today

earthquake,today = crawl_earthquake_info()
#已發送過的地震資訊時間列表
df = pd.read_excel('sent_times.xlsx')
sent_times = df['sent_times']
sent_times = list(sent_times)

for i in earthquake:
    loc = i['EarthquakeInfo']['Epicenter']['Location']
    val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']
    dep = i['EarthquakeInfo']['FocalDepth']#['value']
    eq_time = datetime.strptime(i['EarthquakeInfo']['OriginTime'], "%Y-%m-%d %H:%M:%S")
    img = i['ReportImageURI']
    #print(eq_time)
    #print("eq_time.date() :",eq_time )
    #如果地震是今天發生, 並且該資訊尚未發送過且地震規模大於3.5, 則發送通知
    if eq_time.date() == today  and eq_time not in sent_times and val > 3:
        print(eq_time)
        msg = f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}'
        print(msg)
        send_notification(msg, img)
        #將以發送的地震資訊紀錄到 sent_times
        sent_times.append(eq_time)

# 將 sent_times 轉換為 DataFrame
df = pd.DataFrame(sent_times, columns=['sent_times'])

# 保存 DataFrame 為 xlsx 文件
df.to_excel('sent_times.xlsx', index=False)
#sent_times