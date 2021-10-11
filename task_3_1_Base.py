import requests
from bs4 import BeautifulSoup
import pandas
import re
from pymongo import MongoClient


def my_base(vacancies):
    """Вносим вакансии в базу, если в коллекции вакансии отсутствуют, и запускаем поиск по размеру оплаты"""

    client = MongoClient('localhost', 27017)
    db = client['vacancies']
    collection = db.python_vacancies
    for el in vacancies:
        if not collection.find(el):
            collection.insert_one(el)

    vacancy_filter = collection.find({'размер оплаты MIN': {'$gte': int(input('Ввведите размер оплаты MIN: '))},
                                      'валюта': input('Ввведите валюту (руб., USD или EUR): ')},
                                     {'название вакансии': 1, 'организация': 1, 'размер оплаты MIN': 1,
                                      'ссылка на вакансию': 1, 'валюта': 1, '_id': 0})
    df = pandas.DataFrame(vacancy_filter)
    print(df)


def get_page(page):
    """Получаем страницу с вакансиями по ключевому слову Python в Казани"""

    error = False
    if page == 1:
        url = 'https://kazan.hh.ru/search/vacancy?clusters=true&area=88&ored_clusters=true&enable_snippets=' \
              'true&salary=&st=searchVacancy&text=Python&page=0'
    else:
        url = 'https://kazan.hh.ru/search/vacancy?clusters=true&area=88&ored_clusters=true&enable_snippets=' \
              'true&salary=&st=searchVacancy&text=Python&page=' + page
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code != 200:
        error = True
        return '', error
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup, error


def get_vacancies(soup, vacancies):
    """Получаем название вакансий, размер оплаты, ссылку на вакансии со страницы"""

    res = soup.find_all(name='div', attrs={'class': 'vacancy-serp-item'})
    if res:
        for el in res:
            vacancy_name = el.find(name='a',
                                   attrs={'class': 'bloko-link'}).string
            vacancy_ref = el.find(name='a',
                                  attrs={'class': 'bloko-link'}).get('href')
            employer = el.find_next(name='a',
                                    attrs={'class': 'bloko-link bloko-link_secondary',
                                           'data-qa': 'vacancy-serp__vacancy-employer'}).contents[-1]
            compensation = el.find(name='span',
                                   attrs={'data-qa': 'vacancy-serp__vacancy-compensation',
                                          'class': 'bloko-header-section-3 bloko-header-section-3_lite'})
            if compensation is None:
                compensation = 'не указан'
                vacancy = {'название вакансии': vacancy_name,
                           'организация': employer,
                           'размер оплаты MIN': compensation,
                           'размер оплаты MAX': compensation,
                           'валюта': 'не указанa',
                           'ссылка на вакансию': vacancy_ref}
                vacancies.append(vacancy)
            else:
                compensation_str = ', '.join(compensation.contents).replace('\u202f', '')
                pattern = re.compile(r'\d+')
                compensation_list = re.findall(pattern, compensation_str)
                pattern_currency = re.compile(r'руб\.|USD|EUR')
                currency = re.search(pattern_currency, compensation_str).group()
                if len(compensation_list) == 2:
                    min_compensation = int(compensation_list[0])
                    max_compensation = int(compensation_list[1])
                    vacancy = {'название вакансии': vacancy_name,
                               'организация': employer,
                               'размер оплаты MIN': min_compensation,
                               'размер оплаты MAX': max_compensation,
                               'валюта': currency,
                               'ссылка на вакансию': vacancy_ref}
                    vacancies.append(vacancy)
                else:
                    min_compensation = int(compensation_list[0])
                    max_compensation = 'не указан'
                    vacancy = {'название вакансии': vacancy_name,
                               'организация': employer,
                               'размер оплаты MIN': min_compensation,
                               'размер оплаты MAX': max_compensation,
                               'валюта': currency,
                               'ссылка на вакансию': vacancy_ref}
                    vacancies.append(vacancy)


def get_next_page_number(soup, num_pages):
    """Получаем номер номер следующей страницы"""

    res = soup.find(name='a', attrs={'class': 'bloko-button'})
    if not res:
        return 0
    page = res.get('href')[-1:1] + f'{num_pages}'
    return page


def parse():
    """Главная функция c добавлением в Mongo"""

    page = 1
    num_pages = 0
    vacancies = []

    while page:
        soup, error = get_page(page)
        if error:
            break

        get_vacancies(soup, vacancies)
        num_pages += 1

        page = get_next_page_number(soup, num_pages)

    print(f'Распарсено {num_pages} страниц, получено {len(vacancies)} вакансий.')

    my_base(vacancies)


if __name__ == '__main__':
    parse()
