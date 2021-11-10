from random import randint

import requests
from bs4 import BeautifulSoup

from tamaDB import *


async def fetch(servant, nsfw = None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ctx = servant.ctx
    
    with open(dir_path + "/Database/info.json") as f:
        data = json.loads(f.read())
        
        if nsfw == "nsfw":
            if not ctx.channel.is_nsfw():
                await servant.dialogbox("Cant do that")
                #count nsfw
                #more persona
                #remove group_sex and shitty tags
            else:
                #nsfw only tag, oof
                await servant.dialogbox("Yes")
                pass
        else:
            url = data["Persona"][servant.name]["Booru"]["SFW"]
            total = requests.get(url + '&pid=200&json=0')
            total = total.text
            total = int(re.findall(r'\d\d+', total)[0])
            page = randint(0, total//100+1)
            str = '&pid=%d' %page
            if page == total//100+1:
                str = str+ '&limit=%d' %(total%100)
            
            
            
            request = requests.get(url + str)
            print(request)
            d = json.loads(request.text)
            r = randint(0,len(d)-1)
            x = d[r]["file_url"]
            s = d[r]["source"]
            await servant.boorubox(s,x)
            



async def getPDT(ctx):
    s = json.loads(requests.get('http://worldtimeapi.org/api/timezone/America/Los_Angeles').text)['datetime']
    s = s[:-6]
    dt = parser.parse(s)
    
    st, minute, second = str(dt).split(':')
    date, hour = st.split(' ')
    yy, mm, dd = date.split('-')
    date = [mm, dd, yy]
    date = '-'.join(date)
    
    await ctx.send('PDT time is: ' + hour + ':' + minute + ', ' + date +'.')



async def updateDB(ctx):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    page = requests.get('http://fate-go.cirnopedia.org/summon.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    startyear = 2015
    curryear = datetime.datetime.now().year
    jpyear = curryear-2
    
    
    gacha = {}
    serlist = []
    serdict = {}
    classpickupno = 1
    singularitypickupno = 1
#TODO: change startyear+1 to curryear+1 after testing
    for i in range(startyear, curryear+1):
        gacha[str(i)] = {}
        banners = soup.find(id=str(i))
        banners = banners.next_sibling.next_sibling
        banners_list = banners.find_all('tr')
        del banners_list[0]
        
        for banner in banners_list:
            banner_name = banner.find_all(class_='banner')[0].next_sibling.next_sibling
            banner_date = banner.find_all(class_='banner')[0].next_sibling.next_sibling.next_sibling.next_sibling
            
            curr_e = banner_date
            banner_name = str(banner_name)
            while (str(curr_e).lower().find('class="desc"') == -1):
                if ( (str(curr_e).lower().find(") to ") == -1) and (str(curr_e).lower().find("18:00 to ") == -1) ):
                    banner_name = banner_name + str(curr_e)
                else:
                    banner_date = curr_e
                curr_e = curr_e.next_sibling
            
            
            if (banner_name.find(' <font class="notice">※') != -1):
                banner_name = banner_name.replace('<font class="notice">※','-',1)
            elif (banner_name.replace('<font class="notice">※',' -',1)):
                banner_name = banner_name.replace('<font class="notice">※',' -',1)
            banner_name = banner_name.replace('</font>','',1)
            banner_name = banner_name.replace('<br/>','',100)
            banner_name = banner_name.replace('※','',10)
            
            banner_datetime = datetimesplit(banner_date, i+2)
            banner_date = datesplit(banner_date, i+2)
            
            combination_list = banner.find_all(class_='desc')[0].prettify().split('<td class="desc">')
            del combination_list[0]
            ser, ce = combination_list
            ser =ser.split('\n')
            ce =ce.split('\n')
            ser = [s.strip() for s in list(filter(delete, ser))]
            ser = list(map(parseURL, ser))
            ce = [s.strip() for s in list(filter(delete, ce))]
            
            k=0
            while k<len(ce):
                if ce[k][0] == '★':
                    del ce[k]
                elif ce[k].find('craft_essence_profile') != -1:
                    if not re.findall(r'\w+_\w+\.\w+\?\w+=\d+#*\w+', ce[k]):
                        del ce[k]
                    else:
                        reg = re.findall(r'\w+_\w+\.\w+\?\w+=\d+#*\w+', ce[k])[0]
                        ce[k] = "http://fate-go.cirnopedia.org/" + reg
                        k+=1
                else:
                    k+=1
                    
            gacha[str(i)][banner_name] = {}
            gacha[str(i)][banner_name]['Name'] = banner_name
            gacha[str(i)][banner_name]['Date'] = banner_date
            gacha[str(i)][banner_name]['datetime'] = banner_datetime
            gacha[str(i)][banner_name]["Servants"] = {}
            gacha[str(i)][banner_name]['CE'] = {}
            
            j = 0
            while j<len(ser):
                if ser[j+3].find('&amp;') != -1:
                    ser[j+3] = ser[j+3].replace('&amp;', '&', 1)
                if ser[j+1].find('&amp;') != -1:
                    ser[j+1] = ser[j+1].replace('&amp;', '&', 1)
                gacha[str(i)][banner_name]["Servants"][ser[j+3]] = {}
                gacha[str(i)][banner_name]["Servants"][ser[j+3]]['Name'] = ser[j+2] + " " + ser[j+1]
                gacha[str(i)][banner_name]["Servants"][ser[j+3]]['URL'] = ser[j]
                
                sersort(ser[j+2] + " " + ser[j+1], banner_name, serlist, serdict, banner_date, banner_datetime)
                
                j+=4
            
            j= 0
            while j<len(ce):
                gacha[str(i)][banner_name]["CE"][ce[j+3]] = {}
                gacha[str(i)][banner_name]["CE"][ce[j+3]]['Name'] = ce[j+2] + " " + ce[j+1]
                gacha[str(i)][banner_name]["CE"][ce[j+3]]['URL'] = ce[j]
                j+=4
                
                
                
    with open(dir_path + '/Database/gacha' + '.pkl', 'wb') as f:
        pickle.dump(gacha, f, pickle.HIGHEST_PROTOCOL)
    with open(dir_path + '/Database/serlist' + '.pkl', 'wb') as f:
        pickle.dump(serlist, f, pickle.HIGHEST_PROTOCOL)
    with open(dir_path + '/Database/serdict' + '.pkl', 'wb') as f:
        pickle.dump(serdict, f, pickle.HIGHEST_PROTOCOL)
        
    await ctx.send("Database reloaded.")