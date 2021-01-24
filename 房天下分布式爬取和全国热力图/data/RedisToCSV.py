"""
讲redis中的数据导入csv文件中
"""
import csv
import redis
import re

def connect_to_redis():
    """
    新建一个redis连接
    """
    pool = redis.ConnectionPool(host="127.0.0.1",port=6379,db=0,password="123456")
    redis_cli = redis.Redis(connection_pool=pool)
    return redis_cli

def get_items(redis_cli):
    """
    从redis中pop出一个数据
    """
    item = eval(redis_cli.blpop("ftx:items")[1])
    if item is None:
        #判断redis中是否还有数据
        return 1
    price = item["price"]

    if "价格待定" in price and len(price) != 0:
        #把没有价格的数据删除
        return 2

    if "万" in price:
        #把没有单价的房子进行计算单价处理
        price = int(re.findall(r"\d+", price)[0]) * 10000
        print(item)
        area = item["area"]
        if area:
            #获取房屋面积
            try:
                area = re.findall(r"\d+",area)[0]
            except IndexError:
                area = str(re.findall(r"\d+",area))
        else:
            return 2
        price = int(price) // int(area)
    else:
        price = re.findall(r"\d+",price)#把元/平方去掉，只留下价格
    province = item["province"]
    city = item["city"]
    if price:
        if type(price) == list:
            price = "".join(price)
        data = (province,city,int(price)) #以元组的方式存入
    else:
        return 2
    return data

def save_to_csv(redis_cli):
    """
    数据存入csv文件中
    """
    data = get_items(redis_cli)
    if data != 2 and data != 1:
        with open("data.csv", "a", encoding="utf-8", newline="") as fp:#以添加的方式打开一个data.csv文件，如果没有会新建
            writer = csv.writer(fp)#新建writer
            writer.writerow(data)#存储
            print("存储成功!")

def main():
    csv_header = ("省份","城市","房价/平方")
    with open("data.csv", "a", encoding="utf-8", newline="") as fp:
        #给csv文件添加一个头
        writer = csv.writer(fp)
        writer.writerow(csv_header)
    redis_cli = connect_to_redis()
    while True:
        if get_items(redis_cli) == 1:
            break
        save_to_csv(redis_cli)

if __name__ == '__main__':
    main()