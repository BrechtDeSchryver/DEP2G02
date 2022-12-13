from flask import Flask, jsonify
from flask_cors import CORS
#from sqlfunctions import select_passwordhashes
from text_search_functie import fill_tables_with_score
import json
import time
app = Flask(__name__)
CORS(app)
running="done"
def test():
    global running
    time.sleep(10)
@app.route("/api/predict/Omzet=<Omzet>&personeel=<personeel>&postcode=<postcode>&sector=<sector>&jr=<jaarrekening>&beurs=<beursgenoteerd>",methods=['GET'])
def predcit(Omzet,personeel,postcode,sector,jaarrekening,beursgenoteerd):
    #Omzet= omzetcijfer (int)
    #personeel= aantal personeelsleden (int)
    #postcode= postcode (4 char int)
    #sector= sectornacebel (5 char int)
    #jaarrekening= jaarrekening aanwezig (boolean)
    #beursgenoteerd= beursgenoteerd (boolean)
    score=0
    #hier moet de predict komen en uitkomst stop je in score
    print(Omzet,personeel,postcode,sector,jaarrekening,beursgenoteerd)
    x = {"test" : score}
    return json.dumps(x)
@app.route("/api/recalculate/<code>",methods=['GET'])
def get_posts(code):
    global running
    #sql=select_passwordhashes()
    #hashes=[]
    #for hash in sql:
        #hashes.append(hash[0])
    if code=="DikkeBerta":
      if running!="running":
          running="running"
          #test()
          fill_tables_with_score()
          running="done"
    x = {"status" : running}
    return json.dumps(x)
@app.route("/api/status",methods=['GET'])
def get_status():
    x = {"status" : running}
    return json.dumps(x)


@app.route("/",methods=['GET'])
def uptime():
  x = {"status" : "online"}
  return json.dumps(x)

app.run(host='127.0.0.1', debug=True, port=6969)
