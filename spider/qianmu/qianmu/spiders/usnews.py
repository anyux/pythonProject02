import scrapy

from qianmu.items import UniversityItem


class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    allowed_domains = ['www.qianmu.org']
    start_urls = ['http://www.qianmu.org/ranking/1528.htm']

    def parse(self, response, **kwargs):
        links = response.xpath('//div[@class="rankItem"]//td[2]/a/@href').extract()
        for link in links:
            if not link.startswith('http://www.qianmu.org/'):
                link = f"http://qianmu.org/{link}"
            yield response.follow(link, self.parse_univerity)

    def parse_univerity(self, response):
        """处理大学详情页面"""
        response = response.replace(body=response.text.replace('\t','').replace('\r\n',''))
        item = UniversityItem()
        data = dict()
        item['name'] = response.xpath('//div[@id="wikiContent"]/h1/text()')[0].extract()
        table = response.xpath('//div[@class="infobox"]/table')
        print(data)
        if table:
            table = table[0]
            keys = table.xpath('.//td[1]/p/text()').extract()
            cols = table.xpath('.//td[2]')
            values = [''.join(col.xpath('.//text()').extract_first()) for col in cols]
            if len(keys) == len(values):
                data.update(zip(keys, values))
        item['myrank'] = data.get('排名')
        item['country'] = data.get('国家')
        item['city'] = data.get('城市')
        item['state'] = data.get('州省')
        item['undergraduate_num'] = data.get('本科生人数')
        item['postgraduate_num'] = data.get('研究生人数')
        item['website'] = data.get('网址')
        yield item
