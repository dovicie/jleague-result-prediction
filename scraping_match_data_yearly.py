import re
import csv
import time
import requests
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

club_and_id = pd.read_csv('./club_and_id.csv')

df_elo = pd.read_csv("./elorating.csv")
df_elo["date"] = pd.to_datetime(df_elo["date"])
df_elo = df_elo.set_index("date")

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
#     club_and_id = pd.read_csv('./club_and_id.csv')

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
    df = df.drop("Score", axis=1)
    

    df.insert(9,'W/L',np.nan) 

    for index,row in df.iterrows():
            if row["HomeGF"] >row["AwayGF"]:
                df.at[index,"W/L"] = 1
            elif row["HomeGF"] < row["AwayGF"]:
                df.at[index,"W/L"] = 2
            else:
                df.at[index,"W/L"] = 0
                
    

    df['W/L'] = df['W/L'].astype('int')
    

    df["Attendances"] = df["Attendances"].str.replace(',','').astype(int)


    df.insert(12 ,"HomeRate", np.nan)
    df.insert(13,"AwayRate",np.nan)
    df.insert(14 ,"HomeRD", np.nan)
    df.insert(15,"AwayRD",np.nan)
    
    df["Date"]=pd.to_datetime(df["Date"])

    for index,row in df.iterrows():
        home_elo = df_elo.loc[row["Date"], row["Home"]]
        away_elo = df_elo.loc[row["Date"], row["Away"]]    

        df.at[index,"HomeRate"] = home_elo
        df.at[index,"AwayRate"] = away_elo

        home_elo_1mago = df_elo.loc[row["Date"]- pd.tseries.offsets.DateOffset(months = 1), row["Home"]]
        away_elo_1mago = df_elo.loc[row["Date"]- pd.tseries.offsets.DateOffset(months = 1), row["Away"]]

        df.at[index,"HomeRD"] = home_elo - home_elo_1mago
        df.at[index,"AwayRD"] = away_elo - away_elo_1mago
        
    df[["HomeRate","AwayRate","HomeRD","AwayRD"]] = round(df[["HomeRate","AwayRate","HomeRD","AwayRD"]]).astype(int)
    
    
    df.insert(0,"ID",np.nan)
    df["ID"] = df["ID"].astype(str)
    
    for index,row in df.iterrows():
        df.at[index,"ID"] = row["Date"].strftime('%y')+str(row["Sec"]).zfill(2)+str(row["HomeID"]).zfill(2)+str(row["AwayID"]).zfill(2)
     

    df.to_csv(f'./match_data_yearly/{year}.csv',index=False)
    
def main():
    for year in (2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020):
        write_data(year)
        preprocess_data(year)
        time.sleep(1)

if __name__ == '__main__':
    main()
