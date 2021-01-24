import time

import scrapy
import json
from ..items import DayListItem, CityInfoItem

class YqSpider(scrapy.Spider):
    name = 'yq'
    allowed_domains = ['qq.com']
    start_urls = ['https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list'] #?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare

    params = ["chinaDayAddList", "areaTree"]

    post_data = {
        "modules": ""
    }

    def start_requests(self):
        for param in self.params:
            self.post_data["modules"] = param
            request = scrapy.FormRequest(url=self.start_urls[0], formdata=self.post_data, callback=self.parse)
            request.meta['sign'] = param
            yield request

    def parse(self, response):
        # chinaDayList和chinaDayAddList日期对应对应
        sign = response.meta['sign']
        if sign is "chinaDayAddList":
            # 全中国每天汇总数据
            datas = json.loads(response.text)['data']['chinaDayAddList']
            for data in datas:
                item = DayListItem()
                item['date'] = data['y'] + '.' + data['date']
                item['confirm_add'] = data['confirm'] # 确诊人数
                item['suspect_add'] = data['suspect'] # 疑似人数
                item['dead_add'] = data['dead'] # 死亡人数
                item['heal_add'] = data['heal'] # 痊愈人数
                self.post_data['modules'] = 'chinaDayList'
                request = scrapy.FormRequest(url=self.start_urls[0], formdata=self.post_data, callback=self.parse_total,dont_filter=True)
                request.meta['data'] = item
                yield request
            pass
        elif sign is "areaTree":
            datas = json.loads(response.text)['data']['areaTree'][0]

            country_name = datas['name']
            history_total_data = datas['total'] # 总数据
            provinces_datas = datas['children']
            update_time = time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
            for data in provinces_datas:
                # 每个省的数据（含有今日数据，总数据，各市数据）
                province_name = data['name']
                for city_info in data['children']:
                    item = CityInfoItem()
                    item['update_time'] = update_time
                    item['province_name'] = province_name
                    item['city_name'] = city_info['name'] if city_info['name'] != '地区待确认' else province_name
                    item['confirm'] = city_info['total']['confirm']
                    item['confirm_add'] = city_info['today']['confirm']
                    item['heal'] = city_info['total']['heal']
                    item['dead'] = city_info['total']['dead']
                    yield item

    def parse_total(self,response):
        item = response.meta['data']
        print(item)
        datas = json.loads(response.text)['data']['chinaDayList']
        for data in datas:
            text_date = data['y'] + '.' + data['date']
            if text_date == item['date']:
                date = text_date  # 日期
                tup = time.strptime(date, '%Y.%m.%d')
                ds = time.strftime('%Y-%m-%d', tup)
                item['date'] = ds
                item['confirm'] = data['confirm']  # 确诊人数
                item['suspect'] = data['suspect']  # 疑似人数
                item['dead'] = data['dead']  # 死亡人数
                item['heal'] = data['heal']  # 痊愈人数
                yield item








