import pandas as pd

def get_recent_match_id(match_id):
    df = pd.read_csv("./match_data_yearly/all_years.csv")
    df.sort_values("Date",ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    match_id = match_id
    target_line = 0

    home = ""
    home_recent_matches = []

    away = ""
    away_recent_matches = []


    for index,row in df.iterrows():
        if row["ID"] == match_id:
            target_line = index 
            home = row["Home"]
            away = row["Away"]


    for i ,r in df[target_line+1:target_line+300:].iterrows():
        if home == r["Home"] or home == r["Away"]:
            home_recent_matches.append(r["ID"])
            if len(home_recent_matches) == 5:
                break

    for i ,r in df[target_line+1:target_line+300:].iterrows():
        if away == r["Home"] or away == r["Away"]:
            away_recent_matches.append(r["ID"])
            if len(away_recent_matches) == 5:
                break

    
    return home_recent_matches, away_recent_matches