import re
import os
import csv
import glob
import numpy as np
import pandas as pd
from datetime import timedelta

def get_points_and_gd(year,clubs):
    df_match = pd.read_csv(f"./match_data_yearly/{year}.csv")
    df_match["Date"] =  pd.to_datetime(df_match["Date"])
    df_match.sort_values(['Date','Sec']).reset_index(drop=True)  
    
    date_index = pd.date_range(start=df_match.iloc[0]["Date"] , end=df_match.iloc[-1]["Date"]+timedelta(days=1), freq="D")
    
    df_points = pd.DataFrame(columns=clubs, index=date_index)
    df_points.iloc[0] = 0
    
    df_gd = pd.DataFrame(columns=clubs, index=date_index)
    df_gd.iloc[0] = 0

    
    for date in date_index[:-1]:
        next_date = date +timedelta(days=1)
        df_currentday_match = df_match[df_match["Date"] == date]

        for index, row in df_currentday_match.iterrows():
            # points
            current_home_point = df_points.at[date, row["Home"]]
            current_away_point = df_points.at[date, row["Away"]]

            if row["W/L"] == 0:
                next_home_point = current_home_point + 1
                next_away_point = current_away_point + 1
                df_points.at[next_date,row["Home"]] = next_home_point
                df_points.at[next_date,row["Away"]] = next_away_point

            elif row["W/L"] == 1:
                next_home_point = current_home_point + 3
                df_points.at[next_date,row["Home"]] = next_home_point
            else:
                next_away_point = current_away_point + 3
                df_points.at[next_date,row["Away"]] = next_away_point
                
            # goal_differences
            current_home_gd = df_gd.at[date, row["Home"]]
            current_away_gd = df_gd.at[date, row["Away"]]

            next_home_gd = current_home_gd + (row["HomeGF"] - row["AwayGF"])
            next_away_gd = current_away_gd + (row["AwayGF"] - row["HomeGF"])

            df_gd.at[next_date,row["Home"]] = next_home_gd
            df_gd.at[next_date,row["Away"]] = next_away_gd

        
        df_points.loc[next_date]=df_points.loc[next_date].fillna(df_points.loc[date])
        df_gd.loc[next_date]=df_gd.loc[next_date].fillna(df_gd.loc[date])
       
    df_points.to_csv(f"./points/{year}.csv", index_label="date")
    df_gd.to_csv(f"./goal_differences/{year}.csv", index_label="date")
    
#     df_rank = df_points.rank(axis=1,method='min',ascending=False).astype(int)  
#     df_rank.to_csv(f"./points_rank/{year}.csv", index_label="date")

def create_allyears_points():
    csvs= glob.glob("./points/20*.csv")
    df_points_allyears=pd.DataFrame()
    for csv in csvs:
        df_points_allyears = df_points_allyears.append(pd.read_csv(csv, index_col=0, parse_dates=True))
    df_points_allyears=df_points_allyears.sort_index()
    df_points_allyears=df_points_allyears.fillna(0).astype(int)
    
    df_points_allyears.to_csv("./points/all_years.csv")
    
    

def create_allyears_gd():
    csvs= glob.glob("./goal_differences/20*.csv")
    df_gd_allyears=pd.DataFrame()
    for csv in csvs:
        df_gd_allyears = df_gd_allyears.append(pd.read_csv(csv, index_col=0, parse_dates=True))
    df_gd_allyears=df_gd_allyears.sort_index()
    df_gd_allyears=df_gd_allyears.fillna(0).astype(int)
    
    df_gd_allyears.to_csv("./goal_differences/all_years.csv")
    
    
        

