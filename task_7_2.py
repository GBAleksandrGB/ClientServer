from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['products']
collection = db.mvideo_products

with webdriver.Chrome() as driver:
    driver.get('https://www.mvideo.ru/')
    products = driver.find_elements(By.XPATH, '//mvid-product-mini-card')
    for product in products:
        product_list = product.text.split('\n')
        if len(product_list) > 5:
            product_for_db = {'Товар': product_list[1],
                              'Скидка': product_list[0],
                              'Рейтинг': product_list[2],
                              'Отзывы': product_list[3],
                              'Новая цена': product_list[4].replace(' ', ''),
                              'Старая цена': product_list[5].replace(' ', '')
                              }
        else:
            product_for_db = {'Товар': product_list[1],
                              'Скидка': product_list[0],
                              'Рейтинг': 'отсутствует',
                              'Отзывы': 'отсутствуют',
                              'Новая цена': product_list[3].replace(' ', ''),
                              'Старая цена': product_list[4].replace(' ', '')
                              }
        collection.insert_one(product_for_db)
        # print(product_for_db)
