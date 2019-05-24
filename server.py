from flask import Flask
import requests
import flask
import pickle
import pandas as pd
import sys
import os
from dotenv import load_dotenv
from joblib import load
load_dotenv()

# app = Flask(__name__)
# @app.route('/')
# cookies only needed if behind realm auth
# get meter data
# maximo_domain = sys.argv[1]  # IP Address + PORT
#max_token = sys.argv[2]
asset_id = sys.argv[1]  # "2112"
realm_token = sys.argv[2]

cookies = dict(LtpaToken2=realm_token)
headers = {'Content-Type': 'application/json',
           "maxauth": os.getenv("max_token")}

# Prereq
# Create meter for each sensor value / feature associated with model
q_endpoint = "/maximo/oslc/os/mxasset?oslc.select=assetmeter,expectedlife&oslc.where=assetnum=" + asset_id
res = requests.get(os.getenv("maximo_domain") + q_endpoint,
                   cookies=cookies, headers=headers)

meter_data = {}
print(res)
meters = res.json()["rdfs:member"][0]["spi:assetmeter"]
for m in meters:
    meter_data[m['spi:metername']] = m['spi:lastreading']
# convert meter values to pandas dataframe
meter_df = pd.DataFrame.from_dict(meter_data, orient='index')

'''
clf = load("lin_reg.joblib")
clf.predict(meter_df)
predictions = clf.predict(meter_df)
print("RUL:" + predictions.join())
'''

threshold = 50
predictions = [62]

# update RUL in maximo DB
requests.post(maximo_domain + "/maximo/oslc/os/mxasset/" + restid,
              data={"expectedlife": predictions[0]}, cookies=cookies, headers=headers)

# create work order if RUL below threshold
if predictions[0] < threshold:
    asset_num = str(2112)
    site_id = "DENVER"
    wo_endpoint = "/maxrest/rest/mbo/workorder?_lid=" + username + "&_lpwd=" + password + \
        "&_compact=true&_format=json&description=FixTurboFan&siteid=" + \
        site_id + "&assetnum=" + asset_num
    requests.put(maximo_domain + wo_endpoint,
                 data={"expectedlife": predictions[0]}, cookies=cookies, headers=headers)

# NOTES, remove below
