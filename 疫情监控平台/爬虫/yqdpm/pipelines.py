from itemadapter import ItemAdapter
import pymysql
from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PORT, MYSQL_PW, MYSQL_DB
from yqdpm.items import DayListItem,CityInfoItem


class YqdpmPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PW,
            port=MYSQL_PORT,
            db=MYSQL_DB
        )
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        if isinstance(item, DayListItem):
            sql = "insert into history(ds,confirm,confirm_add,suspect,suspect_add,heal,heal_add,dead,dead_add) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(item['date'],item['confirm'],item['confirm_add'],item['suspect'],item['suspect_add'],item['heal'],item['heal_add'],item['dead'],item['dead_add'],))
            self.conn.commit()
        else:
            sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,(item['update_time'],item['province_name'],item['city_name'],item['confirm'],item['confirm_add'],item['heal'],item['dead']))
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


