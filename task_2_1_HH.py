import requests
from bs4 import BeautifulSoup
import pandas


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
            employer = el.find(name='a', attrs={'class': 'bloko-link bloko-link_secondary',
                                                'data-qa': 'vacancy-serp__vacancy-employer'}).string
            vacancy = {'название вакансии': vacancy_name,
                       'организация': employer,
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
    """Главная функция"""

    page = 1
    num_pages = 0
    vacancies = []

    while int(page) == 1:
        soup, error = get_page(page)
        if error:
            break

        get_vacancies(soup, vacancies)
        num_pages += 1

        page = get_next_page_number(soup, num_pages)

    print(f'Распарсены первые {num_pages} страницы.')
    df = pandas.DataFrame(vacancies, index=range(1, len(vacancies) + 1))
    print(df)


if __name__ == '__main__':
    parse()
