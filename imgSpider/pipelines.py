import scrapy
from scrapy.pipelines.images import ImagesPipeline
from imgSpider import settings

import os


class ImgspiderPipeline(ImagesPipeline):
    #对某一个媒体资源进行请求发送
    #item就是接收到的spider提交过来的item
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['url'], meta={'item':item})
 
    #制定媒体数据存储的名称
    def file_path(self, request, response=None, info=None):
        # 文件夹名称
        item = request.meta['item']

        temp_path = os.path.join(settings.IMAGES_STORE, item['title'])
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        name = item['url'].split('/')[-1]
        print('正在下载：',name)
        return f'{item["title"]}/{name}'
 
    #将item传递给下一个即将给执行的管道类
    def item_completed(self, results, item, info):
        return item
