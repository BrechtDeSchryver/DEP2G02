from flask import Flask, jsonify
from flask_cors import CORS
#from sqlfunctions import select_passwordhashes
# from text_search_functie import fill_tables_with_score
import pickle
import json
import time
app = Flask(__name__)
CORS(app)
running = "done"


def test():
    global running
    time.sleep(10)


# final_model = pickle.load(open('final_model.sav', 'rb'))



@app.route("/api/predict/Omzet=<Omzet>&personeel=<personeel>&sector=<sector>&jr=<jaarrekening>&pdf=<pdf>&beurs=<beursgenoteerd>", methods=['GET'])
def predict(Omzet, personeel, postcode, sector, jaarrekening,pdf ,beursgenoteerd):
    # Omzet= omzetcijfer (int)
    # personeel= aantal personeelsleden (int)
    # postcode= postcode (4 char int)
    # sector= sectornacebel (5 char int)
    # jaarrekening= jaarrekening aanwezig (boolean)
    # beursgenoteerd= beursgenoteerd (boolean)
    score = 0
    # hier moet de predict komen en uitkomst stop je in score
    score = final_model.predict([[Omzet, personeel, postcode, sector, jaarrekening, pdf, beursgenoteerd]])
    print(Omzet, personeel, postcode, sector, jaarrekening, beursgenoteerd)
    x = {"score": score}
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
