import os
import glob
import pandas as pd
from pathlib import Path
import yaml

'''
    Get the path of the root dorectory of the repo.
'''
def get_root():
    cur = Path(os.path.dirname(__file__))
    while(cur.resolve().parts[-1] != 'covid19-forecast-hub') :
        try:
            cur = cur / '..'
        except:
            cur = Path(os.getcwd()) / '..' 
    return cur.resolve()

'''
    Get the path to the `dtaa-processed` folder.
'''
def get_data(path_to_reich_repo):
    root = path_to_reich_repo
    return root/ 'data-processed'

'''
    Returns a list to the forecasts. It just returns the nameof teh forecast (without the .csv extension)
'''
def get_forecasts(path_to_reich_repo):
    root = path_to_reich_repo
    forecasts = list(map(lambda x: x.stem,root.glob('data-processed/**/*.csv')))
    return forecasts

'''
    Same as `get_forecasts`, but return the file path to all forecast files.
'''
def get_forecast_files(path_to_reich_repo):
    root = path_to_reich_repo
    forecasts = list(map(lambda x: x.resolve(),root.glob('data-processed/**/*.csv')))
    return forecasts

'''
    Return the names of all models in the `data-processed` folder.
'''
def get_models(path_to_reich_repo):
    root = path_to_reich_repo
    models = [f.name for f in (root / 'data-processed').iterdir()]
    return models

'''
    Return a dict with all the elements in the metadata file.
    If `model` is None, returns a dict representation of ALL models.
    Else, returns the metadata representation for that particular model.
    `model` SHOULD be `model_abbr`.
'''
def get_metadata(model=None):
    data = get_data()
    if model is not None:
        metadata = data.glob(f"{model}/metadata-{model}.txt")
        with open(metadata, 'r') as m:
            return yaml.load(m, Loader=yaml.BaseLoader)
    else:
        metadatas = []
        for meta in data.glob('**/metadata-*.txt'):
            metadatas.append(yaml.load(open(meta, 'r'), Loader=yaml.BaseLoader))
        return metadatas

'''
    Return a mapping of ALL forecasts for a model. The data returned is in the following format:
    return type: dict.
        - Key: `model_abbr` 
        - Value: dict with the following keys:
            - `metadata` : dict representation of the metadata of `model_abbr` model. 
            - `forcasts`: list of forecast filenames (including .csv extension) for `model_abbr` model.
'''
def get_meta_forecasts():
    metas = get_metadata()
    data = {}
    for meta in metas:
        res = {}
        model_abbr = meta['model_abbr']
        res['metadata'] = meta
        res['forecasts'] = list(map(lambda x: x.name, get_data().glob(f"{model_abbr}/*-{model_abbr}.csv")))
        data[model_abbr] = res
    return data