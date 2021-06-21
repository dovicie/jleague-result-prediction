import csv
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = ["https://data.j-league.or.jp/SFTD04/searchEvent?dspCompetitionFrame=%28%E9%81%B8%E6%8A%9E%E3%81%AA%E3%81%97%29&dspYear=2014%E5%B9%B4%EF%BD%9E2016%E5%B9%B4&dspTeamName=%E6%9C%AD%E5%B9%8C%2C%E4%BB%99%E5%8F%B0%2C%E9%B9%BF%E5%B3%B6%2C%E6%B5%A6%E5%92%8C%2C%E6%9F%8F%2CFC%E6%9D%B1%E4%BA%AC%2C%E5%B7%9D%E5%B4%8E%EF%BC%A6%2C%E6%A8%AA%E6%B5%9CFM%2C%E6%A8%AA%E6%B5%9CFC%2C%E6%B9%98%E5%8D%97%2C%E6%B8%85%E6%B0%B4%2C%E5%90%8D%E5%8F%A4%E5%B1%8B%2C%EF%BC%A7%E5%A4%A7%E9%98%AA%2C%EF%BC%A3%E5%A4%A7%E9%98%AA%2C%E7%A5%9E%E6%88%B8%2C%E5%BA%83%E5%B3%B6%2C%E9%B3%A5%E6%A0%96%2C%E5%A4%A7%E5%88%86&dspOppTeamName=%E4%BB%99%E5%8F%B0%2C%E9%B9%BF%E5%B3%B6%2C%E6%B5%A6%E5%92%8C%2C%E6%9F%8F%2CFC%E6%9D%B1%E4%BA%AC%2C%E5%B7%9D%E5%B4%8E%EF%BC%A6%2C%E6%A8%AA%E6%B5%9CFM%2C%E6%A8%AA%E6%B5%9CFC%2C%E6%B9%98%E5%8D%97%2C%E6%B8%85%E6%B0%B4%2C%E5%90%8D%E5%8F%A4%E5%B1%8B%2C%EF%BC%A7%E5%A4%A7%E9%98%AA%2C%EF%BC%A3%E5%A4%A7%E9%98%AA%2C%E7%A5%9E%E6%88%B8%2C%E5%BA%83%E5%B3%B6%2C%E9%B3%A5%E6%A0%96%2C%E5%A4%A7%E5%88%86&oppoDspFlg=&fromYear=2014&toYear=2016&teamSelect=14&teamSelect=54&teamSelect=1&teamSelect=3&teamSelect=11&teamSelect=22&teamSelect=21&teamSelect=5&teamSelect=34&teamSelect=12&teamSelect=7&teamSelect=8&teamSelect=9&teamSelect=20&teamSelect=18&teamSelect=10&teamSelect=33&teamSelect=31&opponentTeamSelect=54&opponentTeamSelect=1&opponentTeamSelect=3&opponentTeamSelect=11&opponentTeamSelect=22&opponentTeamSelect=21&opponentTeamSelect=5&opponentTeamSelect=34&opponentTeamSelect=12&opponentTeamSelect=7&opponentTeamSelect=8&opponentTeamSelect=9&opponentTeamSelect=20&opponentTeamSelect=18&opponentTeamSelect=10&opponentTeamSelect=33&opponentTeamSelect=31", # 2014年～2016年
        "https://data.j-league.or.jp/SFTD04/searchEvent?dspCompetitionFrame=%28%E9%81%B8%E6%8A%9E%E3%81%AA%E3%81%97%29&dspYear=2017%E5%B9%B4%EF%BD%9E2019%E5%B9%B4&dspTeamName=%E6%9C%AD%E5%B9%8C%2C%E4%BB%99%E5%8F%B0%2C%E9%B9%BF%E5%B3%B6%2C%E6%B5%A6%E5%92%8C%2C%E6%9F%8F%2CFC%E6%9D%B1%E4%BA%AC%2C%E5%B7%9D%E5%B4%8E%EF%BC%A6%2C%E6%A8%AA%E6%B5%9CFM%2C%E6%A8%AA%E6%B5%9CFC%2C%E6%B9%98%E5%8D%97%2C%E6%B8%85%E6%B0%B4%2C%E5%90%8D%E5%8F%A4%E5%B1%8B%2C%EF%BC%A7%E5%A4%A7%E9%98%AA%2C%EF%BC%A3%E5%A4%A7%E9%98%AA%2C%E7%A5%9E%E6%88%B8%2C%E5%BA%83%E5%B3%B6%2C%E9%B3%A5%E6%A0%96%2C%E5%A4%A7%E5%88%86&dspOppTeamName=%E4%BB%99%E5%8F%B0%2C%E9%B9%BF%E5%B3%B6%2C%E6%B5%A6%E5%92%8C%2C%E6%9F%8F%2CFC%E6%9D%B1%E4%BA%AC%2C%E5%B7%9D%E5%B4%8E%EF%BC%A6%2C%E6%A8%AA%E6%B5%9CFM%2C%E6%A8%AA%E6%B5%9CFC%2C%E6%B9%98%E5%8D%97%2C%E6%B8%85%E6%B0%B4%2C%E5%90%8D%E5%8F%A4%E5%B1%8B%2C%EF%BC%A7%E5%A4%A7%E9%98%AA%2C%EF%BC%A3%E5%A4%A7%E9%98%AA%2C%E7%A5%9E%E6%88%B8%2C%E5%BA%83%E5%B3%B6%2C%E9%B3%A5%E6%A0%96%2C%E5%A4%A7%E5%88%86&oppoDspFlg=&fromYear=2017&toYear=2019&teamSelect=14&teamSelect=54&teamSelect=1&teamSelect=3&teamSelect=11&teamSelect=22&teamSelect=21&teamSelect=5&teamSelect=34&teamSelect=12&teamSelect=7&teamSelect=8&teamSelect=9&teamSelect=20&teamSelect=18&teamSelect=10&teamSelect=33&teamSelect=31&opponentTeamSelect=54&opponentTeamSelect=1&opponentTeamSelect=3&opponentTeamSelect=11&opponentTeamSelect=22&opponentTeamSelect=21&opponentTeamSelect=5&opponentTeamSelect=34&opponentTeamSelect=12&opponentTeamSelect=7&opponentTeamSelect=8&opponentTeamSelect=9&opponentTeamSelect=20&opponentTeamSelect=18&opponentTeamSelect=10&opponentTeamSelect=33&opponentTeamSelect=31" # 2017年～2019年
       ]
