from datetime import datetime
import pandas as pd
import numpy as np
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import yfinance as yf


def download_yahoo_finance_ticker(symbols, start, end, save_file=None):
    """
    Télécharge les données financières à partir de Yahoo Finance pour un ou plusieurs symboles.
    
    Parameters:
        symbols (str or list): Le ou les symboles des actions (ex : 'AAPL' ou ['AAPL', 'MSFT']).
        start (str): Date de début au format 'YYYY-MM-DD'.
        end (str): Date de fin au format 'YYYY-MM-DD'.
        save_file (str, optional): Nom du fichier CSV pour sauvegarder les données. 
                                   Si None, les données ne seront pas sauvegardées.
    
    Returns:
        pandas.DataFrame: Un DataFrame contenant les données téléchargées.
    """
    try:
        if not symbols:
            raise ValueError("Le paramètre 'symbols' ne peut pas être vide.")
        if isinstance(symbols, str):
            symbols = [symbols]
        if not isinstance(symbols, list):
            raise TypeError("Le paramètre 'symbols' doit être une chaîne ou une liste de chaînes.")
        

        print(f"Téléchargement des données pour : {', '.join(symbols)} de {start} à {end}...")
        data = yf.download(tickers=symbols, start=start, end=end, group_by='ticker')
        
        if data.empty:
            raise ValueError(f"Aucune donnée téléchargée pour les symboles : {', '.join(symbols)}.")

        if save_file:
            data.to_csv(save_file)
            print(f"Données sauvegardées dans le fichier : {save_file}")

        return data

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None


def as_ndarray(y):
    if isinstance(y, (pd.Series, pd.DataFrame)):
        return y.values
    elif isinstance(y, np.ndarray):
        return y
    else:
        raise ValueError("`y` should be pd.SEries, pd.DataFrame, or np.ndarray to cast to np.ndarray")

def is_datetime_dtypes(x):
    return is_datetime(x)



def add_freq(idx, freq=None):
    """Add a frequency attribute to idx, through inference or directly.

    Returns a copy.  If `freq` is None, it is inferred.
    """

    idx = idx.copy()
    if freq is None:
        if idx.freq is None:
            freq = pd.infer_freq(idx)
        else:
            return idx
    idx.freq = pd.tseries.frequencies.to_offset(freq)
    if idx.freq is None:
        raise AttributeError(
            "no discernible frequency found to `idx`.  Specify"
            " a frequency string with `freq`."
        )
    return idx

