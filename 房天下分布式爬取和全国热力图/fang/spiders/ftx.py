# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem
import scrapy_redis.spiders

class FtxSpider(scrapy_redis.spiders.RedisSpider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    #start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:start_urls"#从redis_key中读取URL，不再从start_urls读取，插入数据的时候就插入到key中即可

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        #找目录页面中所有省份的tr标签
        province = None
        for tr in trs:
            #通过省份的tr再找里面td标签(哪些含有省份和城市的td标签)
            #空白的td标签可以通过它含有class来去除
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0] #省份的td
            province_text = province_td.xpath(".//text()").get()#省份
            province_text = re.sub(r"\s","",province_text)#有些城市有多行，在多行中身份是&nbsp;即空白字符
            if province_text:
                #如果有文本那就有省份，如果没有那就是多行省份
                province = province_text
            if province == "其它":
                #不爬取海外城市
                continue
            city_td = tds[1] #城市的td
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                #获取城市名和每个城市的URL
                city_name = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()

                #构建新房的URL
                url_module = city_url.split(".")
                scheme = url_module[0]# https://hz
                if "https" not in scheme:
                    scheme = scheme.replace("http","https")
                domain = url_module[1] + "." + url_module[2] #fang.com
                newhouse_url = scheme + "." + "newhouse." + domain + "house/s/"

                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city_name)})


    def parse_newhouse(self,response):
        province,city = response.meta.get("info")
        """
        获取新房的小区名称，居室，建筑面积，位置，出售状态，价格
        """
        lis = response.xpath("//div[@class='nl_con clearfix']/ul/li[contains(@id,'lp_')]")
        #获取新房页面每一个房子的li标签
        for li in lis:
            # 楼盘名字
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()

            # 获取到居室数
            house_type_list = li.xpath(".//div[@class='house_type clearfix']/a/text()").getall()
            house_type_list = list(map(lambda x:re.sub(r"\s","",x),house_type_list))#删除空白字符
            rooms = list(filter(lambda x:x.endswith("居"),house_type_list))#只留下以居结尾的数据，其他数据不要

            #建筑面积
            area = "".join(li.xpath(".//div[@class='house_type clearfix']/text()").getall())
            area = re.sub(r"\s|－|/","",area)

            #楼盘地址
            address = li.xpath(".//div[@class='address']/a/@title").get()

            #行政区
            district = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            district = re.search(r".*\[(.*)\].*",district).group(1)

            #是否在售
            sale = li.xpath(".//div[@class='fangyuan']/span/text()").get()

            #价格
            price = li.xpath(".//div[@class='nhouse_price']//text()").getall()
            price = "".join(price)
            price = re.sub(r"\s|广告","",price)

            #房子详情连接
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()

            item = NewHouseItem(name=name,rooms=rooms,area=area,address=address,district=district,sale=sale,price=price,origin_url=origin_url,province=province,city=city)
            yield item

        #下一页的链接
        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href")
        if next_url:
            yield scrapy.Request(url=response.urljoin(str(next_url)),callback=self.parse_newhouse,meta={"info":(province,city)})
            #进行下一页解析

