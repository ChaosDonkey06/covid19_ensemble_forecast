from itertools import filterfalse
import pandas as pd
import numpy as np
import json
import os


URL_CASES  = "https://raw.githubusercontent.com/reichlab/covid19-forecast-hub/master/data-truth/truth-Incident%20Cases.csv"
URL_DEATHS = "https://raw.githubusercontent.com/reichlab/covid19-forecast-hub/master/data-truth/truth-Incident%20Deaths.csv"
URL_FORECAST = "https://raw.githubusercontent.com/reichlab/covid19-forecast-hub/master/data-truth/zoltar-truth.csv"

path_to_truth_data        = './covid19-forecast-hub/data-processed'
path_to_ensemble_metadata = './covid19-forecast-hub/ensemble-metadata'

path_to_save = '/Users/chaosdonkey06/Dropbox/BIOMAC/EnsembleForecast'

dates_eval = pd.date_range(start='2020-06-08', end='2021-02-15', freq='7D')


all_forecasts_df = pd.read_csv(os.path.join(path_to_save, 'data', 'deaths_forecast_all.csv'))
