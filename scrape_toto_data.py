import re
import csv
import time
import requests
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def write_data(times):
    
    df=pd.DataFrame(columns=["No","Group","Date","Winning","Match1","Match2","Match3","Match4","Match5"])
    for t in times:
        url =f'https://toto.rakuten.co.jp/toto/result/{t}/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for group in ["A","B"]:
            date = soup.select(f"#minitotoBlock{group} .tbl-basic-day td")[0].string
            wining = soup.select(f"#minitotoBlock{group} .tbl-basic-money tbody td")[0].string
            toto_data = [time, group, date,wining]

            match = soup.select(f"#minitotoBlock{group} .tbl-result tbody tr")
            for i in range(5):
                match_datas =[match[i].select("td")[1].string, match[i].select("td")[3].string, match[i].select("td")[5].string]
                toto_data.append(match_datas)

            df.loc[f"{t}_{group}"]= toto_data


        time.sleep(1)
        
        
        
    df["Date"] = df["Date"].replace('\(.+\)','',regex=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y年%m月%d日")
    
    df=df.set_index(["No","Date","Group"], drop=True)
        
        
    