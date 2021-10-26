from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['mail']
collection = db.mail_parts

with webdriver.Chrome() as driver:
    driver.get('https://login.yahoo.com/')
    username = driver.find_element(By.XPATH, "//input[@name='username']")
    username.send_keys('tomilov.alex@yahoo.com')
    entry = driver.find_element(By.XPATH, "//input[@id='login-signin']").submit()
    password = driver.find_element(By.XPATH, "//input[@type='password']")
    password.send_keys('GBAleksandrGB')
    entry_next = driver.find_element(By.XPATH, "//button[@id='login-signin']").submit()


    # message_box = driver.find_elements(By.XPATH, '//div[tempid="id=readingpaneView;path=Applications/Views/Mail/MailModuleView.htm"]')

    # print(message_box)


#     for el in vacancies:
#         if el not in list(collection.find({}, {'_id': 0})):
#             collection.insert_one(el)