import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

def write_data(team_id):
    df = pd.read_csv(f"./match_data/{team_id}/{team_id}_2020.csv")
    
    dfH_train = df[(df["H/A"]==0) & (df["節"] <= 25) ].mean()
    Hs = dfH_train["得点"]
    Hg = dfH_train["失点"]
    
    dfA_train = df[(df["H/A"]==1) & (df["節"] <= 25) ].mean()
    As = dfA_train["得点"]
    Ag = dfA_train["失点"]
    
    with open('./match_data/results_1to25.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([team_id, Hs, Hg, As, Ag])
        
        
def main():
    for team_id in ('sapp','send','kasm','uraw','kasw','fctk',"ka-f","y-fm",'y-fc','shon','shim','nago','g-os','c-os','kobe','hiro','tosu','oita'):
        write_data(team_id)


if __name__ == '__main__':
    main()
