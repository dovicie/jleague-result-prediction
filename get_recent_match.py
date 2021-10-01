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

def get_ave_recent_stats(match_id):
    home = ""
    away = ""
    
    df = pd.read_csv("./match_data_yearly/all_years.csv")
    for index,row in df.iterrows():
        if row["ID"] == match_id:
            target_line = index 
            home = row["Home"]
            away = row["Away"]
            
    home_recent_stats = pd.DataFrame()
    away_recent_stats = pd.DataFrame()

    # Home
    for mid in get_recent_match_id(match_id)[0]:
        s = pd.read_csv(f"./stats/{mid}.csv", index_col=0)[home]
        home_recent_stats = pd.concat([home_recent_stats, s], axis = 1)
    home_ave_recent_stats = home_recent_stats.mean(axis=1)
    
    try:
        home_ave_recent_stats.drop("ExpG", inplace=True)
    except KeyError:
        pass
    try:
        home_ave_recent_stats.drop("Sprints", inplace=True)
    except KeyError:
        pass
    try:
        home_ave_recent_stats.drop("DistanceCovered", inplace=True)
    except KeyError:
        pass

    # Away
    for mid in get_recent_match_id(match_id)[1]:
        s = pd.read_csv(f"./stats/{mid}.csv", index_col=0)[away]
        away_recent_stats = pd.concat([away_recent_stats, s], axis = 1)     
    away_ave_recent_stats = away_recent_stats.mean(axis=1)
    
    try:
        away_ave_recent_stats.drop("ExpG", inplace=True)
    except KeyError:
        pass
    try:
        away_ave_recent_stats.drop("Sprints", inplace=True)
    except KeyError:
        pass
    try:
        away_ave_recent_stats.drop("DistanceCovered", inplace=True)
    except KeyError:
        pass

    return home_ave_recent_stats,away_ave_recent_stats
    
        
    
    