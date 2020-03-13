import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pathlib import Path

# Get HTML
driver = webdriver.Firefox()
driver.get("https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd?type=wti")
html = driver.page_source
driver.quit()

# Beautiful Soup
soup = BeautifulSoup(html, 'lxml')

# Remove unnecessary tabs and linebreaks
for char in '\t\n':
    html=html.replace(char,' ')

# Get all table rows
table = soup.find(id='historic-price-list')
rows = table.find_all('tr')

# for row in rows:
#     row_td = row.find_all('td')
#     str_cells = str(row_td)
#     cleantext = BeautifulSoup(str_cells, "lxml").get_text()
#     #print(cleantext)

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
    # Removal of tabs and linebreaks
    for char in '\t\n':
        str_cells=str_cells.replace(char,'')
    list_rows.append(str_cells)

# Convert rows to dataframe
df_rows = pd.DataFrame(list_rows)
df_rows = df_rows[0].str.split(',', expand=True)
df_rows.head(10)

# Extract Labels
col_labels = table.find_all('th')

# Prepare Labels
list_labels = ""
for label in col_labels:
    # Remove commas if any
    str_label = str(label)
    str_label = str_label.replace(',', '')
    # Remove html formatting
    clean = re.compile('<.*?>')
    str_label = (re.sub(clean, '',str_label))
    # Removal of tabs and linebreaks
    for char in '\t\n[]':
        str_label=str_label.replace(char,'')
    #print(str_label)
    list_labels = list_labels + str_label + ","

# Check labels
print(list_labels)

# Add to array
all_header = []
all_header.append(list_labels)
print(all_header)


# Convert header to dataframe
df_header = pd.DataFrame(all_header)
df_header = df_header[0].str.split(',', expand=True)
df_header.head()

# Add headers to 1st row in dataset
frames = [df_header, df_rows]
df = pd.concat(frames)
# Use 1st row to build header
df = df.rename(columns=df_header.iloc[0])
df.head()
# Drop headers from 1st row
df = df.drop(df.index[0])
df.head()

# Check dataframe correct
df.info()
df.shape

# Prepare output dir
output_dir = Path('output')
output_dir.mkdir(parents=True, exist_ok=True)

# Save to CSV
df.to_csv(r'output/dataset1.csv', index=False)