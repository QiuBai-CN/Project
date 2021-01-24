import time

from selenium.webdriver import Chrome,ChromeOptions
import re,pymysql

conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            port=3306,
            db="yq"
        )
cursor = conn.cursor()
sql = "insert into hotsearch(dt, content) values (%s,%s)"

option = ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no-sandbox")
driver = Chrome(executable_path="E:\chromedriver\chromedriver.exe",options=option)
driver.get("https://s.weibo.com/weibo?q=%23%E5%9B%BD%E9%99%85%E7%96%AB%E6%83%85%E5%8A%A8%E6%80%81%23")
texts = driver.find_elements_by_xpath("//div[@class='card-wrap']//div[@class='card']")
for text in texts:
    try:
        hot_search = text.find_element_by_xpath(".//p[@class='txt'][1]").text
        hot_search = re.search(r'【(.*?)】', hot_search).group(1)
        hot_search = re.sub(r'[#、\\，,]+', '', hot_search)
        good_num = text.find_element_by_xpath(".//div[@class='card-act']//em").text
        good_num = good_num if good_num else "0"
        hot_search = hot_search + "," + good_num
    except:
        break
    dt = time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
    cursor.execute(sql,(dt, hot_search))
    conn.commit()