years = ["2014_2016","2017_2019"]

def write_data(url,year):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    records = soup.find_all('tr')
    data = []
    for record in records[:-4]:
        l = [field.text for field in record.find_all(['th','td'])]           
        data.append(l)

    with open(f'./results_{year}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

def preprocess_data(year):
    df = pd.read_csv(f"./results_{year}.csv")
    
    df = df.drop(df.columns[8], axis=1) # 空のカラムを削除
    df = df.drop('大会', axis=1)
    df = df.rename(columns={'チーム': 'HomeClub', '対戦チーム': 'AwayClub',  '勝': 'Won', '分': 'Drawn', '敗': 'Lost', '得点': 'GF', '失点': 'GA'})
    df = df.groupby(['HomeClub','AwayClub']).sum()
    
    points_per_matchs = []
    goals_defferences = []

    for index,row in df.iterrows():
        points =  row["Won"] * 3 + row["Drawn"] 
        played = row["Won"] + row["Drawn"] + row["Lost"] 
        points_per_match = points / played 
        points_per_matchs.append(round(points_per_match,2))
        
        goals_defference = row["GF"] - row["GA"]
        goals_defferences.append(goals_defference)
        
    df.insert(3,'Points/M',points_per_matchs)
    df.insert(6,'GD',goals_defferences)
    
    club_and_id = pd.read_csv('./club_and_id.csv')
    
    homeclub_ids = []
    homeclubs = []
    awayclub_ids = []
    awayclubs= []
    
    
    for index,row in df.iterrows():
        for i,r in club_and_id.iterrows():
            if index[0] == r["クラブ名"]:
                homeclubs.append(r["club"])
                homeclub_ids.append(r["club_id"])   

            if index[1] == r["クラブ名"]:
                awayclubs.append(r["club"])
                awayclub_ids.append(r["club_id"])

                
    df.insert(0, 'HomeClub', homeclubs)
    df.insert(1, 'AwayClub', awayclubs)
    df.insert(2, 'HomeClubID', homeclub_ids)
    df.insert(3, 'AwayClubID', awayclub_ids)
    
    df.to_csv(f'./results_{year}.csv', index=False)

def main():
    for url,year in zip(urls,years):
        write_data(url,year)
        preprocess_data(year)
        time.sleep(1)

if __name__ == '__main__':
    main()
