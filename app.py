#coding utf-8
from bottle import route,run
from requests_oauthlib import OAuth1Session
import conf
import json
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
    req = twitter.get(url,params = params)
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            tweet_text = tweet["text"]
            if re.search("OPEN",tweet_text):
                return "OPEN"
            if re.search("CLOSE",tweet_text):
                return "CLOSE"
            return "ERROR"
    else:
        return "ERROR"

@route('/')
def denden():
    return "でんでん～"

@route('/box&c=<campus>',method = 'GET')
def oc_show(campus = 'k'):
    status = getOC(campus)
    return {"status":status}

run(host="0.0.0.0", port=8124)