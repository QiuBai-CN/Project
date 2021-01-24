from datetime import datetime,timedelta
# def get_proxy_ip(ip_list):
#     """
#     请求代理IP，times是请求个数
#     """
#     proxy_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="
#     resp = requests.get(proxy_url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}).text
#     result = json.loads(resp)
#     #json数据load成字典
#     ip_datas = result["data"]
#     #拿到获取的所有IP信息
#
#     for ip_data in ip_datas:
#         """
#         遍历所有IP信息
#         """
#         ip = ip_data["ip"]
#         #IP
#         port = ip_data["port"]
#         #端口
#         ex_time = ip_data["expire_time"]
#         #过期时间
#         ip_list.append("{}:{},{}".format(ip,port,ex_time))
#         #添加进IP池
#     return ip_list
#
# def comfire_ip(ip_list):
#     random_ip,ex_time = random.choice(ip_list).split(",")
#     #随机选取IP信息
#     ex_time = datetime.strptime(ex_time, "%Y-%m-%d %H:%M:%S")
#     #将过期时间str格式转换成datetime格式
#     now = datetime.now()
#     #获取当前时间
#     if now > ex_time:
#         #如果IP过期，从IP池中删除并重新获取新的一个，否则直接返回这个IP
#         get_proxy_ip(ip_list)
#         ip_list.remove("{},{}".format(random_ip,ex_time))
#         random_ip = comfire_ip(ip_list)
#     return random_ip
class ProxyModel(object):
    def __init__(self,data):
        self.ip = data["ip"]
        #IP
        self.port = data["port"]
        #端口
        self.ex_time = data["expire_time"]
        #过期时间
        self.proxy = "https://{}:{}".format(self.ip,self.port)
        #代理IP

        date_str,time_str = self.ex_time.split(" ")
        year,month,day = date_str.split("-")
        hour,minute,second = time_str.split(":")
        self.expire_time = datetime(year=int(year),month=int(month),day=int(day),hour=int(hour),minute=int(minute),second=int(second))
        #构建datetime类型的过期时间数据，可以使用datetime里的方法，但是方法效率不高

    @property
    def is_expiring(self):
        #判断代理ip是否即将过期
        now = datetime.now()
        if (self.expire_time - now) < timedelta(seconds=5):
            #过期前5秒进行更换代理
            return True
        else:
            return False

