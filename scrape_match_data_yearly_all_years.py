import re
import csv
import os
import glob
import datetime
import numpy as np
import pandas as pd


csvs = glob.glob('./match_data_yearly/20*.csv')
df = pd.DataFrame()
for csv in csvs:
    df = df.append(pd.read_csv(csv))
df = df.sort_values(['Date','Sec']).reset_index(drop=True) 

df["ID"] = df["ID"].astype(str)
for index,row in df.iterrows():
    df.at[index,"ID"]  = str(row["ID"]).zfill(8)
    
df.to_csv("./match_data_yearly/all_years.csv",index=False)
