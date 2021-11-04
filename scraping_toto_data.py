import re
import csv
import time
import requests
import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


column_array=[["No","Group","Date","Winning","Match1","Match1","Match1","Match2","Match2","Match2","Match3","Match3","Match3","Match4","Match4","Match4","Match5","Match5","Match5"],["","","","","Home","Away","W/L","Home","Away","W/L","Home","Away","W/L","Home","Away","W/L","Home","Away","W/L"]]
column_tuples = list(zip(*column_array))
column = pd.MultiIndex.from_tuples(column_tuples)

club_id = pd.read_csv("./club_and_id.csv")

df_match_data_all = pd.read_csv("./match_data_yearly/all_years.csv")
df_match_data_all["Date"] = pd.to_datetime(df_match_data_all["Date"])
df_match_data_all =df_match_data_all.set_index(["Date"], drop=True)

# 対象外試合を含む回(ルヴァン,ナビスコ,天皇杯)
not_covered_nos = [439, 442, 451, 454, 518, 556, 559, 566, 570, 571, 575, 612, 613, 615, 617, 621, 626, 628, 634, 635, 651, 656, 661, 669, 671, 681, 684, 687, 695, 696, 697, 698, 707, 716, 719, 720, 726, 727, 735, 752, 754, 757, 760, 767, 769, 771, 791, 792, 799, 800, 805, 813, 816, 831, 832, 835, 839, 846, 848, 850, 869, 870, 875, 878, 879, 888, 899, 901, 914, 920, 924, 926, 928, 932, 934, 939, 945, 953, 955, 959, 962, 963, 967, 978, 990, 992, 997, 1001, 1007, 1009, 1026, 1037, 1040, 1041, 1044, 1047, 1048, 1050, 1057, 1074, 1076, 1083, 1087, 1091, 1095, 1100, 1102, 1104, 1112, 1118, 1119, 1122, 1127, 1129, 1132, 1144, 1155, 1177, 1179, 1184, 1194, 1225, 1231, 1235, 1238, 1243, 1244, 1255, 1260, 1263]

def scrape(year, first, final):
    df=pd.DataFrame(columns=column)
    
    for n in range(first,final):
        
        if (n in not_covered_nos):
            continue
            
        url =f'https://toto.rakuten.co.jp/toto/result/{n:04}/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            for group in ["A","B"]:
                date = soup.select(f"#minitotoBlock{group} .tbl-basic-day td")[0].string
                wining = soup.select(f"#minitotoBlock{group} .tbl-basic-money tbody td")[0].string
                toto_data = [n, group, date,wining]

                match = soup.select(f"#minitotoBlock{group} .tbl-result tbody tr")
                for i in range(5):
                    home_ja = match[i].select("td")[1].string
                    away_ja = match[i].select("td")[3].string

                    home = ""
                    away = ""

                    for index,row in club_id.iterrows():
                        if home_ja == row["club_ja"]:
                            home = row["club"]
                        elif away_ja == row["club_ja"]:
                            away = row["club"]

                    match_data =[home, away, int(match[i].select("td")[5].string)]
                    toto_data.extend(match_data)

                if not "" in toto_data:
                    df.loc[f"{n}_{group}"]= toto_data

        except IndexError:
            pass
        except ValueError:
            pass

        time.sleep(1)
        
        
    df["Date"] = df["Date"].replace('\(.+\)','',regex=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y年%m月%d日")
    
    df=df.set_index(["No","Group"], drop=True)
    
    df["Winning"]=df["Winning"].str.replace(",","")
    df["Winning"]=df["Winning"].str.replace("円","").astype(int)
    
    df.insert(2, ( 'Match1', 'MatchID'),np.nan)
    df.insert(6, ( 'Match2', 'MatchID'),np.nan)
    df.insert(10, ( 'Match3', 'MatchID'),np.nan)
    df.insert(14, ( 'Match4', 'MatchID'),np.nan)
    df.insert(18, ( 'Match5', 'MatchID'),np.nan)
    

    df_match_data = df_match_data_all[f"{year}"]
    
    for index,row in df.iterrows():
        for i in range(1,6):
            home = row[f"Match{i}"]["Home"]
            away = row[f"Match{i}"]["Away"]
            df[f"Match{i}","W/L"]=df[f"Match{i}","W/L"].astype(int)
            try:
                match_id = df_match_data[(df_match_data["Home"]==home) & (df_match_data["Away"] == away)]["ID"].values[0]
                df.at[index, (f"Match{i}","MatchID")] = match_id
            except IndexError:
                pass    
            
    df=df.dropna()
    
    pd.options.mode.chained_assignment = None # これを有効にすると､SettingWithCopyWarningをオフできる(非推奨)
    for i in range(1,6):
        df[f"Match{i}","MatchID"] = df[f"Match{i}","MatchID"].astype(int)

        
    df.to_csv(f"./toto_data/{year}.csv")
    
    
def main():
    args = [
        [2010,435,488],
        [2011,488,550],
        [2012,550,609],
        [2013,609,672],
        [2014,678,739],
        [2015,750,817],
        [2016,818,902],
        [2017,903,981],
        [2018,981,1064],
        [2019,1064,1147],
        [2020,1147,1214]
    ]
    
    for arg in args:
        scrape(arg[0], arg[1], arg[2])
        

if __name__ == '__main__':
    main()
    

    
        
        
        
        