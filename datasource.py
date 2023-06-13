import requests

stationID = {
    '南港':'0990',
    '台北':'1000',
    '板橋':'1010',
    '桃園':'1020',
    '新竹':'1030',
    '苗栗':'1035',
    '台中':'1040',
    '彰化':'1043',
    '雲林':'1047',
    '嘉義':'1050',
    '台南':'1060',
    '左營':'1070'
}

def getInfo(start,end,date):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    url = f'https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/OD/{stationID[start]}/to/{stationID[end]}/{date}?%24format=JSON'
    response = requests.get(url,headers=header)
    data_list = response.json()
    data_list_temp = list()
    for item in data_list:
        data_list_temp.append(item)
    return data_list_temp

def priceInfo(start,end):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    url = f'https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare/{stationID[start]}/to/{stationID[end]}?%24format=JSON'
    response = requests.get(url,headers=header)
    data_list = response.json()
    price_list_temp = list()
    for item in data_list:
        for item1 in item['Fares']:
            price_list_temp.append(item1['Price'])
    return price_list_temp