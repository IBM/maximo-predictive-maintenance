from flask import Flask
import requests
import flask
import pickle
import pandas as pd
import sys

# app = Flask(__name__)
# @app.route('/')
# cookies only needed if behind realm auth
cookies = dict(LtpaToken2=realm_token)
headers = {'Content-Type': 'application/json', "maxauth": max_token}
# get meter data
maximo_domain = sys.argv[1]  # IP Address + PORT
max_token = sys.argv[2]
asset_id = sys.argv[3] #"2112"

endpoint = "/oslc/os/mxasset?oslc.select=assetmeter,expectedlife&oslc.where=assetnum=" + asset_id
res = requests.get(maximo_domain + endpoint, cookies=cookies, headers=headers)

meter_data = {}
meters = res["rdfs:member"][0]["spi:assetmeter"]
for m in meters:
    meter_data[m['spi:metername']] = m['spi:lastreading']
# convert meter values to pandas dataframe
pd.DataFrame.from_dict(meter_data)
classifier = pickle.loads(load('model.joblib'))
predictions = classifier.predict(meter_data)
requests.post("/oslc/os/mxasset/" + restid,
              data={"expectedlife": predictions[0]})

# NOTES, remove below

# docs
# get token
# https://a3jgroup.com/querying-maximo-using-the-rest-and-json-apis/

# token=$(echo $MAXIMO_USERNAME:$MAXIMO_PASSWORD | base64)
# curl $MAXIMO_URL

# Query Maximo for List of Assets Matching certain type

# Query Maximo for Asset Meter

# Create METER
# /maxrest/rest/os/mxasset/32409?ASSETMETER.ID1.METERNAME=RUNHOURS&ASSETMETER.ID1.LINEARASSETMETERID=0&ASSETMETER.ID1.METERREADING.ID1.READING=1876&ASSETMETER.ID1.METERREADING.ID1.READINGDATE=2014-06-09T11:34:00&ASSETMETER.ID1.METERREADING.ID1.INSPECTOR=OCHEE&ASSETMETER.ID1.METERREADING.ID1.DELTA=77
# Maximo REST queries
# https://developer.ibm.com/static/site-id/155/maximodev/restguide/Maximo_Nextgen_REST_API.html

# /oslc/os/mxasset/{restid}?oslc.select=assetnum,status,exp.myreplacecost,assetmeter{...}

# ENDPOINT='/oslc/os/mxasset?oslc.pageSize=10'
# ENDPOINT='/oslc/os/mxasset?oslc.select=assetnum,status,exp.myreplacecost,assetmeter{...}'

# curl -v --cookie "$COOKIE" -H 'Content-Type: application/json' -H "maxauth: $token" ${MAXIMO_URL}${ENDPOINT}

# select assetmeters where assetid = ""
# curl --cookie "$COOKIE" -H 'Content-Type: application/json' -H "maxauth: d2lsc29uOndpbHNvbg==" "$MAXIMO_URL/oslc/os/mxasset?oslc.select=assetnum,assetmeter&oslc.where=assetnum=\"2112\"" | jq .
