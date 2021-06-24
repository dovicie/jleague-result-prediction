import re
import csv
import time
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from ast import literal_eval

def write_data(team):
    url = f'https://footballdatabase.com/clubs-ranking/{team}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('script')
    m = re.search('^.*var data_array=([^;]*).*$', records[1].contents[0])
    data_list = literal_eval(m.group(1))

    with open(f'./elo_rating_data/{team}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data_list)

def preprocess_data(team):
    df = pd.read_csv(f'./elo_rating_data/{team}.csv')
    
    df = df.drop(df.index[-1]) # Today行(最終行)削除
    
    for index,row in  df.iterrows():
        df.at[index,"Month"] = datetime.datetime.strptime(row["Month"],'%B %Y')
    df["Month"] = pd.to_datetime(df["Month"])

    df.to_csv(f'elo_rating_data/{team}.csv',index=False)

def main():
    for team in ('consadole-sapporo','vegalta-sendai','kashima-antlers','urawa-red-diamonds','kashiwa-reysol','fc-tokyo','kawasaki-frontale','yokohama-fa-marinos','yokohama-fc','shonan-bellmare','shimizu-s-pulse','nagoya-grampus-eight','gamba-osaka','cerezo-osaka','vissel-kobe','sanfrecce-hiroshima','tokushima-vortis','avispa-fukuoka','sagan-tosu','oita-trinita'):
        write_data(team)
        preprocess_data(team)
        time.sleep(1)


if __name__ == '__main__':
    main()
