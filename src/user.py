import json
import os
import redis

dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
r = redis.from_url(os.environ.get("REDIS_URL"))



def initdict():
    d = {}
    js = json.dumps(d)
    r.set('user', js)



def jsonsave(data):
    raw = json.dumps(data)
    r.set('user', raw)


# adopted: being a master
# discovered: regalia
# mode: persona
# nsfw: nsfw count
# intro: current intro page
# sanction: punishment for violating stuff
# bond: bond
def inituser(id, data = None):
    flag = False
    if data == None:
        flag = True
        data = json.loads(r.get('user'))
    data[str(id)] = {'adopted': False, 'discovered': False, 'mode': 'OG', 'nsfw': 0, 'intro': 1, 'sanction': 0,
                     'bond': 0, 'emoji': 0}
    if flag:
        jsonsave(data)



# user discovery
def userdisc(id):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)
    data[str(id)]['discovered'] = True
    jsonsave(data)



def getuserdisc(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        discovered = data[str(id)]['discovered']
    else:
        inituser(id)
        discovered = False

    return discovered



def getmode(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        mode = data[str(id)]['mode']
    else:
        inituser(id)
        mode = 'OG'

    return mode



def changemode(id, mode):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)
    data[str(id)]['mode'] = mode
    jsonsave(data)



def nsfwinc(id):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)
    data[str(id)]['nsfw'] += 1
    jsonsave(data)



def getnsfw(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        nsfw = data[str(id)]['nsfw']
    else:
        inituser(id)
        nsfw = 0

    return nsfw



def setadopt(id):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)
    data[str(id)]['adopted'] = True
    jsonsave(data)



def getadopt(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        adopt = data[str(id)]['adopted']
    else:
        inituser(id)
        adopt = False

    return adopt



def setpage(id, page):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)
    data[str(id)]['intro'] = page
    jsonsave(data)



def getpage(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        page = data[str(id)]['intro']
    else:
        inituser(id)
        page = 1
    return page



def getsanction(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        sanction = data[str(id)]['sanction']
    else:
        inituser(id)
        sanction = 0
    return sanction



def decsanction(id):
    data = json.loads(r.get('user'))
    sanction = data[str(id)]['sanction']
    sanction -= 1
    data[str(id)]['sanction'] = sanction
    jsonsave(data)



#TODO remember to check if need inituser
def sanction(id):
    data = json.loads(r.get('user'))
    sanction = data[str(id)]['sanction']
    sanction += 10
    data[str(id)]['sanction'] = sanction
    data[str(id)]['adopted'] = False
    bond = data[str(id)]['bond']
    bond = bond // 2
    data[str(id)]['bond'] = bond
    jsonsave(data)



def getbond(id):
    data = json.loads(r.get('user'))
    if str(id) in data:
        bond = data[str(id)]['bond']
    else:
        inituser(id)
        bond = 0

    return bond



def incbond(id, num=1):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)
    data[str(id)]['bond'] += num
    jsonsave(data)



def useEmoji(id):
    data = json.loads(r.get('user'))
    if not str(id) in data:
        inituser(id, data)

    data[str(id)]['emoji'] +=1
    jsonsave(data)

