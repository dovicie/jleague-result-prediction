import numpy as np
import pandas as pd
from scipy.stats import poisson
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier 

def predict_with_randomforest(match_id):
    df_allmatch = pd.read_csv("./match_data_yearly/all_years.csv")
    df_allmatch["Date"] = pd.to_datetime(df_allmatch["Date"])
    df_allmatch.set_index("ID",inplace=True)
    df_allmatch.sort_index(inplace=True)
    
    df_recent_stats = pd.read_csv("./recent_stats.csv", index_col=0)
    df_recent_stats.fillna({
        'HomeShots':10, 'HomeShotsOnTarget':3, 'HomeShotsFromPK':0.2, 'HomePasses':400,
        'HomeCrosses':16, 'HomeDirectFK':10, 'HomeIndirectFK':2, 'HomeCK':4,
        'HomeThrowin':20, 'HomeDribbling':10, 'HomeTackles':18, 'HomeClearances':23,
        'HomeIntercepts':2, 'HomeOffsides':1.5, 'HomeYellowCards':1, 'HomeRedCards':0,
        'Home30mLineEntries':33, 'HomePenaltyAreaEntries':9, 'HomeAttacks':117,
        'HomeChanceBuildingRate':10, 'HomePossession':44,
        'AwayShots':10, 'AwayShotsOnTarget':3, 'AwayShotsFromPK':0.2, 'AwayPasses':400,
        'AwayCrosses':16, 'AwayDirectFK':10, 'AwayIndirectFK':2, 'AwayCK':4,
        'AwayThrowin':20, 'AwayDribbling':10, 'AwayTackles':18, 'AwayClearances':23,
        'AwayIntercepts':2, 'AwayOffsides':1.5, 'AwayYellowCards':1, 'AwayRedCards':0,
        'Away30mLineEntries':33, 'AwayPenaltyAreaEntries':9, 'AwayAttacks':117,
        'AwayChanceBuildingRate':10, 'AwayPossession':44
    }, inplace=True)
    df_recent_stats.sort_index(inplace=True)
    
    df = pd.concat([df_allmatch,df_recent_stats], axis=1)
    items = [
        'Rate','RD','Shots', 'ShotsOnTarget', 'ShotsFromPK','Passes', 'Crosses', 'DirectFK', 
        'IndirectFK', 'CK','Throwin', 'Dribbling', 'Tackles', 'Clearances','Intercepts', 'Offsides', 
        'YellowCards', 'RedCards','30mLineEntries', 'PenaltyAreaEntries', 'Attacks', 'Possession'
    ]
    
    for item in items:
        df.insert(len(df.columns), f"{item}Diff", df[f"Home{item}"]-df[f"Away{item}"])
    
    match = df[df.index==match_id]
    match_year = match.at[match_id,"Year"]
    df_past = df[
        ((match.at[match_id,"Date"] - relativedelta(years=3)) <= df["Date"]) & 
        (df["Date"] < match.at[match_id,"Date"])
    ]
    
    X_train=df_past[[
        'Sec', 'Attendances', 'HomeRate', 'AwayRate',
        'HomeRD', 'AwayRD', 'HomeShots', 'HomeShotsOnTarget', 'HomeShotsFromPK',
        'HomePasses', 'HomeCrosses', 'HomeDirectFK', 'HomeIndirectFK', 'HomeCK',
        'HomeThrowin', 'HomeDribbling', 'HomeTackles', 'HomeClearances',
        'HomeIntercepts', 'HomeOffsides', 'HomeYellowCards', 'HomeRedCards',
        'Home30mLineEntries', 'HomePenaltyAreaEntries', 'HomeAttacks',
        'HomeChanceBuildingRate', 'HomePossession', 'AwayShots',
        'AwayShotsOnTarget', 'AwayShotsFromPK', 'AwayPasses', 'AwayCrosses',
        'AwayDirectFK', 'AwayIndirectFK', 'AwayCK', 'AwayThrowin',
        'AwayDribbling', 'AwayTackles', 'AwayClearances', 'AwayIntercepts',
        'AwayOffsides', 'AwayYellowCards', 'AwayRedCards', 'Away30mLineEntries',
        'AwayPenaltyAreaEntries', 'AwayAttacks', 'AwayChanceBuildingRate',
        'AwayPossession','RateDiff', 'RDDiff', 'ShotsDiff',
        'ShotsOnTargetDiff', 'ShotsFromPKDiff', 'PassesDiff', 'CrossesDiff',
        'DirectFKDiff', 'IndirectFKDiff', 'CKDiff', 'ThrowinDiff',
        'DribblingDiff', 'TacklesDiff', 'ClearancesDiff', 'InterceptsDiff',
        'OffsidesDiff', 'YellowCardsDiff', 'RedCardsDiff', '30mLineEntriesDiff',
        'PenaltyAreaEntriesDiff', 'AttacksDiff', 'PossessionDiff'
    ]].values
    y_train = df_past["W/L"].values
    
    X_test = match[[
        'Sec', 'Attendances', 'HomeRate', 'AwayRate',
        'HomeRD', 'AwayRD', 'HomeShots', 'HomeShotsOnTarget', 'HomeShotsFromPK',
        'HomePasses', 'HomeCrosses', 'HomeDirectFK', 'HomeIndirectFK', 'HomeCK',
        'HomeThrowin', 'HomeDribbling', 'HomeTackles', 'HomeClearances',
        'HomeIntercepts', 'HomeOffsides', 'HomeYellowCards', 'HomeRedCards',
        'Home30mLineEntries', 'HomePenaltyAreaEntries', 'HomeAttacks',
        'HomeChanceBuildingRate', 'HomePossession', 'AwayShots',
        'AwayShotsOnTarget', 'AwayShotsFromPK', 'AwayPasses', 'AwayCrosses',
        'AwayDirectFK', 'AwayIndirectFK', 'AwayCK', 'AwayThrowin',
        'AwayDribbling', 'AwayTackles', 'AwayClearances', 'AwayIntercepts',
        'AwayOffsides', 'AwayYellowCards', 'AwayRedCards', 'Away30mLineEntries',
        'AwayPenaltyAreaEntries', 'AwayAttacks', 'AwayChanceBuildingRate',
        'AwayPossession','RateDiff', 'RDDiff', 'ShotsDiff',
        'ShotsOnTargetDiff', 'ShotsFromPKDiff', 'PassesDiff', 'CrossesDiff',
        'DirectFKDiff', 'IndirectFKDiff', 'CKDiff', 'ThrowinDiff',
        'DribblingDiff', 'TacklesDiff', 'ClearancesDiff', 'InterceptsDiff',
        'OffsidesDiff', 'YellowCardsDiff', 'RedCardsDiff', '30mLineEntriesDiff',
        'PenaltyAreaEntriesDiff', 'AttacksDiff', 'PossessionDiff'
    ]].values
    y_test = match["W/L"].values
    
    params = {'n_estimators': [30, 50, 100, 200, 300],'max_depth': [2, 3, 4, 5, 6, 7, 8 , 9,10]}
    clf = GridSearchCV(RandomForestClassifier(random_state=1234), params, cv=5, n_jobs=-1, verbose=1)
    clf.fit(X_train,y_train)
    
    return clf.predict_proba(X_test)[0]

