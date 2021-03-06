'''
By: Jonah Stegman
feature extraction for ENGG*6500 project
This file looks up the country in which a url is hosted.
'''

import requests
import pandas as pd
import os
import json
import re
import time


url = 'https://api.freegeoip.app/json/'
key = '?apikey=d4d79110-44e2-11ec-b60c-f1d7f1dfb6b1'
path = os.path.dirname(__file__)
input_file = "data/malicious_phish.csv"
df = pd.read_csv(os.path.join(path, input_file))
num = 111501
while num < df['URL'].count() + 1:
    total = num+14500
    if total > df['URL'].count() + 1:
        total = df['URL'].count() + 1
    df2 = df[num:total]
    num = total
    country = []
    for x in df2['URL']:
        #query the endpoint and get the country codes for each URL
        website = re.split("^http(s|)://",x.lower())[-1]
        website = website.replace('www.','').split('/')[0]
        response = requests.get(url+website+key)
        if '404' not in response.text:
            try:
                code = json.loads(response.text)["country_code"]
                country.append(code)
            except Exception:
                country.append('zz')
        else:
            country.append('zz')

    df2['Country'] = country
    df2.to_csv('out2.csv', mode='a', header=False,index=False)
    #wait for the api cooldown to finish
    time.sleep(2700)
    #df.to_csv('out.csv',index=False)