import pandas

def read_csv():
    """
    读取csv中的数据，加载成DataFrame数据
    """
    data = pandas.read_csv("data.csv", encoding="utf-8")
    return data

def cal_price():
    """
    对数据通过城市进行分组并计算平均房价
    """
    data = read_csv()
    grouped_data = data.groupby("城市")["房价/平方"].mean().round(2)
    #通过城市进行分组，计算房价的平均值并保留2位小数
    return grouped_data

def store_csv():
    data = cal_price()
    data.to_csv("ave_price.csv")
    print("存储完成！")

def main():
    store_csv()

if __name__ == '__main__':
    main()