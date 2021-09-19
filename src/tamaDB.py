import re
import datetime
from dateutil import parser
import pickle
import os
from tamaLINE import *
import discord
from discord.ext import commands


def delete(word):
    word = word.strip()
    temp = re.findall(r'\w+',word)
    if not temp or temp[0] in ['ch1','ch2','ch3','strong','br','','span','hr','max','event','td']:
        return False
    elif word.lower().find('max') !=-1 or word.find('</a>') !=-1:
        return False
    elif word.lower().find('atk') !=-1 or word.lower().find(' hp') !=-1 or word.find('HP') !=-1:
        return False
    elif word.find('｢') !=-1 or word.find('%') !=-1:
        return False
    elif word.lower().find('apply') !=-1 or word.lower().find('increase') !=-1:
        return False
    elif word.lower().find('def') !=-1 or word.lower().find('np') !=-1:
        return False
    elif word.lower().find('gain') !=-1 or word.lower().find('decrease') !=-1:
        return False
    elif word.lower().find('damage') !=-1 or word.lower().find('turn') !=-1:
        return False
    elif word.lower().find('activates') !=-1 or word.lower().find('defeated') !=-1:
        return False
    elif word.lower().find('equipped') !=-1 or word.lower().find('dddddddd') !=-1:
        return False
    else:
        return True
    
    
def parseURL(string):
    prefix = "http://fate-go.cirnopedia.org/"
    if string.find('servant_profile') != -1 or  string.find('craft_essence_profile') != -1:
        reg = re.findall(r'\w+_\w+\.\w+\?\w+=\d+#*\w+', string)[0]
        return prefix + reg
    else:
        return string
    
    

def datesplit(date, realyear):
    split = re.findall(r'\d+\/\d+', date)
    return "Estimated from "+split[0] + '/%d to ' %realyear + split[1]+"/%d" %realyear



def datetimesplit(date, realyear):
    split = re.findall(r'\d+\/\d+', date)
    string = split[0]+'/%d' %realyear
    return parser.parse(string)



def sersort(name, banner, serlist, serdict, date, datetime):
    if not name in serlist:
        serlist.append(name)
    try:
        serdict[name]['Rate up'] +=1
    except KeyError:
        serdict[name] = {}
        serdict[name]['Rate up'] = 1
        serdict[name]['Banner'] = {}
    finally:
        serdict[name]['Banner'][banner] = {"Date":date ,"datetime":datetime }
        
          
        
def search(name):
    name = name.lower()
    lname = name.split(' ')
    dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
    #with open(dir_path + '/Database/serlist.pkl', 'rb') as b, open(dir_path+ '/Database/seraliases.pkl', 'rb') as a:
    
    for i in range(len(lname)):
        #sorry artoria lovers but I'm not messing with the already built databases
            if lname[i] == 'artoria':
                lname[i] = 'altria'
            if lname[i] == 'onee':
                lname[i] = 'nee'
            if lname[i] == 'bikini' or lname[i] == 'swimsuit':
                lname[i] = 'summer'
            if lname[i] == 'ssr':
                lname[i] = '5★'
            if lname[i] == 'sr':
                lname[i] = '4★'
            if lname[i] == 'r' or lname[i] == 'rare':
                lname[i] = '3★'
            if lname[i] == 'star' or lname[i] == 'stars':
                lname[i] = '★'
    
    candidate = []
    #notcandidate = []
    
    with open(dir_path + '/Database/serlist.pkl', 'rb') as b, open(dir_path+ '/Database/seraliases.pkl', 'rb') as a:
        seraliases = pickle.load(a)
        serlist = pickle.load(b)
        
        for ser in seraliases:
            found = False
            for alias in seraliases[ser]:
                true = True
                breakbol = False
                splalias = alias.split(' ')
                
                for pname in lname:
                    true = true&(pname in splalias)
                if true:
                    for spl in splalias:
                        true = true&(spl in lname)
                '''if not 'alter' in name and 'alter' in splalias:
                    true = False
                    notcandidate.append(ser)
                    breakbol = True
                elif len(lname) == len(splalias) and not 'alter' in name:
                    true2 = True
                    for pname in lname:
                        true2 = true2&(pname in splalias)
                    if true2:
                        notcandidate.pop()
                        breakbol = False
                        true = True'''
                    #if not 'summer' in name and 'summer' in splalias:
                    #    true = False
                    #    notcandidate.append(ser)
                    #   breakbol = True
                    #if not true:
                    #    break
                if true:
                    found = True
                    break
            if found:
                candidate.append(ser)
                
        for ser in serlist:
            true = True
            for split in lname:
                true = true&(split in ser.lower())
                if not true:
                    break
            if true:
                if not ser in candidate:
                    candidate.append(ser)
            
    return candidate                             
    
async def serrateup(ctx, ser):
    dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))
    sername = ' '.join(ser.split(' ')[2:])
    serclass = ' '.join(ser.split(' ')[:2])
    now = datetime.datetime.now()
    curryear = now.year
    jpyear = curryear-2
    startyear = 2015
    servant = Servant(ctx, "Tamamo of Knowledge")
    
    with open(dir_path + '/Database/gacha' + '.pkl', 'rb') as f1, open(dir_path + '/Database/serdict' + '.pkl', 'rb') as f2:
        gacha = pickle.load(f1)
        serdict = pickle.load(f2)
        rateup = serdict[ser]['Rate up']
        banner = serdict[ser]['Banner']
        
        if ser in ['5★ Lancer Tamamo-no-Mae', '4★ Berserker Tamamo Cat', '5★ Caster Tamamo-no-Mae']:
            await servant.dialogbox("Turned out you are still able to make good decision huh? But still, I can't guarantee the outcome.")
        else:
            await servant.dialogbox("... still want to gamble huh? Human sure are stupid.")
        
        embed=discord.Embed(title="%s servant, %s has %d rate-ups in total. The next rate-up banner are:" %(serclass, sername, rateup) ,color=servant.color)
        
        for rateup in banner:
           if serdict[ser]['Banner'][rateup]['datetime'] > now:
               embed.add_field(name = rateup, value= serdict[ser]['Banner'][rateup]['Date'], inline = False)
        
        await ctx.send(embed=embed)
        await servant.convbox("Special thanks to http://fate-go.cirnopedia.org/ for the information provided.")
        
            
            
