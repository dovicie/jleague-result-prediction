import csv
import numpy as np
import pandas as pd
from scipy.stats import poisson
from dateutil.relativedelta import relativedelta

def write_data(year):

    df_allmatch = pd.read_csv("./match_data_yearly/all_years.csv", index_col=0)
    df_allmatch["Date"] = pd.to_datetime(df_allmatch["Date"])

    df_pred = pd.DataFrame(index=df_allmatch[df_allmatch["Year"] == year].index, columns=[0,1,2])

    for index, row in df_pred.iterrows():

        match_id=index
        date_range=6

        current_day = df_allmatch.at[match_id,"Date"]
        home = df_allmatch.at[match_id,"Home"]
        away = df_allmatch.at[match_id,"Away"]

        df_recent = df_allmatch[
            (current_day-relativedelta(months=date_range) < df_allmatch["Date"] ) &
            (df_allmatch["Date"] < current_day) 
        ]

        df_recent_home = df_recent[df_recent["Home"] == home]
        df_recent_away = df_recent[df_recent["Away"] == away]

        homegf_ave = df_recent_home["HomeGF"].mean()
        homega_ave = df_recent_home["AwayGF"].mean()
        awaygf_ave = df_recent_away["AwayGF"].mean()
        awayga_ave = df_recent_away["HomeGF"].mean()
        homegf_league_ave = df_recent["HomeGF"].mean()
        awaygf_league_ave = df_recent["AwayGF"].mean()

        # 欠損値処理
        # 10-20までのJ2降格チームのホームとアウェイ別での平均得点と平均失点(0.99,1.66,0.94,1.83)で穴埋め       
        if  homegf_ave is np.nan:
            homegf_ave = 0.99
        if homega_ave is np.nan:
            homega_ave = 1.66
        if awaygf_ave is np.nan:
            awaygf_ave = 0.94
        if awayga_ave is np.nan:
            awayga_ave = 1.83

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

        df_poisson.to_csv(f"./goal_for_predict_proba_poisson_distribution/csv/{year}/{index}.csv", float_format='%.18f')
        df_poisson.to_json(f"./goal_for_predict_proba_poisson_distribution/json/{year}/{index}.json", orient="index")


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

        row[0] = draw_prob_sum 
        row[1] = win_prob_sum
        row[2] = loss_prob_sum

    df_pred.to_csv(f"./predict_proba_poisson_distribution/csv/{year}.csv", float_format='%.18f')
    df_pred.to_json(f"./predict_proba_poisson_distribution/json/{year}.json", orient="index")
    
def main():
    for year in range(2006,2021):
        write_data(year)
        
if __name__ == '__main__':
    main()
