import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from itemloaders import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://kazan.leroymerlin.ru/catalogue/iskusstvennye-eli/']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="c155f0re_plp c1pkpd8l_plp largeCard"]/a/@href').getall()
        for link in links:
            yield response.follow('https://kazan.leroymerlin.ru' + link, callback=self.parse_links)

    def parse_links(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), selector=response)
        loader.add_xpath('name', '//h1[@class="header-2"]/text()')
        loader.add_xpath('photos', '//uc-pdp-card-ga-enriched/uc-pdp-media-carousel'
                                   '//source[@media=" only screen and (min-width: 1024px)"]/@srcset')
        loader.add_xpath('price', '//uc-pdp-price-view/span/text()')
        yield loader.load_item()
