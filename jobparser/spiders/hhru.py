import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://kazan.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = 'https://kazan.hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']
        response.follow(next_page, callback=self.parse)
        vac = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header'
                           ' a.bloko-link::attr(href)').getall()
        for link in vac:
            yield response.follow(link, callback=self.vac_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vac_parse(self, response: HtmlResponse):
        name = ''.join(response.css('h1[data-qa="vacancy-title"]::text').getall())
        salary = ''.join(response.css('span[class="bloko-header-2 bloko-header-2_lite"]::text').getall())
        employer = ''.join(response.css('span[data-qa="bloko-header-2"][class="bloko-header-section-2'
                                        ' bloko-header-section-2_lite"]::text').getall())
        ref = response.url

        print('\nНазвание вакансии: ', name)
        print('Зарплата: ', salary)
        print('Работодатель: ', employer)
        print('Ссылка на вакансию: ', ref)

        yield JobparserItem(name=name,
                            salary=salary,
                            employer=employer,
                            ref=ref)


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.start()
