import csv
import pandas as pd
import numpy as np
import datetime as dt

from get_recent_match import get_ave_recent_stats, get_recent_match_id

df = pd.read_csv("./match_data_yearly/all_years.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index(df["Date"])
df = df["2010":]

columns_df_stats = ['HomeShots', 'HomeShotsOnTarget', 'HomeShotsFromPK', 'HomePasses','HomeCrosses','HomeDirectFK', 'HomeIndirectFK', 'HomeCK', 'HomeThrowin', 'HomeDribbling', 'HomeTackles', 'HomeClearances', 'HomeIntercepts', 'HomeOffsides', 'HomeYellowCards', 'HomeRedCards','Home30mLineEntries', 'HomePenaltyAreaEntries', 'HomeAttacks', 'HomeChanceBuildingRate','HomePossession','AwayShots', 'AwayShotsOnTarget', 'AwayShotsFromPK', 'AwayPasses', 'AwayCrosses','AwayDirectFK', 'AwayIndirectFK', 'AwayCK', 'AwayThrowin', 'AwayDribbling', 'AwayTackles','AwayClearances', 'AwayIntercepts', 'AwayOffsides', 'AwayYellowCards', 'AwayRedCards','Away30mLineEntries', 'AwayPenaltyAreaEntries', 'AwayAttacks','AwayChanceBuildingRate','AwayPossession']

df_home_stats = pd.DataFrame()
df_away_stats = pd.DataFrame()
for index,row in df.iterrows():
    
    #Home
    try:
        home_stats = get_ave_recent_stats(row["ID"])[0]
    except FileNotFoundError:
        home_stats = pd.Series(index=['Shots', 'ShotsOnTarget', 'ShotsFromPK', 'Passes', 'Crosses','DirectFK', 'IndirectFK', 'CK', 'Throwin', 'Dribbling', 'Tackles','Clearances', 'Intercepts', 'Offsides', 'YellowCards', 'RedCards','30mLineEntries', 'PenaltyAreaEntries', 'Attacks', 'ChanceBuildingRate','Possession'], dtype='float64')
    df_home_stats = pd.concat([df_home_stats, home_stats], axis=1)
    
    #Away
    try:
        away_stats = get_ave_recent_stats(row["ID"])[1]
    except FileNotFoundError:
        away_stats = pd.Series(index=['Shots', 'ShotsOnTarget', 'ShotsFromPK', 'Passes', 'Crosses','DirectFK', 'IndirectFK', 'CK', 'Throwin', 'Dribbling', 'Tackles','Clearances', 'Intercepts', 'Offsides', 'YellowCards', 'RedCards','30mLineEntries', 'PenaltyAreaEntries', 'Attacks', 'ChanceBuildingRate','Possession'], dtype='float64')
    df_away_stats = pd.concat([df_away_stats, away_stats], axis=1)
    
df_home_stats = df_home_stats.T
df_away_stats = df_away_stats.T

df_home_stats.index = df["ID"].values
df_away_stats.index =  df["ID"].values

df_stats = pd.concat([df_home_stats,df_away_stats], axis=1)
df_stats.columns = columns_df_stats

df_stats.to_csv("./recent_stats.csv", index=True)