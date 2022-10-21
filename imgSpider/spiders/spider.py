import scrapy
from ..items import downImgItem
import re

class spider(scrapy.Spider):
    # 爬虫名称
    name = "spider"
    # 爬虫的网页地址
    start_urls = ['https://m.syt5.com/mnmm/index.html']

    def parse(self, response):
        # 解析返回的数据
        aList = response.xpath('//div[@class="img"]/a')
        for a in aList:
            url = a.xpath('@href').extract_first()
            title = a.xpath('img/@alt').extract_first()
            item = downImgItem()
            item['title'] = title
            yield scrapy.Request(url, self.downImg, meta={'item': item})

        # 获取下一页地址
        next_page = response.xpath('//a[@class="a1 nextlist"]/@href').extract_first()
        if next_page:
            yield scrapy.Request("https://m.syt5.com" + next_page)


    def downImg(self, response):
        item = response.meta.get('item')

        scripts = response.xpath('//script/text()').extract()
        script = scripts[len(scripts) -1]
        el = re.compile(r"picshowArr=.*]")
        imgList = el.findall(script)[0].replace("picshowArr=[", "").replace("\"", "").replace("]", "").split(",")
        for imgUrl in imgList:
            if not imgUrl:
                continue
            item['url'] = imgUrl
            # print(item)
            yield downImgItem(item)