def predict_with_poisson(match_id, match_range = 17):
    
    df_allmatch = pd.read_csv("./match_data_yearly/all_years.csv", index_col=0)
    df_allmatch["Date"] = pd.to_datetime(df_allmatch["Date"])

    current_day = df_allmatch.at[match_id,"Date"]
    home = df_allmatch.at[match_id,"Home"]
    away = df_allmatch.at[match_id,"Away"]
    
    df_recent_home = df_allmatch[
        (df_allmatch["Date"] < current_day) &
        ((current_day.year-1)<= df_allmatch["Year"]) &
        (df_allmatch["Home"] == home) 
    ].tail(match_range)

    if  (match_range- len(df_recent_home)) :
        for _ in range(match_range- len(df_recent_home)):
            df_recent_home = df_recent_home.append({'Date':(current_day-relativedelta(days=1)) ,'HomeGF': 0.99, 'AwayGF': 1.66}, ignore_index=True)

    df_recent_away = df_allmatch[
        (df_allmatch["Date"] < current_day) &
        ((current_day.year-1)<= df_allmatch["Year"]) &
        (df_allmatch["Away"] == away)
    ].tail(match_range)

    if  (match_range- len(df_recent_away)) :
        for _ in range(match_range- len(df_recent_away)):
            df_recent_away = df_recent_away.append(
                {'Date':(current_day-relativedelta(days=1)) ,'HomeGF': 1.83, 'AwayGF': 0.94}, ignore_index=True)

    beginning_day = min(df_recent_home.iloc[0,2],df_recent_away.iloc[0,2])

    df_recent = df_allmatch[
        (beginning_day <= df_allmatch["Date"] ) &
        (df_allmatch["Date"] < current_day) 
    ]

    homegf_ave = df_recent_home["HomeGF"].mean()
    homega_ave = df_recent_home["AwayGF"].mean()
    awaygf_ave = df_recent_away["AwayGF"].mean()
    awayga_ave = df_recent_away["HomeGF"].mean()
    homegf_league_ave = df_recent["HomeGF"].mean()
    awaygf_league_ave = df_recent["AwayGF"].mean()
    
    home_attack = homegf_ave / homegf_league_ave
    away_defense = awayga_ave / homegf_league_ave
    homegf_pred = home_attack * away_defense * homegf_league_ave

    away_attack = awaygf_ave / awaygf_league_ave
    home_defense = homega_ave / awaygf_league_ave
    awaygf_pred = away_attack * home_defense * awaygf_league_ave
    
    x =  np.arange(0, 10, 1)

    home_poisson = poisson.pmf(x, homegf_pred)
    away_poisson = poisson.pmf(x, awaygf_pred)

    df_poisson = pd.DataFrame([home_poisson,away_poisson],columns=x, index=[home,away])
    
    win_prob_sum = 0
    loss_prob_sum = 0
    draw_prob_sum = 0
    
    for gf in x:
        gf_prob = df_poisson.at[home, gf]
        for ga in x:
            ga_prob = df_poisson.at[away,ga]
            score_prob = gf_prob * ga_prob

            if gf>ga:
                win_prob_sum += score_prob
            elif gf<ga:
                loss_prob_sum += score_prob
            else:
                draw_prob_sum += score_prob

    prob_sum = win_prob_sum+loss_prob_sum+draw_prob_sum
    win_prob_sum = win_prob_sum/prob_sum
    loss_prob_sum = loss_prob_sum/prob_sum
    draw_prob_sum = draw_prob_sum/prob_sum

    return [draw_prob_sum,win_prob_sum,loss_prob_sum]


