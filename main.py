import flask
from flask import Flask, Response, send_file, after_this_request
import urllib
import json                 # Used to load data into JSON format
from pprint import pprint
import pandas as pd
import os

# app = flask.Flask("after_response")
# AfterResponse(app)

app = Flask(__name__)

@app.before_request
def before_request_func():
    print("before_request is running!")
    try:
        def a(x):
            assert  x==3
    except NameError:
        print(a(2))
    except:
        print("1234")
    if __name__ =="__main__":
        print(a(3))

@app.route('/')
def hello():
    url = "https://data.sa.gov.au/data/api/3/action/datastore_search?resource_id=fec742c1-c846-4343-a9f1-91c729acd097&limit=5&q=title:jones"
    response = urllib.request.urlopen(url)

    text = response.read()
    json_data = json.loads(text)

    try:
        json_file = open("response.json", "w")
        json.dump(json_data, json_file, indent=6)
        json_file.close()

        df = pd.read_json("response.json")
        df.to_csv("response.csv")

    except Exception as e:
        print(e)

    return send_file('response.csv',
                     mimetype='text/csv',
                     attachment_filename='response.csv',
                     as_attachment=True)

@app.after_request
def after_request_func(response):
    print("Cleaning up temp files... ")

    try:
        os.remove("response.json")
        os.remove("response.csv")
    except Exception as e:
        print(e)

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)