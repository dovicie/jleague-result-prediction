import csv
import time
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

def write_data(team_id, year):
    url = f'https://www.football-lab.jp/{team_id}/match/?year={year}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('tr')
    data = []
    for record in records[1:]:
        l = [field.text for field in record.find_all(['th','td'])]
        #if record in records[2:]:        
            #l[0] = int(l[0])
            #dt = datetime.datetime.strptime(f'{year}.{l[1]}', '%Y.%m.%d')
            #l[1] = datetime.date(dt.year, dt.month, dt.day)

            #l[5] = 1 if l[5] == 'H' else 0

            #for i in [11,13,14]:
            #   l[i] = l[i].replace('%','')

            #l[7] = l[7].replace(',','')

            #for i in [0,7,9,10,12]:
            #    l[i] = int(l[i])

            #for i in [11,13,14,15,16,17,18]:
            #    l[i] = float(l[i])
            
        data.append(l)

    with open(f'{team_id}_{year}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def preprocess_data(team_id,year):
    df = pd.read_csv(f'{team_id}_{year}.csv')
    df.set_index('節',inplace=True)
    df = df.rename(columns={df.columns[1]: '曜日'})
    df = df.rename(columns={df.columns[4]: 'H/A'})
    df['観客数'] = df['観客数'].str.replace(',','').astype(int)
    df['チャンス構築率']= df['チャンス構築率'].str.replace('%','').astype(float)
    df['シュート成功率']= df['シュート成功率'].str.replace('%','').astype(float)

    with open(f'{team_id}_{year}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(df)

def main():
    for team_id in ('shim', 'fctk'):
        for year in (2019, 2020):
            write_data(team_id, year)
           # preprocess_data(team_id, year)
            time.sleep(1)


if __name__ == '__main__':
    main()
