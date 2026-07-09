# using requests

#%pip install requests

import requests

r = requests.get('https://res2.imgw.pl/products/hydro/monitor-lite-products/TEMPERATURY_WOD.pdf?ts=1774396800000')

print(r.status_code)

with open('water_temp_today.pdf', 'wb') as f:
    f.write(r.content)


#%pip install pdfplumber
import pdfplumber 
import pandas as pd
import re
import os


tables = []
all_text_chunks = []

# Prevent wrapping and expand the display width
#pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 100)


with pdfplumber.open('water_temp_today.pdf') as pdf:
    for page in pdf.pages:
        tables_on_page = page.extract_tables({})
        text_on_page = page.extract_text()
        if text_on_page:
            all_text_chunks.append(text_on_page)


        if tables_on_page:
            for table in tables_on_page:
                if table:
                    tables.append({
                        'page': pdf.pages.index(page) + 1,
                        'data': table
                    })

for table in tables:
    print('Page:', table['page'])
    df = pd.DataFrame(table['data']) 
    #print(df)
    
#print(all_text_chunks[0])
date = re.search(r'\d{2}\.\d{2}\.\d{4}', all_text_chunks[0])
date_parsed = date.group()

date_dt = pd.to_datetime(date_parsed, format='%d.%m.%Y').date()
print(date_dt)

# ustalenie nazw kolumn 
df.columns = df.iloc[0]
df = df[1:]
df = df.reset_index(drop=True)

df['date'] = date_dt

print(df)

csv_file = "temp.csv"

file_exists = os.path.exists(csv_file)

df.to_csv(csv_file, mode='a', index=False, header=not file_exists, encoding='utf-8')

#df.to_csv("temp.csv", index=False)
