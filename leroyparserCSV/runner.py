from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroyparserCSV.spiders.leroy import LeroySpider
from leroyparserCSV import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroySpider)
    process.start()
