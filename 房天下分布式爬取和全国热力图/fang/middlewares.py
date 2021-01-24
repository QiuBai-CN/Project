# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import requests
from scrapy import signals
from fake_useragent import UserAgent
from model.models import ProxyModel
from twisted.internet.defer import DeferredLock

class FangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class FangDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class UserAgentAndIPProxyMiddleware(object):
    """
    配置随机请求头和IP代理
    """
    PROXY_URL = "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="

    def __init__(self):
        super(UserAgentAndIPProxyMiddleware,self).__init__()
        self.ua = UserAgent()
        self.current_proxy = ProxyModel(dict({"ip":"120.43.134.119","port":4242,"expire_time":"2020-09-11 13:04:26"}))
        self.lock = DeferredLock()
        #当前的代理

    def get_proxy(self):
        self.lock.acquire()
        #由于scrapy框架下的twisted是异步执行，会导致几乎同时有很多运行这个函数多次，使用锁机制，不会多次无意义请求代理
        if self.current_proxy is None or self.current_proxy.is_expiring:
            resp = requests.get(self.PROXY_URL).text
            result = json.loads(resp)
            if len(result["data"]) > 0:
                data = result["data"][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
        self.lock.release()

    def process_request(self,request,spider):
        request.headers["User-Agent"] = self.ua.random
        if  "proxy" not in request.meta or self.current_proxy.is_expiring:
            #如果请求的meta里面没有传递proxy，就给一个代理IP
            self.get_proxy()
            request.meta['proxy'] = self.current_proxy.proxy
        print(self.current_proxy.ip)

    def process_response(self,request,response,spider):
        if response.status != 200 or "captcha-verify" in response.url:
            self.get_proxy()
            return request
        #如果返回的状态不是200或者返回的URL里面带有了captcha-verify，说明代理不可用，更换代理并且重新返回这个请求进行重新请求
        return response
        #如果正常就要返回response，不返回就不会传到爬虫





