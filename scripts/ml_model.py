import pandas as pd
from sqlfunctions import get_datapunten_voor_model
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler


def get_initial_dataframe():
    data = get_datapunten_voor_model()
    dataframe = pd.DataFrame(data, columns=['ondernemingnr', 'omzet', 'beursgenoteerd', 'sector', 'personeelsleden', 'site_aanwezig', 'pdf_aanwezig', 'score'])
    dataframe = dataframe.groupby('ondernemingnr').agg({'omzet': 'first', 'beursgenoteerd': 'first', 'sector': 'first', 'personeelsleden': 'first', 'site_aanwezig': 'first', 'pdf_aanwezig': 'first', 'score': 'sum'}).reset_index()
    dataframe.drop("ondernemingnr", axis=1, inplace=True)
    dataframe.drop("score", axis=1, inplace=True)
    return dataframe


def transform_data(data):
    # TODO: we hebben originele data nodig om nieuwe data te transformeren
    data["sector"] = data["sector"].astype('category')
    ordinal_encoder = OrdinalEncoder()
    data["sector"] = ordinal_encoder.fit_transform(data[["sector"]])
    data["beursgenoteerd"] = data["beursgenoteerd"].astype('category')
    data["pdf_aanwezig"] = data["pdf_aanwezig"].astype('category')
    data["site_aanwezig"] = data["site_aanwezig"].astype('category')
    min_max_scaler = MinMaxScaler()
    data["omzet"] = min_max_scaler.fit_transform(data[["omzet"]])
    data["personeelsleden"] = min_max_scaler.fit_transform(data[["personeelsleden"]])
    data["personeelsleden"] = data["personeelsleden"].astype('float')
    

    return data
