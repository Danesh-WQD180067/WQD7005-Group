import re
import pandas as pd

# WebScraping
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date
from datetime import timedelta

# Get HTML
driver = webdriver.Firefox()
lastYear  = (date.today() - timedelta(days = 365)).strftime('%d.%m.%y')
todayDate = date.today().strftime('%d.%m.%y')

driver.get("https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd/"   + lastYear + '_' + todayDate)
html = driver.page_source
driver.quit()

# Remove unnecessary tabs and linebreaks
for char in '\t\n':
    html=html.replace(char,'')

# Beautiful Soup
soup = BeautifulSoup(html, 'lxml')

# Get all table rows
table = soup.find(id='historic-price-list')
rows = table.find_all('tr')

# Add rows to array.
list_rows = []
for row in rows:
    cells = row.find_all('td')
    list_cells = ""
    # Each cell is cleaned to remove commas (if any)
    # Each cell is then stitched into "list cells" separated by comma
    for cell in cells:
        str_cell = str(cell)
        clean_cell = str_cell.replace(',', '')
        list_cells = list_cells + clean_cell + ","
    str_cells = list_cells
    # Remove html formatting
    clean = re.compile('<.*?>')
    str_cells = (re.sub(clean, '',str_cells))
    list_rows.append(str_cells)

# Convert rows to dataframe
df_rows = pd.DataFrame(list_rows)
df_rows = df_rows[0].str.split(',', expand=True)
df_rows.head(10)

# Labels section removed.
########################

# Drop headers from 1st row
df_rows = df_rows.drop(df_rows.index[0])
df_rows.head()

# Check dataframe correct
df_rows.info()
df_rows.shape

# Prepare output dir
output_dir = Path('output')
output_dir.mkdir(parents=True, exist_ok=True)

# Save to CSV
df_rows.to_csv(r'output/price.csv', index=False)
