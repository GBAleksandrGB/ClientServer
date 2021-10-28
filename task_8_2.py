# import pandas as pd
# url = 'http://www.meteorf.ru/opendata/7703092752-kosmon/data-20151230-structure-20151230.csv'
# data_frame = pd.read_csv(url, sep=',')
# print(data_frame[data_frame['MaxSpeed'] > 3])


import csv
from requests import get


url = 'http://www.meteorf.ru/opendata/7703092752-kosmon/data-20151230-structure-20151230.csv'
data = get(url)
f = open('data.csv', 'wb')
f.write(data.content)
f.close()
with open('data.csv', 'r', encoding='UTF-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    field_names = reader.fieldnames
    for row in reader:
        print(row['Year'], row['Region'], row['TotalCyclones'], row['MaxSpeed'], sep=', ')
