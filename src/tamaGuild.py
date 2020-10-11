import json
import os
import re
import redis
dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
r = redis.from_url(os.environ.get("REDIS_URL"))



def initdb():
    d = {}
    js = json.dumps(d)
    r.set('guild', js)

def jsonsave(data):
    raw = json.dumps(data)
    r.set('guild', raw)


def initguild(id):
    data = json.loads(r.get('guild'))
    data[str(id)] = {}
    jsonsave(data)
        
        
def addgif(id, emoji, url):
    data = json.loads(r.get('guild'))
    if str(id) in data:
        pass
    else:
        data[str(id)] = {}
        data[str(id)][emoji] = url
        jsonsave(data)
        return 0
    
    if emoji in data[str(id)]:
        return 1
    else:
        data[str(id)][emoji] = url
        jsonsave(data)
        return 0


def deletegif(id, emoji):
    data = json.loads(r.get('guild'))
    if str(id) in data:
        if emoji in data[str(id)]:
            del data[str(id)][emoji]
            jsonsave(data)
            return 0
        else:
            return 1
    else:
        return 1
            

def checkemoji(message):
    temp = re.findall(r':[A-Za-z0-9]+:', message)
    if len(temp)==0:
        return False
    return True


def checkurl(message):
    if message.find(".gif") != 1 and message.find("http") !=-1:
        return True
    return False

