# -*- coding: utf-8 -*-
from bottle import route,run
from requests_oauthlib import OAuth1Session
import conf
import json
import os
import re


CK = conf.consumer_key
CS = conf.consumer_secret
AT = conf.access_token
AS = conf.access_token_secret


twitter = OAuth1Session(CK,CS,AT,AS)

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params = {
    "screen_name":"denx_robotaro",
    "count" : "1"
}

req = twitter.get(url,params = params)
if req.status_code == 200:
    timeline = json.loads(req.text)
    for tweet in timeline:
        print(tweet["text"])
else:
    print("Error:%d"%req.status_code)

def getOC(campus):
    
    name = "denx_robotaro"
    if campus == "i":
        name = "denx_imadegawa"
    
    params = {
         "screen_name":name,
         "count" : "10"
    }
    oc = ""
    stat_change_time = ""
        
    req = twitter.get(url,params = params)
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:           
            
            #statusの更新
            tweet_text = tweet["text"]
            m = re.search("OPEN|CLOSE",tweet_text)
            if m is not None:
                stat = {
                    "status":tweet_text[m.start():m.end()],
                    "stat_change_time":getTime(tweet_text),
                    "campus":"imadegawa" if campus == "i" else "kyotanabe"
                }
                return stat
            return "ERROR"
    else:
        return "ERROR"

def getTime(tweet_text):
    m = re.search(r"\d*時\d*分",tweet_text)
    if m is not None:
        return tweet_text[m.start():m.end()]
    else:
        return "GET TIME ERROR"

@route('/')
def denden():
    return "でんでんでんくす"

@route('/box&c=<campus>',method = 'GET')
def oc_show(campus = 'k'):
    status = getOC(campus)
    return json.dumps(status,ensure_ascii=False)

run(host="0.0.0.0",port=int(os.environ.get("PORT", 5000)))
#run(host="localhost",port=int(os.environ.get("PORT", 5000)))