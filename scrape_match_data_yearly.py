import re
import csv
import time
import requests
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def write_data(year):        
    url = f'https://data.j-league.or.jp/SFMS01/search?competition_years={year}&competition_frame_ids=1' 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('tr')
    data = []
    for record in records[:-9]:
        l = [field.text for field in record.find_all(['th','td'])]           
        data.append(l)

    with open(f'./match_data_yearly/{year}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def preprocess_data(year):
    df = pd.read_csv(f'./match_data_yearly/{year}.csv')
    club_and_id = pd.read_csv('./club_and_id.csv')

    df = df.drop({"K/O時刻" ,"大会","インターネット中継・TV放送"}, axis=1) 
    df = df.rename(columns={'年度':'Year','節': 'Sec', '試合日': 'Date',  'ホーム': 'Home','スコア':'Score', 'アウェイ': 'Away','スタジアム': 'Stadium', '入場者数': 'Attendances'})
    df = df.replace({'\t','\r','\n'},'',regex=True)
    
    df ["Date"] = df["Date"].replace('\(.+\)','',regex=True)
    for index,row in df.iterrows():
        df.at[index,"Date"] = datetime.datetime.strptime(f'{row["Year"]}/{row["Date"]}','%Y/%m/%d')
        
        
    df["Sec"] =df["Sec"].replace({'第','節.+日'},'',regex=True).astype(int)


    df.insert(6, 'HomeID',np.nan)
    df.insert(7, 'AwayID', np.nan)

    for index,row in df.iterrows():
        for i,r in club_and_id.iterrows():
            if row["Home"] == r["club_ja"]:
                df.at[index, "HomeID"] = r["club_id"]
                df.at[index,"Home"] = r["club"]

        for i,r in club_and_id.iterrows():
            if row["Away"] == r["club_ja"]:
                df.at[index,"AwayID"] = r["club_id"]
                df.at[index,"Away"] = r["club"]

    df[['HomeID', 'AwayID']] = df[['HomeID', 'AwayID']].astype('int')
                    

    df.insert(8, 'HomeGF', np.nan)
    df.insert(9, 'AwayGF', np.nan)

    for index,row in df.iterrows():
        home_gf,away_gf = map(int,row["Score"].split("-"))
        df.at[index,"HomeGF"] = home_gf
        df.at[index,"AwayGF"] = away_gf
    df[['HomeGF', 'AwayGF']] = df[['HomeGF', 'AwayGF']].astype('int')
    

    df.insert(10,'W/L',np.nan) 

    for index,row in df.iterrows():
            if row["HomeGF"] >row["AwayGF"]:
                df.at[index,"W/L"] = 1
            elif row["HomeGF"] < row["AwayGF"]:
                df.at[index,"W/L"] = 2
            else:
                df.at[index,"W/L"] = 0

    df['W/L'] = df['W/L'].astype('int')
    

    df["Attendances"] = df["Attendances"].str.replace(',','').astype(int)

    
#     df.insert(13 ,"HomeElo", np.nan)
#     df.insert(14,"AwayElo",np.nan)
#     df.insert(15 ,"HomeED", np.nan)
#     df.insert(16,"AwayED",np.nan)

#     for index,row in df.iterrows():
#         df_home = pd.read_csv(f'./elo_rating_data/{row["Home"]}.csv')
#         df_away = pd.read_csv(f'./elo_rating_data/{row["Away"]}.csv')
#         df_home["Month"] = pd.to_datetime(df_home["Month"])
#         df_away["Month"] = pd.to_datetime(df_away["Month"])
#         for i,r in df_home.iterrows():
#             if row["Date"].year == r["Month"].year and row["Date"].month == r["Month"].month:
#                 df.at[index,"HomeElo"] = r["Points"]
#                 df.at[index,"HomeED"] = r["PD"]
#         for i,r in df_away.iterrows():
#             if row["Date"].year == r["Month"].year and row["Date"].month == r["Month"].month:
#                 df.at[index,"AwayElo"] = r["Points"]
#                 df.at[index,"AwayED"] = r["PD"]

                
    df = df.drop("Score", axis=1)
 
    df.to_csv(f'./match_data_yearly/{year}.csv',index=False)
    
def main():
    for year in (2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020):
        write_data(year)
        preprocess_data(year)
        time.sleep(1)

if __name__ == '__main__':
    main()
