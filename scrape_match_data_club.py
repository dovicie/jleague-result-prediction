import csv
import time
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

def write_data(c,club, year):
    url = f'https://www.football-lab.jp/{c}/match/?year={year}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('tr')
    data = []
    for record in records[1:]:
        l = [field.text for field in record.find_all(['th','td'])]           
        data.append(l)

    with open(f'./match_data/{club}/{club}_{year}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def preprocess_data(c,club,year):
    df = pd.read_csv(f'./match_data/{club}/{club}_{year}.csv')
    
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
    
    for index,row in  df.iterrows():
        df.at[index,"開催日"] = datetime.datetime.strptime(f'{year}.{str(row["開催日"])}','%Y.%m.%d')

        
    goals_fors = []
    goals_againsts = []
    
    for index,row in df.iterrows():
        gf,ga = map(int,row["スコア"].split("-"))
        goals_fors.append(gf)
        goals_againsts.append(ga)
        
    df.insert(5, 'GF', goals_fors)
    df.insert(6, 'GA', goals_againsts)
    
    
    win_loss = []  
    
    for index,row in df.iterrows():
        if row["GF"] >row["GA"]:
            win_loss.append(1)
        elif row["GF"] < row["GA"]:
            win_loss.append(2)
        else:
            win_loss.append(0)

    df.insert(7,'W/L',win_loss)   
    
                
    df=df.fillna("") # NaNを空の文字列で埋める
    
    for index,row in df.iterrows():
        scorers = row["得点者"].split(",")
        df.at[index,"得点者"] = scorers
    
    
    club_and_id = pd.read_csv('./club_and_id.csv')
    opponent_ids = []
    
    for index,row in df.iterrows():
            if not row["相手"] in club_and_id["クラブ名"].values:
                opponent_ids.append(0)
                df.at[index,"相手"] = "other"
            else:
                for i,r in club_and_id.iterrows():
                    if row["相手"] == r["クラブ名"]:
                        opponent_ids.append(r["club_id"])
                        df.at[index,"相手"] = r["club"]
    
    df.insert(4, 'OppID', opponent_ids)
    
    df = df.drop(df.columns[2], axis=1) 
    df = df.rename(columns={'節': 'Sec', '開催日': 'Date',  '相手': 'Opp', 'スコア': 'Score', '会場': 'Stadium', '観客数': 'Attendances', '天候': 'Weather','チャンス構築率': 'CBR', 'シュート': 'Shots',  'シュート成功率': 'SSR', '支配率': 'Possession', '攻撃CBP': 'AttackCBP', 'パスCBP': 'PassCBP', '奪取P': 'StealP', '守備P': 'DefenceP',  '得点者': 'Scorers', '指揮官': 'HeadCoach'})

    
    df.to_csv(f'match_data/{club}/{club}_{year}.csv',index=False)

def main():
    cs = ['sapp','send','kasm','uraw','kasw','fctk',"ka-f","y-fm",'y-fc','shon','shim','nago','g-os','c-os','kobe','hiro','toku','fuku','tosu','oita']
    clubs = ['consadole-sapporo','vegalta-sendai','kashima-antlers','urawa-red-diamonds','kashiwa-reysol','fc-tokyo','kawasaki-frontale','yokohama-fa-marinos','yokohama-fc','shonan-bellmare','shimizu-s-pulse','nagoya-grampus-eight','gamba-osaka','cerezo-osaka','vissel-kobe','sanfrecce-hiroshima','sagan-tosu','oita-trinita']
    for c,club in zip(cs,clubs):
        for year in (2018,2019, 2020):
            write_data(c,club, year)
            preprocess_data(c,club, year)
            time.sleep(1)


if __name__ == '__main__':
    main()
