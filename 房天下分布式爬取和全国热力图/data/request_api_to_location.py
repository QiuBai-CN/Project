import pandas
import requests
import re

def read_city_col():
    data = pandas.read_csv("ave_price.csv", header=0)
    return data

def req_api():
    datas = read_city_col()
    for index,city in datas.iterrows():
        city_name = city[0]#获取数据中的城市
        ave_price = city[1]
        if city_name == "博尔塔拉":
            city_name = city_name + "蒙古自治州"
        url = "http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak=dxMIgBbRWHGVuWaTby88fYRQx9k4ANMx&callback=showLocation".format(city_name)
        resp = requests.get(url).text

        #通过百度API返回城市的经纬度
        lng = re.findall(r'"lng":(\d+\.\d+)',resp)[0]
        #获取城市经度
        lat = re.findall(r'"lat":(\d+\.\d+)',resp)[0]
        #获取城市纬度
        data_format = {
            "lng":lng,
            "lat":lat,
            "count":ave_price
        }
        data_format = str(data_format) + ","
        print(data_format)


def main():
    req_api()

if __name__ == '__main__':
    main()