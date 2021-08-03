import re
import csv
import os
import glob
import datetime
import numpy as np
import pandas as pd

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

def write_data():
    csvs = glob.glob('./match_data_yearly/*.csv')
#     df_match = pd.DataFrame()
#     for csv in csvs:
#         df_match = df_match.append(pd.read_csv(csv))
    df_match = pd.read_csv("./match_data_yearly/all_years.csv")
    df_match = df_match.sort_values(['Date','Sec']).reset_index(drop=True)    

    df_club = pd.read_csv("./club_and_id.csv")
    clubs = list(df_club["club"])[:-1:]
    initial_rates = [1500,1500,1500,1380,1500,1380,1500,1500,1500,1500,1380,1380,1500,1380,1380,1500,1500,1500,1500,1500,1500,1500,1380,1500,1380,1380,1380,1380,1380,1380,1500]

    date_index = pd.date_range(start="2006-02-04", end="2020-12-20", freq="D")
    df_elo=pd.DataFrame(columns=clubs,index = date_index )
    df_elo.loc["2006-02-04"] = initial_rates

    df_match["Date"] =  pd.to_datetime(df_match["Date"])

    for date in date_index[:-1]:
        next_date = date+pd.tseries.offsets.Day()

        df_date_match = df_match[df_match["Date"] == date]    
        for index,row in df_date_match.iterrows():

            home_rate= df_elo.loc[date ,row["Home"]]
            away_rate= df_elo.loc[date ,row["Away"]]
            g = calculate_g(row["W/L"])

            home_rate_upd,away_rate_upd = calculate_rate(home_rate, away_rate, g)

            df_elo.at[next_date, row["Home"]] = home_rate_upd
            df_elo.at[next_date, row["Away"]] = away_rate_upd
            
        df_elo.loc[next_date]=df_elo.loc[next_date].fillna(df_elo.loc[date])
    
    df_elo.to_csv('./elorating.csv', index_label="date")
    

def main():
    write_data()
    
if __name__ == '__main__':
    main()
    