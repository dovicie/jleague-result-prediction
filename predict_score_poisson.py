from scipy.stats import poisson
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

def predict_score(home,away):
    
    df_AD = pd.read_csv("./match_data/HaHdAaAd.csv").set_index("team")
    df_1_25 = pd.read_csv("./match_data/results_1to25.csv")
    df_26_34 = pd.read_csv("./match_data/match_26to34.csv")

    aveHs = result1_25["Hs"].mean()
    hscores = df.at[home,"HA"] * df.at[away,"AD"] * aveHs

    aveAg = df_1_25["Ag"].mean()
    ascores = df_AD.at["shim","HD"] * df_AD.at["kobe","AA"] * aveAg

    prediction_hs = np.argmax(poisson.pmf(k=x, mu=hscores))
    prediction_as =  np.argmax(poisson.pmf(k=x, mu=ascores))
    
    
def get_match():
    