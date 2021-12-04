import csv
import numpy as np
import pandas as pd
from datetime import timedelta

def get_points_and_gd(year):
    df_match = pd.read_csv(f"./match_data_yearly/{year}.csv")
    df_match["Date"] =  pd.to_datetime(df_match["Date"])
    df_match.sort_values(['Date','Sec']).reset_index(drop=True)  
    
    clubs = ['kashima-antlers','jef-united','urawa-red-diamonds','tokyo-verdy','yokohama-fa-marinos','yokohama-flugels','shimizu-s-pulse','nagoya-grampus-eight','gamba-osaka','sanfrecce-hiroshima','kashiwa-reysol','shonan-bellmare','jubilo-iwata','consadole-sapporo','vissel-kobe','cerezo-osaka','kawasaki-frontale','fc-tokyo','avispa-fukuoka','kyoto-sanga','omiya-ardija','ventforet-kofu','montedio-yamagata','oita-trinita','sagan-tosu','yokohama-fc','tokushima-vortis','matsumoto-yamaga','v-varen-nagasaki','vegalta-sendai','albirex-niigata']
    
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
    
    df_rank = df_points.rank(axis=1,method='min',ascending=False).astype(int)  
    df_rank.to_csv(f"./points_rank/{year}.csv", index_label="date")

def main():
    for year in range(2006,2021):
        get_points_and_gd(year)
    
if __name__ == '__main__':
    main()
    
    
  