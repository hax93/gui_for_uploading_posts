"""URL
from csv
"""
import csv
import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup

#   errors
logging.basicConfig(filename='error_message.txt',
                    filemode='a+',
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s"
                    )

try:
    slownik = {}
    header = ['Tytuł', 'ID', 'Link']
    data = []
    file_html = 'data/sp.html'
    link_do_edit = []

    def sharepoint_attachment_link(name_postano):
        with requests.Session() as session:
            with open(file_html, 'r', encoding='UTF-8') as response:
                soup = BeautifulSoup(response, 'html.parser')

                #   get all title result
                for i in soup.select('div[id]'): 
                    link = i.find('a', href=True)
                    if link is None:
                        continue
                    x = link.get('href')
                    find_id = x.find('ID=')
                    id = x[find_id + 3:120]
                    data.append([link.get_text(), id, x])

                    with open('data/lista.csv', 'w', encoding='UTF-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(data)
                        
            # search name in base
            df = pd.read_csv('data/lista.csv')
            for i in range(len(df.Tytuł)):
                if name_postano == df.Tytuł[i]:
                    indx = i
                    link_do_edit.append(df.iloc[indx][2])
                    return df.iloc[indx][0], df.iloc[indx][1], df.iloc[indx][2]
                else:
                    continue

                
except Exception as exc:
    logging.error(f"ERROR: {exc}")

