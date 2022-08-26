# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import redis
from scrapy.exceptions import DropItem

class RedisPipeline:
    def open_spider(self,spider):
        self.r = redis.Redis(
            host='192.168.255.71',
            port=6379
        )

    def close_spider(self, conn):
        self.r.close()

    def process_item(self, item, spider):
        if self.r.sadd(spider.name,item['name']):
            return item
        raise DropItem

class QianmuPipeline:
    def open_spider(self,spider):
        self.conn = pymysql.connect(
            host='192.168.255.71',
            port=3306,
            db='qianmu_gp01',
            user='root',
            password='root',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def close_spider(self,conn):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        print(self.cur.connection.connect())
        keys,values = zip(*item.items())
        # print(keys,values)
        sql = 'insert into un ({}) values({})'.format(",".join(['`{}`'.format(k) for k in keys]),','.join(['"{}"'.format(k) for k in values]))
        sql = sql.replace('""','"')
        print(sql)
        self.cur.execute('select version()')
        data = self.cur.fetchone()
        print(data)
        if self.cur.execute(sql):
            print("执行成功")
        else:
            print("执行失败")
        self.conn.commit()
        return item
