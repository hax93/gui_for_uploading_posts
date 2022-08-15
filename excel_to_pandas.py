import glob

import pandas as pd

"""Pandas
data from sp.xlsx
"""

file = 'data/final_excel.xlsx'


def list_excel():
    data = []
    df = pd.read_excel(file)
    suma = 0
    for i in range(0, 100): 
        if df.loc[i]['xyz'] == False:        
            result = df.loc[i]['xyz'], df.loc[i]['xyz']
            data.append(result)
            suma += 1
        else:
            continue
    return data
        
def list_excel_items(name_postano):
    #   return title, name, date start/expired
    df = pd.read_excel(file)
    for i in range(len(df["xyz"].values)):        
        if name_postano == df["xyz"].values[i]:
            od = df.loc[i]['xyz']
            do = df.loc[i]['xyz']
            indx = i
            return df.iloc[indx][0], od[:10], do[:10], df.iloc[indx][3], df.iloc[indx][9]


