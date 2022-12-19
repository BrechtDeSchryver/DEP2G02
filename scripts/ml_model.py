import pandas as pd
from sqlfunctions import get_datapunten_voor_model
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
import pickle


def get_initial_dataframe():
    data = get_datapunten_voor_model()
    dataframe = pd.DataFrame(data, columns=['ondernemingnr', 'omzet', 'beursgenoteerd',
                             'sector', 'personeelsleden', 'site_aanwezig', 'pdf_aanwezig', 'score'])
    dataframe = dataframe.groupby('ondernemingnr').agg({'omzet': 'first', 'beursgenoteerd': 'first', 'sector': 'first',
                                                        'personeelsleden': 'first', 'site_aanwezig': 'first', 'pdf_aanwezig': 'first', 'score': 'sum'}).reset_index()
    dataframe.drop("ondernemingnr", axis=1, inplace=True)
    dataframe.drop("score", axis=1, inplace=True)
    return dataframe


def transform_data(data):
    data["sector"] = data["sector"].astype('category')
    data["beursgenoteerd"] = data["beursgenoteerd"].astype('category')
    data["pdf_aanwezig"] = data["pdf_aanwezig"].astype('category')
    data["site_aanwezig"] = data["site_aanwezig"].astype('category')
    data["stedelijkheidsklasse"] = data["stedelijkheidsklasse"].astype(
        'category')

    data["beursgenoteerd"] = data["beursgenoteerd"].cat.codes
    data["beursgenoteerd"] = data["beursgenoteerd"].astype('category')

    data["personeelsleden"] = data["personeelsleden"].astype('float')

    data = data.dropna()

    data["sector"] = data["sector"].astype('category')

    return data
