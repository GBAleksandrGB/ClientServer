import requests
from lxml import html
from pymongo import MongoClient
import datetime
from pprint import pprint


def add_to_base(news_list):
    client = MongoClient('localhost', 27017)
    db = client['news']
    collection = db.top_news
    count_new_news = 0
    for el in news_list:
        if el not in list(collection.find({}, {'_id': 0})):
            collection.insert_one(el)
            count_new_news += 1
    count_news_in_base = collection.count_documents({})
    pprint(f'Всего в базе {count_news_in_base} новостей.')
    pprint(f'Добавлено новых новостей: {count_new_news}')
    news_from_base = collection.find({}, {'_id': 0})
    pprint(list(news_from_base), width=100)


def get_parse(res_html, path):
    news_headers = res_html.xpath(path[0])
    news_refs = res_html.xpath(path[1])
    news_sources = []
    news_dates = []
    dt = datetime.datetime
    for ref in news_refs:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(ref, headers=headers)
        if res:
            res_html = html.fromstring(res.text)
            news_source = res_html.xpath(path[2])
            news_sources.append(news_source[0])
            news_date = res_html.xpath(path[3])
            news_dates.append(dt.fromisoformat(*news_date).strftime('%d.%m.%Y г. %H:%M'))
    news_zip = zip(map(lambda x: x.replace('\xa0', ' ').strip(), news_headers), news_refs, news_sources, news_dates)
    news_list = []
    for el in list(news_zip):
        d_el = {'заголовок новости': el[0],
                'ссылка на новость': el[1],
                'источник новости': el[2],
                'дата новости': el[3]}
        news_list.append(d_el)
    return news_list


def get_request(links):
    error = False

    for link, path in links.items():
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(link, headers=headers)
        if res.status_code != 200:
            error = True
            print(res.status_code)
        res_html = html.fromstring(res.text)
        return get_parse(res_html, path), error


def get_news():
    mail_text = '//span[contains(@class, "js-topnews__notification")]/text()'
    mail_href = '//a[contains(@class, "js-topnews__item")]/@href'
    mail_source = '//a[contains(@class, "link color_gray breadcrumbs__link")]/span/text()'
    mail_date = '//span[contains(@class, "breadcrumbs__item")]/span/span/@datetime'

    links = {'https://news.mail.ru/': [mail_text, mail_href, mail_source, mail_date]}

    news_list, error = get_request(links)

    if error:
        return 1

    add_to_base(news_list)


if __name__ == '__main__':
    get_news()
