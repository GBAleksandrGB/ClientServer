import scrapy


def filter_name(name):
    return ''.join(name)


def filter_price(price):
    return int(''.join(price[0]).replace(' ', ''))


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=filter_name)
    photos = scrapy.Field()
    price = scrapy.Field(output_processor=filter_price)
    pass
