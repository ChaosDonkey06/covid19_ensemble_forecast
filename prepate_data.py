# zoltpy related dependencies
from zoltpy.covid19 import COVID_TARGETS, covid19_row_validator, validate_quantile_csv_file, COVID_ADDL_REQ_COLS
from zoltpy.quantile_io import json_io_dict_from_quantile_csv_file
from zoltpy.cdc_io import YYYY_MM_DD_DATE_FORMAT
from zoltpy.connection import ZoltarConnection
import zoltpy.util as zutil

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


elig_df_all = []
for date in dates_eval:
    path_to_read   = os.path.join(path_to_ensemble_metadata, date.strftime('%Y-%m-%d')+'-inc_death-model-eligibility.csv')
    model_elige_df = pd.read_csv(path_to_read)
    model_elige_df["date_forecast"] = date
    elig_df_all.append(model_elige_df)
elig_df_all = pd.concat(elig_df_all)

# keep only eligible models
models_df = elig_df_all.copy()
models_df = models_df[models_df.overall_eligibility=="eligible"]

import datetime

all_forecasts = []
# iterate over eligible models
for model in models_df.model.unique():
    model_df = models_df.copy(); model_df = model_df[model_df.model==model]
    for date in model_df.date_forecast.unique():
        date0 = pd.to_datetime(date)
        date1 = pd.to_datetime(date)-datetime.timedelta(1)

        path_to_csv0 = os.path.join(path_to_truth_data, model, date0.strftime('%Y-%m-%d')+'-{}.csv'.format(model))
        path_to_csv1 = os.path.join(path_to_truth_data, model, date1.strftime('%Y-%m-%d')+'-{}.csv'.format(model))

        if os.path.isfile(path_to_csv0):
            df_forecast = pd.read_csv(path_to_csv0)
        elif os.path.isfile(path_to_csv1):
            df_forecast = pd.read_csv(path_to_csv1)

        else:
            print(f"Model {model} for date {date0}, {date1} not found")

        df_forecast["model"] = model
        all_forecasts.append(df_forecast)

all_forecasts_df = pd.concat(all_forecasts)
all_forecasts_df.to_csv(os.path.join(path_to_save, 'data', 'deaths_forecast_all.csv'))

df1         = pd.read_csv(URL_CASES)
df2         = pd.read_csv(URL_DEATHS)
df_forecast = pd.read_csv(URL_FORECAST)

df1.to_csv(os.path.join(path_to_save, 'data','cases.csv'))
df2.to_csv(os.path.join(path_to_save, 'data','deaths.csv'))