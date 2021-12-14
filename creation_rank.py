import re
import os
import csv
import glob
import numpy as np
import pandas as pd
from datetime import timedelta


def create_rank(year,clubs):
    df_match = pd.read_csv(f"./match_data_yearly/{year}.csv")
    df_match["Date"] =  pd.to_datetime(df_match["Date"])
    df_match.sort_values(['Date','Sec']).reset_index(drop=True)    
    
    date_index = pd.date_range(start=df_match.iloc[0]["Date"] , end=df_match.iloc[-1]["Date"]+timedelta(days=1), freq="D")

    df_points = pd.read_csv(f"./points/{year}.csv",parse_dates=[0],index_col=0)
    df_gd = pd.read_csv(f"./goal_differences/{year}.csv",parse_dates=[0], index_col=0)
    
    df_rank = pd.DataFrame(columns=clubs, index=date_index)

    for index,row in df_rank.iterrows():

        current_points_gd = pd.DataFrame(index=clubs, columns=["Points","GD"]) 
        current_points_gd["Points"] = df_points.loc[index].values
        current_points_gd["GD"] = df_gd.loc[index].values
        current_points_gd=current_points_gd.sort_values(["Points","GD"], ascending=False)

        current_ranks = []
        tie_count = 1
        rank = 0
        prev_row = None
        for i, r in current_points_gd.iterrows():
            if tuple(r) != prev_row:
                rank += tie_count
                tie_count = 1
            else:
                tie_count += 1

            current_ranks.append(rank)
            prev_row = tuple(r)


        current_points_gd['Rank'] = current_ranks
        df_rank.loc[index] = current_points_gd['Rank']
    
    df_rank.to_csv(f"./ranks/{year}.csv")
    
def create_allyears_ranks():
    csvs= glob.glob("./ranks/20*.csv")
    df_ranks_allyears=pd.DataFrame()
    for csv in csvs:
        df_ranks_allyears = df_ranks_allyears.append(pd.read_csv(csv, index_col=0, parse_dates=True))
    df_ranks_allyears=df_ranks_allyears.sort_index()
    df_ranks_allyears=df_ranks_allyears.fillna(19).astype(int)
    
    df_ranks_allyears.to_csv("./ranks/all_years.csv")
        
    
def main ():
    
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

    for year,clubs in zip(range(2006,2021), [clubs_2006,clubs_2007,clubs_2008,clubs_2009,clubs_2010,clubs_2011,clubs_2012,clubs_2013,clubs_2014,clubs_2015,clubs_2016,clubs_2017,clubs_2018,clubs_2019,clubs_2020]):
        create_rank(year,clubs)
        
    create_allyears_ranks()
        
    
if __name__ == '__main__':
    main()
    
    
        
        