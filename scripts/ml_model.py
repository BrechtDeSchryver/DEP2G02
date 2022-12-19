import pandas as pd
from sqlfunctions import get_datapunten_voor_model
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
import pickle

min_max_scaler_omzet = pickle.load(
    open('scripts\\ml_files\\min_max_scaler_omzet.sav', 'rb'))
min_max_scaler_personeel = pickle.load(
    open('scripts\\ml_files\\min_max_scaler_personeelsleden.sav', 'rb'))


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
    # TODO: we hebben originele data nodig om nieuwe data te transformeren
    data["sector"] = data["sector"].astype('category')
    # ordinal_encoder = OrdinalEncoder()
    # data["sector"] = ordinal_encoder.fit_transform(data[["sector"]])
    # print(ordinal_encoder.categories_)
    data["beursgenoteerd"] = data["beursgenoteerd"].astype('category')
    data["pdf_aanwezig"] = data["pdf_aanwezig"].astype('category')
    data["site_aanwezig"] = data["site_aanwezig"].astype('category')
    data["stedelijkheidsklasse"] = data["stedelijkheidsklasse"].astype(
        'category')

    data["omzet"] = min_max_scaler_omzet.fit_transform(data[["omzet"]])
    data["personeelsleden"] = min_max_scaler_personeel.fit_transform(
        data[["personeelsleden"]])

    data["personeelsleden"] = data["personeelsleden"].astype('float')

    return data
