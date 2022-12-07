from flask import Flask, jsonify
from flask_cors import CORS
#from sqlfunctions import select_passwordhashes
#from text_search_functie import fill_tables_with_score
import json
import time
app = Flask(__name__)
CORS(app)
running="done"
def test():
    global running
    time.sleep(10)
@app.route("/api/recalculate/<code>",methods=['GET'])
def get_posts(code):
    global running
    #sql=select_passwordhashes()
    #hashes=[]
    #for hash in sql:
        #hashes.append(hash[0])
    if code is "DikkeBerta":
      if running!="running":
          running="running"
          test()
          #fill_tables_with_score()
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

app.run(host='0.0.0.0', debug=True, port=8080)
