import csv
import pandas as pd
import numpy as np

df = pd.read_csv("./match_data_yearly/all_years.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index(df["Date"])
df = df["2012":]

columns_df_stats = ['HomeShots', 'HomeShotsOnTarget', 'HomeShotsFromPK', 'HomePasses','HomeCrosses','HomeDirectFK', 'HomeIndirectFK', 'HomeCK', 'HomeThrowin', 'HomeDribbling', 'HomeTackles', 'HomeClearances', 'HomeIntercepts', 'HomeOffsides', 'HomeYellowCards', 'HomeRedCards','Home30mLineEntries', 'HomePenaltyAreaEntries', 'HomeAttacks', 'HomeChanceBuildingRate','HomePossession','AwayShots', 'AwayShotsOnTarget', 'AwayShotsFromPK', 'AwayPasses', 'AwayCrosses','AwayDirectFK', 'AwayIndirectFK', 'AwayCK', 'AwayThrowin', 'AwayDribbling', 'AwayTackles','AwayClearances', 'AwayIntercepts', 'AwayOffsides', 'AwayYellowCards', 'AwayRedCards','Away30mLineEntries', 'AwayPenaltyAreaEntries', 'AwayAttacks','AwayChanceBuildingRate','AwayPossession']

df_home_stats = pd.DataFrame()
df_away_stats = pd.DataFrame()

for index,row in df.iterrows():
    #Home
    home_stats = pd.read_csv(f"./stats/{row['Year']}/{row['ID']}.csv",index_col=0)[f"{row['Home']}"]
    df_home_stats = pd.concat([df_home_stats, home_stats], axis = 1)
    #Away
    away_stats = pd.read_csv(f"./stats/{row['Year']}/{row['ID']}.csv",index_col=0)[f"{row['Away']}"]
    df_away_stats = pd.concat([df_away_stats, away_stats], axis = 1)
    
df_home_stats=df_home_stats.drop(['DistanceCovered','Sprints','ExpG'])
df_away_stats=df_away_stats.drop(['DistanceCovered','Sprints','ExpG'])

df_home_stats = df_home_stats.T
df_away_stats = df_away_stats.T

df_home_stats.index = df["ID"].values
df_away_stats.index = df["ID"].values

df_stats = pd.concat([df_home_stats,df_away_stats], axis=1)
df_stats.columns = columns_df_stats

df_stats.to_csv("./stats.csv", index=True)
    