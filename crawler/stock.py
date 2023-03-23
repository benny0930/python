import pandas as pd
import requests
import time
import json

def start(_number):
    # 打算要取得的股票代碼
    stock_list_tse = ['0050', '0056', '2330', '2317', '1216']
    stock_list_otc = ['6547', '6180']
    stock_list_tse = []
    stock_list_otc = []
    if(_number[0]=="6"):
        stock_list_otc = [_number]
    else:
        stock_list_tse = [_number]

    # 組合API需要的股票清單字串
    stock_list1 = '|'.join('tse_{}.tw'.format(stock) for stock in stock_list_tse)

    # 6字頭的股票參數不一樣
    stock_list2 = '|'.join('otc_{}.tw'.format(stock) for stock in stock_list_otc)

    if (_number[0] == "6"):
        stock_list = stock_list2
    else:
        stock_list = stock_list1

    print(stock_list)

    # 　組合完整的URL
    query_url = f'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}'
    print(query_url)
    # 呼叫股票資訊API
    response = requests.get(query_url)

    # 判斷該API呼叫是否成功
    if response.status_code != 200:
        raise Exception('取得股票資訊失敗.')
    else:
        print(response.text)

    # {"msgArray": [], "referer": "", "userDelay": 5000, "rtcode": "0000",
    #  "queryTime": {"sysDate": "20230323", "stockInfoItem": 1991, "stockInfo": 73685, "sessionStr": "UserSession",
    #                "sysTime": "17:31:38", "sho

    # {"msgArray": [], "referer": "", "userDelay": 5000, "rtcode": "0000",
    #  "queryTime": {"sysDate": "20230323", "stockInfoItem": 1991, "stockInfo": 73685, "sessionStr": "UserSession",
    #                "sysTime": "17:31:38", "sho
    #                    wChart":false,"sessionFromTime":-1,"sessionLatestTime":-1},"rtmessage":"OK"}


                   # 將回傳的JSON格式資料轉成Python的dictionary
    data = json.loads(response.text)
    print(data['msgArray'])
    # 過濾出有用到的欄位
    columns = ['c', 'n', 'z', 'tv', 'v', 'o', 'h', 'l', 'y', 'tlong']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號', '公司簡稱', '成交價', '成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價',
                  '資料更新時間']

    # 自行新增漲跌百分比欄位
    df.insert(9, "漲跌百分比", 0.0)

    # 用來計算漲跌百分比的函式
    def count_per(x):
        if isinstance(x[0], int) == False:
            x[0] = 0.0

        result = (x[0] - float(x[1])) / float(x[1]) * 100

        return pd.Series(['-' if x[0] == 0.0 else x[0], x[1], '-' if result == -100 else result])

    # 填入每支股票的漲跌百分比
    df[['成交價', '昨收價', '漲跌百分比']] = df[['成交價', '昨收價', '漲跌百分比']].apply(count_per, axis=1)

    # 紀錄更新時間
    def time2str(t):
        print(t)
        t = int(t) / 1000  # UTC時間加8小時為台灣時間

        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

    # 把API回傳的秒數時間轉成容易閱讀的格式
    df['資料更新時間'] = df['資料更新時間'].apply(time2str)

    # 顯示股票資訊
    return df