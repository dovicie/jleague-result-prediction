import re
import csv
import time
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from ast import literal_eval

def write_data(club,url):
#     url = f'https://footballdatabase.com/clubs-ranking/{club}'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('script')
    m = re.search('^.*var data_array=([^;]*).*$', records[1].contents[0])
    data_list = literal_eval(m.group(1))

    with open(f'./elo_rating_data/{club}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data_list)

def preprocess_data(club):

    df = pd.read_csv(f'./elo_rating_data/{club}.csv')

    df = df.drop(df.index[-1]) # Today行(最終行)削除

    for index,row in  df.iterrows():
        df.at[index,"Month"] = datetime.datetime.strptime(row["Month"],'%B %Y')
    df["Month"] = pd.to_datetime(df["Month"])

    PD = df["Points"].diff().rename("PD")
    df = pd.concat([df, PD ],axis=1)


    df.to_csv(f'elo_rating_data/{club}.csv',index=False)
    

def main():
    for club in ('kashima-antlers','jef-united','urawa-red-diamonds','tokyo-verdy','yokohama-fa-marinos','yokohama-flugels','shimizu-s-pulse','nagoya-grampus-eight','gamba-osaka','sanfrecce-hiroshima','kashiwa-reysol','shonan-bellmare','jubilo-iwata','consadole-sapporo','vissel-kobe','cerezo-osaka','kawasaki-frontale','fc-tokyo','avispa-fukuoka','kyoto-sanga','omiya-ardija','ventforet-kofu','montedio-yamagata','oita-trinita','sagan-tosu','yokohama-fc','tokushima-vortis','matsumoto-yamaga','v-varen-nagasaki','vegalta-sendai','albirex-niigata'):
        
        url = f'https://footballdatabase.com/clubs-ranking/{club}'
        
        if requests.get(url).url == url:
            write_data(club,url)
            preprocess_data(club)
            time.sleep(1)


if __name__ == '__main__':
    main()
