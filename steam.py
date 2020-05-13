#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import os
import urllib.parse
import json
import re

# Config
bot_name = "PUT_YOU_BOT_NAME_HERE"

basesteam = 'https://store.steampowered.com/app/'
basedb = "https://steamdb.info/sales/?min_discount=95&min_rating=0"
url = "http://127.0.0.1:1242/Api/Bot/{}/Redeem".format(bot_name)

headers = {
    'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion'
}

response = requests.get(basedb, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

filterapps = soup.findAll("td", {"class": "applogo"})
text = '{}'.format(filterapps)
soup2 = BeautifulSoup(text, "html.parser")

for link in soup2.findAll('a', attrs={'href': re.compile("^/")}):
    link = link.get('href')
    templink = link.replace("/", "")
    finalappid = templink.replace("app", "")
    print('Found free Game! App-ID: ' + finalappid)
    print('Here is the Link: {}'.format(basesteam + finalappid))
    print('Redeming')
    GG = "{}".format(finalappid)
    data = {"KeysToRedeem": [GG]}
    print(data)
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    cc = requests.post(url, data=json.dumps(data), headers=headers)
    print(cc)
    print(cc.text)
