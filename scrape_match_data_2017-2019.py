import re
import csv
import time
import requests
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def write_data():
    # 年度	2020年
    # 大会	Ｊ１リーグ
    # 節	(指定なし)
    # チーム	札幌,仙台,鹿島,浦和,柏,FC東京,川崎Ｆ,横浜FM,横浜FC,湘南,清水,名古屋,Ｇ大阪,Ｃ大阪,神戸,広島,鳥栖,大分
    # ホームアウェイ	全体
    url = 'https://data.j-league.or.jp/SFMS01/search?competition_years=2019&competition_years=2018&competition_years=2017&competition_frame_ids=1&team_ids=14&team_ids=54&team_ids=1&team_ids=3&team_ids=11&team_ids=22&team_ids=21&team_ids=5&team_ids=34&team_ids=12&team_ids=7&team_ids=8&team_ids=9&team_ids=20&team_ids=18&team_ids=10&team_ids=33&team_ids=31&home_away_select=0&tv_relay_station_name=' 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('tr')
    data = []
    for record in records[:-9]:
        l = [field.text for field in record.find_all(['th','td'])]           
        data.append(l)

    with open('./match_data_2017-2019.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def preprocess_data():
    df = pd.read_csv('./match_data_2017-2019.csv')
    club_and_id = pd.read_csv('./club_and_id.csv')
    df_14to16_pts = pd.read_csv("./results_2014_2016.csv")
    
    df = df.replace({'\t','\r','\n'},'',regex=True)
    df = df.drop({"大会","インターネット中継・TV放送"}, axis=1) 
    
    df ["試合日"] = df["試合日"].replace('\(.+\)','',regex=True)
    for index,row in df.iterrows():
        df.at[index,"試合日"] = datetime.datetime.strptime(f'{row["年度"]}/{row["試合日"]}','%Y/%m/%d')
        
    df["節"] =df["節"].replace({'第','節.+日'},'',regex=True).astype(int)

    
    homeclub_ids = []
    awayclub_ids = []

    for index,row in df.iterrows():
        if not row["ホーム"] in club_and_id["クラブ名"].values:
            homeclub_ids.append(0)
            df.at[index,"ホーム"] = "other"
        else:
            for i,r in club_and_id.iterrows():
                if row["ホーム"] == r["クラブ名"]:
                    homeclub_ids.append(r["club_id"])  
                    df.at[index,"ホーム"] = r["club"]

        if not row["アウェイ"] in club_and_id["クラブ名"].values:
            awayclub_ids.append(0)
            df.at[index,"アウェイ"] = "other"
        else:
            for i,r in club_and_id.iterrows():
                if row["アウェイ"] == r["クラブ名"]:
                    awayclub_ids.append(r["club_id"])  
                    df.at[index,"アウェイ"] = r["club"]
                    
    df.insert(7, 'HomeID',homeclub_ids)
    df.insert(8, 'AwayID', awayclub_ids)
    
    
    home_gfs = []
    away_gfs = []
    
    for index,row in df.iterrows():
        home_gf,away_gf = map(int,row["スコア"].split("-"))
        home_gfs.append(home_gf)
        away_gfs.append(away_gf)
        
    df.insert(9, 'HomeGF', home_gfs)
    df.insert(10, 'AwayGF', away_gfs)
    
    
    win_loss = [] 
    
    for index,row in df.iterrows():
        if row["HomeGF"] >row["AwayGF"]:
            win_loss.append(1)
        elif row["HomeGF"] < row["AwayGF"]:
            win_loss.append(2)
        else:
            win_loss.append(0)
            
    df.insert(8,'W/L',win_loss)  
    
    df["入場者数"] = df["入場者数"].str.replace(',','').astype(int)
    
    df = df.drop({"年度","K/O時刻" ,"スコア"}, axis=1) 
    df = df.rename(columns={'節': 'Sec', '試合日': 'Date',  'ホーム': 'Home', 'アウェイ': 'Away','スタジアム': 'Stadium', '入場者数': 'Attendances'})
    
    #  2014-2016の間での1試合あたりの勝ち点と得失点数(Points/M､GD)を作成
    df.insert(11, "Points/M", np.nan)
    df.insert(12,"GD",np.nan)
    
    for index,row in df.iterrows():
        for i,r in df_14to16_pts.iterrows():
            if row["HomeID"] == r["HomeClubID"] and row["AwayID"] == r["AwayClubID"] :
                df.at[index,"Points/M"] = r["Points/M"]
                df.at[index,"GD"] = r["GD"]
                
    df = df.dropna(how='any')
    
    
    for index,row in df.iterrows():
        df_home = pd.read_csv(f'./elo_rating_data/{row["Home"]}.csv')
        df_away = pd.read_csv(f'./elo_rating_data/{row["Away"]}.csv')
        df_home["Month"] = pd.to_datetime(df_home["Month"])
        df_away["Month"] = pd.to_datetime(df_away["Month"])
        for i,r in df_home.iterrows():
            if row["Date"].year == r["Month"].year and row["Date"].month == r["Month"].month:
                df.at[index,"HomeElo"] = r["Points"]
        for i,r in df_away.iterrows():
            if row["Date"].year == r["Month"].year and row["Date"].month == r["Month"].month:
                df.at[index,"AwayElo"] = r["Points"]


    
 
    df.to_csv('./match_data_2017-2019.csv',index=False)

def main():
    write_data()
    preprocess_data()
    time.sleep(1)

if __name__ == '__main__':
    main()
