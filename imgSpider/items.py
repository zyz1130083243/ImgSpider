import scrapy

class downImgItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field() # 图片链接
