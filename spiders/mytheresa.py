import scrapy

class MytheresaSpider(scrapy.Spider):
    name='mytheresa'
    start_urls=['https://www.mytheresa.com/int_en/men/shoes.html']
    
    def parse(self,response):
        for link in response.xpath('//a[contains(@class,"product-image")]/@href'):
            yield response.follow(link.get(),callback=self.parse_item)
            
        next_page=response.xpath('//li[contains(@class,"next")]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
    def parse_item(self,response):
            yield{
                
                'breadcrumbs':response.xpath('//div[contains(@class,"breadcrumbs")]/ul/li/a/span/text()').getall(),
                'img_url':response.css('img.gallery-image').xpath('@src').get(),
                'brand':response.xpath('//div[contains(@class,"product-designer")]/span/a/text()').get(),
                'product_name':response.xpath('//div[contains(@class,"product-name")]/span/text()').get(),
                'price':response.xpath('//div[contains(@class,"price-info pa1-rmm-price")]/div/span/span/text()').get(),
                'product_id':response.xpath('//div[contains(@class,"product-sku pa1-rm-tax")]/span/text()').get().replace('item no.\xa0',''),
                'sizes':response.xpath('//ul[contains(@class,"sizes")]/li/a/span/text()').getall(),
                'description': response.xpath('//p[contains(@class,"pa1-rmm product-description")]/text()').get(),
                'other_images':response.css('img.lazyload').xpath('@data-src').getall()
        }