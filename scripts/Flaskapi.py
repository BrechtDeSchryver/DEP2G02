from flask import Flask, jsonify
from flask_cors import CORS
#from sqlfunctions import select_passwordhashes
# from text_search_functie import fill_tables_with_score
import pickle
from ml_model import transform_data
import pandas as pd
import numpy as np
import json
import time
app = Flask(__name__)
CORS(app)
running = "done"


def test():
    global running
    time.sleep(10)


final_model = pickle.load(open('scripts\\ml_files\\final_model.sav', 'rb'))
min_max_scaler_omzet = pickle.load(
    open('scripts\\ml_files\\min_max_scaler_omzet.sav', 'rb'))
min_max_scaler_personeel = pickle.load(
    open('scripts\\ml_files\\min_max_scaler_personeelsleden.sav', 'rb'))


@app.route("/api/predict/omzet=<omzet>&personeel=<personeel>&sector=<sector>&jr=<jaarrekening>&website=<website>&beurs=<beursgenoteerd>&stedelijkheidsklasse=<stedelijkheidsklasse>", methods=['GET'])
def predict(omzet, personeel, sector, jaarrekening, website, beursgenoteerd, stedelijkheidsklasse):
    # Omzet= omzetcijfer (int)
    # personeel= aantal personeelsleden (int)
    # postcode= postcode (4 char int)
    # sector= sectornacebel (5 char int)
    # jaarrekening= jaarrekening aanwezig (boolean)
    # beursgenoteerd= beursgenoteerd (boolean)
    beursgenoteerd = 1 if beursgenoteerd == "true" else 0
    website = 1 if website == "true" else 0
    jaarrekening = 1 if jaarrekening == "true" else 0
    data = np.array([int(omzet), beursgenoteerd, int(sector),
            int(personeel), website, jaarrekening, int(stedelijkheidsklasse)])
    data = data.reshape(1, -1)
    # appendd values to dataframe
    dataframe = pd.DataFrame(data, columns=['omzet', 'beursgenoteerd', 'sector',
                             'personeelsleden', 'site_aanwezig', 'pdf_aanwezig', 'stedelijkheidsklasse'])
    print(dataframe)
    # transform data
    dataframe = transform_data(dataframe)
    last_row = dataframe.iloc[-1]
    print(last_row)
    # get score
    score = final_model.predict([last_row])

    # hier moet de predict komen en uitkomst stop je in score
    # score = final_model.predict([[Omzet, personeel,  sector, jaarrekening, pdf, beursgenoteerd]])
    # print(Omzet, personeel, sector, jaarrekening, beursgenoteerd)
    x = {"score": float(score)}
    return json.dumps(x)


# @app.route("/api/recalculate/<code>", methods=['GET'])
# def get_posts(code):
#     global running
#     # sql=select_passwordhashes()
#     # hashes=[]
#     # for hash in sql:
#     # hashes.append(hash[0])
#     if code == "DikkeBerta":
#         if running != "running":
#             running = "running"
#             # test()
#             fill_tables_with_score()
#             running = "done"
#     x = {"status": running}
#     return json.dumps(x)


@app.route("/api/status", methods=['GET'])
def get_status():
    x = {"status": running}
    return json.dumps(x)


@app.route("/", methods=['GET'])
def uptime():
    x = {"status": "online"}
    return json.dumps(x)


app.run(host='0.0.0.0', debug=True, port=8080)
