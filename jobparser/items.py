import scrapy


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    employer = scrapy.Field()
    ref = scrapy.Field()

    pass
