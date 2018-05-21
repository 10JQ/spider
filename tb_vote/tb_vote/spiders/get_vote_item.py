import scrapy

class QuotesSpider(scrapy.Spider):
    name = "vote_item"

    def start_requests(self):
        urls = [
            'https://s.taobao.com/search?q=%E6%8A%95%E7%A5%A8&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # 保存整个网页
    # 执行: scrapy crawl 爬虫名
    '''
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    '''

    # 提取数据
    # 执行: scrapy crawl 爬虫名 -o 爬虫名.json
    #'''
    def parse(self, response):
        for item in response.css('a'):
            text = item.css('::text').extract_first()
            print(text)
    #'''