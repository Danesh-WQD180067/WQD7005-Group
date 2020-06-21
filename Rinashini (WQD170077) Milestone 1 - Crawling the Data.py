# Project Title: Analyzing Crude Oil Prices with Data Mining Techniques
# Team Members : Danesh A/L Durairetnam (WQD180067)
#                Rinashini A/P Arunasalam Sukormaru (WQD170077)


import matplotlib
import pandas as pd
import re
matplotlib.use('TkAgg')
from bs4 import BeautifulSoup
from selenium import webdriver


## Web crawling
driver = webdriver.Firefox()
driver.get(
    "https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd/3.9.2011_11.3.2020?type=wti")
html = driver.page_source

for char in '\t\n':
    html = html.replace(char, '')

soup = BeautifulSoup(html, 'lxml')
type(soup)
table = soup.find(id='historic-price-list')
rows = table.find_all('tr')
#print(rows)


## Cleaning and Appending Rows
list_rows = []
for row in rows:
    cells = row.find_all('td')
    list_cells = ""
    for cell in cells:
        str_cell = str(cell)
        clean_cell = str_cell.replace(',', '')
        list_cells = list_cells + clean_cell + ","
    str_cells = list_cells
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
#print(clean2)


## Set the data into data frames
df = pd.DataFrame(list_rows)
df1 = df[0].str.split(',', expand=True)
#print(df1)


## Extracting Headers
col_labels = table.find_all('th')
list_labels = "["
for label in col_labels:
    str_label = str(label)
    clean_label = str_label.replace(',', '')
    list_labels = list_labels + clean_label + ","
list_labels = list_labels + "]"
#print(list_labels)

all_header = []
col_str = list_labels
cleantext = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext)
df2 = pd.DataFrame(all_header)
df3 = df2[0].str.split(',', expand=True)
#print(df3)


## Appending Headers to dataset
frames = [df3, df1]
df4 = pd.concat(frames)
pd.set_option('mode.chained_assignment', None)
#print(df4)


## Reformatting header
df5 = df4.rename(columns=df4.iloc[0])
df6 = df5.drop(']', axis=1)
df7 = df6.drop(df6.index[0])
df7.rename(columns={'[Date': 'Date'},inplace=True)
print(df7)

## Exporting dataframe to csv file
df7.to_csv(r'dataset.csv', index=False)