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
        data.append(l)

    with open(f'./match_data/{team_id}/{team_id}_{year}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def preprocess_data(team_id,year):
    df = pd.read_csv(f'./match_data/{team_id}/{team_id}_{year}.csv')
    
    df = df.rename(columns={df.columns[2]: '曜日'})
    
    df = df.rename(columns={df.columns[5]: 'H/A'})
    df["H/A"]=df["H/A"].replace("H",0)
    df["H/A"]=df["H/A"].replace("A",1)
    
    df['観客数'] = df['観客数'].str.replace(',','').astype(int)
    
    df['チャンス構築率'] = df['チャンス構築率'].str.replace('%','').astype(float)*0.01
    df["チャンス構築率"] = df["チャンス構築率"].round(3)

    df['シュート成功率']= df['シュート成功率'].str.replace('%','').astype(float).round(3)*0.01
    df["シュート成功率"] = df["シュート成功率"].round(3)
    
    df['支配率']= df['支配率'].str.replace('%','').astype(float).round(3)*0.01
    df["支配率"] = df["支配率"].round(3)
    
    for i in range(len(df["開催日"])):
        dt = datetime.datetime.strptime(f'{year}.{df["開催日"][i]}', '%Y.%m.%d')
        df["開催日"][i] = datetime.date(dt.year, dt.month, dt.day)

    score_list = []
    concede_list = []
    for i in range(len(df)):
            score,concede=map(int,df["スコア"][i].split("-"))
            score_list.append(score)
            concede_list.append(concede)
            
    df.insert(5, '得点', score_list)
    df.insert(6, '失点', concede_list)
    
    win_loss_list = []
    for index,row in df.iterrows():
        if row["得点"] >row["失点"]:
            win_loss_list.append(1)
        elif row["得点"] < row["失点"]:
            win_loss_list.append(2)
        else:
            win_loss_list.append(0)
    
    df.insert(7,'勝敗',win_loss_list)
    
                
    df=df.fillna("")
    
    for i in range(len(df)):
        scorer_list = df["得点者"][i].split(",")
        df["得点者"][i] = scorer_list

    df.to_csv(f'match_data/{team_id}/{team_id}_{year}.csv',index=False)

def main():
    for team_id in ('sapp','send','kasm','uraw','kasw','fctk',"ka-f","y-fm",'y-fc','shon','shim','nago','g-os','c-os','kobe','hiro','toku','fuku','tosu','oita'):
        for year in (2018,2019, 2020):
            write_data(team_id, year)
            preprocess_data(team_id, year)
            time.sleep(1)


if __name__ == '__main__':
    main()