def predict_goalfor_with_poisson(match_id, match_range = 17):
    
    df_allmatch = pd.read_csv("./match_data_yearly/all_years.csv", index_col=0)
    df_allmatch["Date"] = pd.to_datetime(df_allmatch["Date"])
    
    current_day = df_allmatch.at[match_id,"Date"]
    home = df_allmatch.at[match_id,"Home"]
    away = df_allmatch.at[match_id,"Away"]
    
    df_recent_home = df_allmatch[
        (df_allmatch["Date"] < current_day) &
        ((current_day.year-1)<= df_allmatch["Year"]) &
        (df_allmatch["Home"] == home) 
    ].tail(match_range)

    if  (match_range- len(df_recent_home)) :
        for _ in range(match_range- len(df_recent_home)):
            df_recent_home = df_recent_home.append({'Date':(current_day-relativedelta(days=1)) , 'HomeGF': 0.99, 'AwayGF': 1.66}, ignore_index=True)

    df_recent_away = df_allmatch[
        (df_allmatch["Date"] < current_day) &
        ((current_day.year-1)<= df_allmatch["Year"]) &
        (df_allmatch["Away"] == away)
    ].tail(match_range)

    if  (match_range- len(df_recent_away)) :
        for _ in range(match_range- len(df_recent_away)):
            df_recent_away = df_recent_away.append({'Date':(current_day-relativedelta(days=1)) , 'HomeGF': 1.83, 'AwayGF': 0.94}, ignore_index=True)

    beginning_day = min(df_recent_home.iloc[0,2],df_recent_away.iloc[0,2])

    df_recent = df_allmatch[
        (beginning_day <= df_allmatch["Date"] ) &
        (df_allmatch["Date"] < current_day) 
    ]

    homegf_ave = df_recent_home["HomeGF"].mean()
    homega_ave = df_recent_home["AwayGF"].mean()
    awaygf_ave = df_recent_away["AwayGF"].mean()
    awayga_ave = df_recent_away["HomeGF"].mean()
    homegf_league_ave = df_recent["HomeGF"].mean()
    awaygf_league_ave = df_recent["AwayGF"].mean()
    
    home_attack = homegf_ave / homegf_league_ave
    away_defense = awayga_ave / homegf_league_ave
    homegf_pred = home_attack * away_defense * homegf_league_ave

    away_attack = awaygf_ave / awaygf_league_ave
    home_defense = homega_ave / awaygf_league_ave
    awaygf_pred = away_attack * home_defense * awaygf_league_ave
    
    x =  np.arange(0, 10, 1)
    
    home_poisson = poisson.pmf(x, homegf_pred)
    away_poisson = poisson.pmf(x, awaygf_pred)
    

    
    return [home_poisson.tolist(),away_poisson.tolist()]
