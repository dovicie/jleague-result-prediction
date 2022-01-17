import re
import csv
import os
import glob
import numpy as np
import pandas as pd
from datetime import timedelta

def calculate_rate(home_rate,away_rate,g):
    k=16
    e = 1 /(1+pow(10, (away_rate-home_rate)/400) )
    home_rate =  home_rate+k*(g-e) 
    away_rate = away_rate+k*(abs(g-1)-(1-e))
    return home_rate,away_rate


def calculate_g(n):
    g=0
    if n == 1:
        g=1
    elif n == 0:
        g=0.5
    else:
        g=0        
    return g 

def create_rating():

    j1clubs = [
        [
            'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
             'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
             'gamba-osaka', 'sanfrecce-hiroshima',  'jubilo-iwata',  'cerezo-osaka', 
             'kawasaki-frontale', 'fc-tokyo', 'avispa-fukuoka', 'kyoto-sanga', 
             'omiya-ardija', 'ventforet-kofu',  'oita-trinita','albirex-niigata'
        ],[
            'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
            'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
            'gamba-osaka', 'sanfrecce-hiroshima',  'jubilo-iwata',  
            'kawasaki-frontale', 'fc-tokyo',   
            'omiya-ardija', 'ventforet-kofu',  'oita-trinita','albirex-niigata',
            'vissel-kobe','kashiwa-reysol','yokohama-fc',
        ],[
            'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
            'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
            'gamba-osaka',  'jubilo-iwata',  
            'kawasaki-frontale', 'fc-tokyo',   
            'omiya-ardija',   'oita-trinita','albirex-niigata',
            'vissel-kobe','kashiwa-reysol',
            'consadole-sapporo',  'tokyo-verdy','kyoto-sanga',
        ],[
            'kashima-antlers', 'jef-united', 'urawa-red-diamonds', 
             'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
             'gamba-osaka',  'jubilo-iwata',  
             'kawasaki-frontale', 'fc-tokyo',   
             'omiya-ardija',   'oita-trinita','albirex-niigata',
            'vissel-kobe','kashiwa-reysol',
             'kyoto-sanga','sanfrecce-hiroshima', 'montedio-yamagata',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 
            'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
            'gamba-osaka',  'jubilo-iwata',  
            'kawasaki-frontale', 'fc-tokyo',   
            'omiya-ardija',   'albirex-niigata',
            'vissel-kobe',
            'kyoto-sanga','sanfrecce-hiroshima', 'montedio-yamagata',
            'vegalta-sendai', 'cerezo-osaka', 'shonan-bellmare',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 
            'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
            'gamba-osaka',  'jubilo-iwata',  
            'kawasaki-frontale',    
            'omiya-ardija',   'albirex-niigata',
            'vissel-kobe',
            'sanfrecce-hiroshima', 'montedio-yamagata',
            'vegalta-sendai', 'cerezo-osaka',
            'kashiwa-reysol', 'ventforet-kofu', 'avispa-fukuoka',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 
             'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
             'gamba-osaka',  'jubilo-iwata',  'kawasaki-frontale',    
             'omiya-ardija',   'albirex-niigata','vissel-kobe',
             'sanfrecce-hiroshima', 'vegalta-sendai', 'cerezo-osaka',
             'kashiwa-reysol',  'fc-tokyo', 'sagan-tosu', 'consadole-sapporo',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 
            'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
            'jubilo-iwata',  'kawasaki-frontale',    
            'omiya-ardija',   'albirex-niigata',
            'sanfrecce-hiroshima', 'vegalta-sendai', 'cerezo-osaka',
            'kashiwa-reysol',  'fc-tokyo', 'sagan-tosu', 
            'ventforet-kofu', 'shonan-bellmare', 'oita-trinita',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 
            'yokohama-fa-marinos', 'shimizu-s-pulse', 'nagoya-grampus-eight', 
            'kawasaki-frontale',    
            'omiya-ardija',   'albirex-niigata',
            'sanfrecce-hiroshima', 'vegalta-sendai', 'cerezo-osaka',
            'kashiwa-reysol',  'fc-tokyo', 'sagan-tosu', 
            'ventforet-kofu',   'gamba-osaka', 'vissel-kobe', 'tokushima-vortis',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'shimizu-s-pulse', 'nagoya-grampus-eight', 'kawasaki-frontale',
            'albirex-niigata','sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
            'fc-tokyo', 'sagan-tosu', 'ventforet-kofu', 'gamba-osaka', 
            'vissel-kobe', 'shonan-bellmare', 'matsumoto-yamaga', 'montedio-yamagata',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'nagoya-grampus-eight', 'kawasaki-frontale',
            'albirex-niigata','sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
            'fc-tokyo', 'sagan-tosu', 'ventforet-kofu', 'gamba-osaka', 
            'vissel-kobe', 'shonan-bellmare', 
            'omiya-ardija', 'jubilo-iwata', 'avispa-fukuoka',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'kawasaki-frontale',
            'albirex-niigata','sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
            'fc-tokyo', 'sagan-tosu', 'ventforet-kofu', 'gamba-osaka', 
            'vissel-kobe','omiya-ardija', 'jubilo-iwata', 
            'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'kawasaki-frontale',
            'sanfrecce-hiroshima', 'vegalta-sendai','kashiwa-reysol',
            'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 
            'vissel-kobe', 'jubilo-iwata', 
            'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
            'shonan-bellmare', 'v-varen-nagasaki', 'nagoya-grampus-eight',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'kawasaki-frontale',
            'sanfrecce-hiroshima', 'vegalta-sendai',
            'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 
            'vissel-kobe', 'jubilo-iwata', 
            'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
            'shonan-bellmare',  'nagoya-grampus-eight',
            'matsumoto-yamaga', 'oita-trinita',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'kawasaki-frontale','sanfrecce-hiroshima', 'vegalta-sendai',
            'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 'vissel-kobe', 
            'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
            'shonan-bellmare',  'nagoya-grampus-eight',
            'oita-trinita', 'kashiwa-reysol', 'yokohama-fc',
        ],[
            'kashima-antlers',  'urawa-red-diamonds', 'yokohama-fa-marinos',
            'kawasaki-frontale','sanfrecce-hiroshima', 'vegalta-sendai',
            'fc-tokyo', 'sagan-tosu',  'gamba-osaka', 'vissel-kobe', 
            'consadole-sapporo', 'shimizu-s-pulse', 'cerezo-osaka',
            'shonan-bellmare',  'nagoya-grampus-eight','oita-trinita', 
            'kashiwa-reysol', 'yokohama-fc','tokushima-vortis','avispa-fukuoka',
        ]
    ]
    
    df_clubs = pd.read_csv("./clubs.csv",index_col=0)
    final_rates=None
    
    for year,clubs in zip(range(2006,2022),j1clubs):
        try:
            prev_clubs = df_clubs.loc[year+1].tolist()
        except KeyError:
            pass

        df_match = pd.read_csv(f"./match_data_yearly/{year}.csv", index_col=0)
        df_match["Date"] = pd.to_datetime(df_match["Date"])
        df_match = df_match.sort_values(["Date","Sec"])

        date_index = pd.date_range(start=df_match.iloc[0]["Date"] , end=df_match.iloc[-1]["Date"]+timedelta(days=1), freq="D")

        df_elo = pd.DataFrame(columns=clubs, index=date_index)
        
        if year == 2006:
            df_elo.iloc[0] = 1500
        else:
            df_elo.iloc[0] = final_rates
            df_elo.iloc[0] = df_elo.iloc[0].fillna(relegation_rate)

        for current_date in date_index[:-1]:
            prev_date = current_date+timedelta(days=1)
            df_current_date = df_match[df_match["Date"] == current_date]
            for i,r in df_current_date.iterrows():
                home_rate = df_elo.loc[current_date, r["Home"]]
                away_rate = df_elo.loc[current_date, r["Away"]]
                g = calculate_g(r["W/L"])

                prev_home_rate, prev_away_rate = calculate_rate(home_rate,away_rate,g)

                df_elo.at[prev_date,r["Home"]] = prev_home_rate
                df_elo.at[prev_date,r["Away"]] = prev_away_rate

            df_elo.loc[prev_date] = df_elo.loc[prev_date].fillna(df_elo.loc[current_date])

        final_rates = df_elo.iloc[-1]
        
        relegated_clubs = list(set(clubs) - set(prev_clubs))
        relegation_rate = final_rates.loc[relegated_clubs].mean()
        
        if np.isnan(relegation_rate):
            relegation_rate = 1400

        
        df_elo.astype(int).to_csv(f"./rating/{year}.csv")
        
def create_allyears_rating():
    csvs = glob.glob('./rating/20*.csv')

    df_rate_allyears = pd.DataFrame()
    for csv in csvs:
        df_rate_allyears = df_rate_allyears.append(pd.read_csv(csv, index_col=0,parse_dates=True))
        
    df_rate_allyears = df_rate_allyears.sort_index()
    df_rate_allyears.iloc[0] = df_rate_allyears.iloc[0].fillna(1350)
    df_rate_allyears =df_rate_allyears.interpolate(limit_direction='both').astype(int)
    df_rate_allyears.to_csv("./rating/all_years.csv")
    
def main ():
    create_rating()
    create_allyears_rating()
        
        
    
if __name__ == '__main__':
    main()
    