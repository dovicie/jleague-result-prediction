import re
import csv
import time
import requests
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

match_data = pd.read_csv("./match_data_yearly/all_years.csv")
match_data["Date"] = pd.to_datetime(match_data["Date"])
match_data = match_data.set_index(match_data["Date"])

club_id = pd.read_csv("./club_and_id.csv")

def scrape(year):    
    for index,row in match_data[f'{year}'].iterrows():
        month = row["Date"].month
        date = row["Date"].day

        home=row["Home"]
        away=row["Away"]

        match_id=row["ID"]

        for i, r in club_id.iterrows():
            if home == r["club"]:
                club_abbr = r["club_abbr"]

        url = f'https://www.football-lab.jp/{club_abbr}/report/?year={year}&month={month:02}&date={date:02}'
        r = requests.get(url)

        if r.status_code != 200:
            if home == 'fc-tokyo':
                url = f'https://www.football-lab.jp/f-tk/report/?year={year}&month={month:02}&date={date:02}'    
                r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.select(f"article  table.statsTbl6")
        records = table[1].select("tr")

        del records[1::2]


        data = []
        for record in records:
            l = [field.text for field in record.find_all(['th','td'])]           
            data.append(l)


        with open(f'./stats/{year}/{match_id}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
            
        df = pd.read_csv(f'./stats/{year}/{match_id}.csv', index_col=3)
        df = df.drop({"今季平均","成功率","成功率.1","今季平均.1"}, axis=1)
        df = df.rename(columns={'総数':f'{home}', '総数.1':f'{away}'})
        
        
        new_index = []
        try:
        
            if len(df.index) == 24:
                new_index = ["ExpG","Shots","ShotsOnTarget","ShotsFromPK","Passes","Crosses","DirectFK","IndirectFK","CK","Throwin","Dribbling","Tackles","Clearances","Intercepts","Offsides","YellowCards","RedCards","30mLineEntries","PenaltyAreaEntries","DistanceCovered","Sprints","Attacks","ChanceBuildingRate","Possession"]
            elif len(df.index) == 23:
                new_index = ["Shots","ShotsOnTarget","ShotsFromPK","Passes","Crosses","DirectFK","IndirectFK","CK","Throwin","Dribbling","Tackles","Clearances","Intercepts","Offsides","YellowCards","RedCards","30mLineEntries","PenaltyAreaEntries","DistanceCovered","Sprints","Attacks","ChanceBuildingRate","Possession"]
            elif len(df.index) == 22:
                new_index = ["ExpG","Shots","ShotsOnTarget","ShotsFromPK","Passes","Crosses","DirectFK","IndirectFK","CK","Throwin","Dribbling","Tackles","Clearances","Intercepts","Offsides","YellowCards","RedCards","30mLineEntries","PenaltyAreaEntries","Attacks","ChanceBuildingRate","Possession"]
            elif len(df.index) == 21:
                new_index = ["Shots","ShotsOnTarget","ShotsFromPK","Passes","Crosses","DirectFK","IndirectFK","CK","Throwin","Dribbling","Tackles","Clearances","Intercepts","Offsides","YellowCards","RedCards","30mLineEntries","PenaltyAreaEntries","Attacks","ChanceBuildingRate","Possession"]


            df[""] = new_index
            df = df.set_index("")

            try:
                df.at["DistanceCovered",f"{home}"] = df.at["DistanceCovered",f"{home}"].replace("m","").replace(",","")
                df.at["DistanceCovered",f"{away}"] = df.at["DistanceCovered",f"{away}"].replace("m","").replace(",","")
            except KeyError:
                pass

            df.at["ChanceBuildingRate",f"{home}"] = df.at["ChanceBuildingRate",f"{home}"].replace("%","")
            df.at["ChanceBuildingRate",f"{away}"] = df.at["ChanceBuildingRate",f"{away}"].replace("%","")


            df.at["Possession",f"{home}"] = df.at["Possession",f"{home}"].replace("%","")
            df.at["Possession",f"{away}"] = df.at["Possession",f"{away}"].replace("%","")
            
        except ValueError:
            print(f"ID : {match_id} ,URL : {url}")
        
        df.to_csv(f"./stats/{year}/{match_id}.csv")
        
        time.sleep(1)
            
    
    
def main():
    for year in range(2012,2022):
        scrape(year)
        
if __name__ == '__main__':
    main()