def main():
    clubs_2006 = [
        'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka', 'sanfrecce-hiroshima',  'jubilo-iwata',  'cerezo-osaka', 
         'kawasaki-frontale', 'fc-tokyo', 'avispa-fukuoka', 'kyoto-sanga', 
         'omiya-ardija', 'ventforet-kofu',  'oita-trinita','albirex-niigata'
    ]

    clubs_2007 = [
        'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka', 'sanfrecce-hiroshima',  'jubilo-iwata',  
         'kawasaki-frontale', 'fc-tokyo',   
         'omiya-ardija', 'ventforet-kofu',  'oita-trinita','albirex-niigata',
        'vissel-kobe','kashiwa-reysol','yokohama-fc',
    ]

    clubs_2008 = [
        'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka',  'jubilo-iwata',  
         'kawasaki-frontale', 'fc-tokyo',   
         'omiya-ardija',   'oita-trinita','albirex-niigata',
        'vissel-kobe','kashiwa-reysol',
         'consadole-sapporo',  'tokyo-verdy','kyoto-sanga',
    ]

    clubs_2009 = [
        'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka',  'jubilo-iwata',  
         'kawasaki-frontale', 'fc-tokyo',   
         'omiya-ardija',   'oita-trinita','albirex-niigata',
        'vissel-kobe','kashiwa-reysol',
         'kyoto-sanga','sanfrecce-hiroshima', 'montedio-yamagata',
    ]

    clubs_2010 = [
        'kashima-antlers',  'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka',  'jubilo-iwata',  
         'kawasaki-frontale', 'fc-tokyo',   
         'omiya-ardija',   'albirex-niigata',
        'vissel-kobe',
         'kyoto-sanga','sanfrecce-hiroshima', 'montedio-yamagata',
         'vegalta-sendai', 'cerezo-osaka', 'shonan-bellmare',
    ]

    clubs_2011 = [
        'kashima-antlers',  'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka',  'jubilo-iwata',  
         'kawasaki-frontale',    
         'omiya-ardija',   'albirex-niigata',
        'vissel-kobe',
         'sanfrecce-hiroshima', 'montedio-yamagata',
         'vegalta-sendai', 'cerezo-osaka',
         'kashiwa-reysol', 'ventforet-kofu', 'avispa-fukuoka',
    ]

    clubs_2012 = [
        'kashima-antlers',  'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'gamba-osaka',  'jubilo-iwata',  'kawasaki-frontale',    
         'omiya-ardija',   'albirex-niigata','vissel-kobe',
         'sanfrecce-hiroshima', 'vegalta-sendai', 'cerezo-osaka',
         'kashiwa-reysol',  'fc-tokyo', 'sagan-tosu', 'consadole-sapporo',
    ]

    clubs_2013 = [
        'kashima-antlers',  'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
        'jubilo-iwata',  'kawasaki-frontale',    
         'omiya-ardija',   'albirex-niigata',
         'sanfrecce-hiroshima', 'vegalta-sendai', 'cerezo-osaka',
         'kashiwa-reysol',  'fc-tokyo', 'sagan-tosu', 
         'ventforet-kofu', 'shonan-bellmare', 'oita-trinita',
    ]

    clubs_2014 = [
        'kashima-antlers',  'urawa-red-diamonds', 
         'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
         'kawasaki-frontale',    
         'omiya-ardija',   'albirex-niigata',
         'sanfrecce-hiroshima', 'vegalta-sendai', 'cerezo-osaka',
         'kashiwa-reysol',  'fc-tokyo', 'sagan-tosu', 
         'ventforet-kofu',   'gamba-osaka', 'vissel-kobe', 'tokushima-vortis',
    ]

    clubs_2015 = [
        'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
        'shimizu-s-pulse', 'nagoya-grampus-eight', 'kawasaki-frontale',
        'albirex-niigata','sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
        'fc-tokyo', 'sagan-tosu', 'ventforet-kofu', 'gamba-osaka', 
        'vissel-kobe', 'shonan-bellmare', 'matsumoto-yamaga', 'montedio-yamagata',
    ]

    clubs_2016 = [
        'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
        'nagoya-grampus-eight', 'kawasaki-frontale',
        'albirex-niigata','sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
        'fc-tokyo', 'sagan-tosu', 'ventforet-kofu', 'gamba-osaka', 
        'vissel-kobe', 'shonan-bellmare', 
        'omiya-ardija', 'jubilo-iwata', 'avispa-fukuoka',
    ]

    clubs_2017 = [
        'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
         'kawasaki-frontale',
        'albirex-niigata','sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
        'fc-tokyo', 'sagan-tosu', 'ventforet-kofu', 'gamba-osaka', 
        'vissel-kobe','omiya-ardija', 'jubilo-iwata', 
         'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
    ]

    clubs_2018 = [
        'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
         'kawasaki-frontale',
        'sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
        'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 
        'vissel-kobe', 'jubilo-iwata', 
         'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
         'shonan-bellmare', 'v-varen-nagasaki', 'nagoya-grampus-eight',
    ]

    clubs_2019 = [
        'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
         'kawasaki-frontale',
        'sanfrecce-hiroshima', 'vegalta-sendai',
        'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 
        'vissel-kobe', 'jubilo-iwata', 
         'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
         'shonan-bellmare',  'nagoya-grampus-eight',
         'matsumoto-yamaga', 'oita-trinita',
    ]

    clubs_2020 = [
        'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
         'kawasaki-frontale','sanfrecce-hiroshima', 'vegalta-sendai',
        'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 'vissel-kobe', 
         'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
         'shonan-bellmare',  'nagoya-grampus-eight',
          'oita-trinita', 'kashiwa-reysol', 'yokohama-fc',
    ]
    for year,clubs in zip(range(2006,2021),[clubs_2006,clubs_2007,clubs_2008,clubs_2009,clubs_2010,clubs_2011,clubs_2012,clubs_2013,clubs_2014,clubs_2015,clubs_2016,clubs_2017,clubs_2018,clubs_2019,clubs_2020]):
        get_points_and_gd(year,clubs)
    create_allyears_points()
    create_allyears_gd()
    
if __name__ == '__main__':
    main()
    
    
  