import discord
from discord.ext import commands
import time
import re
import sys
import json
import requests
import os
from tamaLINE import *
from PIL import Image, ImageDraw, ImageFont
from user import *
import redis

#need to be a class
class TrackMessage(commands.Cog):
    #init
    def __init__(self, bot):
        self.bot = bot
     
    #cog listener
    @commands.Cog.listener()
    async def on_message(self, message):
        global ctr
        text = re.findall(r'(\w+)', message.content.lower())
        text = ''.join(text)
        
        # so you can't change the master variable from here
        # considering go back to using json
        # and going back to using json meaning everything used 'mode' will have to be imported from json everytime
        # so for now I will stick with this until a cog that requires changing roles comes up 
        if text.find("slap") != -1 and message.author.id != int(tamamo) and message.author.id != 605219399980285955:
            
            slapper = message.guild.get_member(message.author.id).display_name
            #print(message.content)
            lr = 0
            slapped = False
            temp = ''
            if len(message.mentions) == 0:
                file = discord.File(dir_path +"/Pictures/slap.png")
                await message.channel.send(file = file)
                
            for i in message.mentions:
                if slapped:
                    slapper = temp
                    slapped = False
                    
                name = message.guild.get_member(i.id).display_name
                
                #anti slap
                if i.id == int(tamamo):
                    temp = slapper
                    slapper = message.guild.get_member(int(tamamo)).display_name
                    name = temp
                    slapped = True
                
                im = Image.open(dir_path+'/Pictures/slap.jpg').copy()
                font = ImageFont.truetype(dir_path+ '/Fonts/MS Gothic.ttf', size= 80)
                color = (255,255,0)
                if lr%2 == 0:
                    draw = ImageDraw.Draw(im)
                    w,h = draw.textsize(name, font = font)
                    draw.text((350-w//2,380-h//2), name,font=font,fill=color)
                    w2,h2 = draw.textsize(slapper, font = font)
                    draw.text((730-w2//2,120-h2//2), slapper,font=font,fill=color)
                    im.save(dir_path+'/Pictures/slaptemp.jpg')
                    
                else:
                    im = im.transpose(Image.FLIP_LEFT_RIGHT)
                    draw2 = ImageDraw.Draw(im)
                    w,h = draw.textsize(name, font = font)
                    draw2.text((700+(700-(350-w//2))-w,380-h//2), name,font=font,fill=color)
                    w2,h2 = draw.textsize(slapper, font = font)
                    draw2.text((700+(700-(730-w2//2))-w2,120-h2//2), slapper,font=font,fill=color)
                    im.save(dir_path+'/Pictures/slaptemp.jpg')
                
                file = discord.File(dir_path +"/Pictures/slaptemp.jpg")
                await message.channel.send(file = file)
                lr+=1
                
                
                # nope still cant change
                #mode = 'Cat'
                
            #elif mode == 'Cat':
            #   servant = Servant(None, "Tamamo Cat", message.channel)
            #    await servant.dialogbox("cat")
                
                
        elif (text.find("lenny") != -1 or message.content.find("( ͡° ͜ʖ ͡°)") != -1) and message.author.id != int(tamamo):
            await message.channel.send('( ͡° ͜ʖ ͡°)')
            file = discord.File(dir_path +"/Pictures/smirk.jpg")
            await message.channel.send(file = file)
            
        elif (text.find("it's") !=-1 or text.find("its") != -1) and text.find("him") !=-1 and text.find("officer") !=-1:
            file = discord.File(dir_path +"/Pictures/officer.jpg")
            await message.channel.send(file = file)
            
        #emoji    
        elif message.content.find(":") !=-1 and message.content.find("<3addemoji") == -1 and message.author.id != int(tamamo) and message.author.id != 605219399980285955:
            r = redis.from_url(os.environ.get("REDIS_URL"))
            emo = re.findall(r':[A-Za-z0-9]+:', message.content)
            data = json.loads(r.get('guild'))
            for e in emo:
                if str(message.channel.guild.id) in data:
                    if e in data[str(message.channel.guild.id)]:
                        useEmoji(message.author.id)
                        url = data[str(message.channel.guild.id)][e]
                        with open(dir_path +'/Pictures/gif_temp.gif', 'wb') as g:
                            try:
                                g.write(requests.get(url).content)
                            except:
                                await message.channel.send("URL error, please delete %s" %e)
                            else:
                                file = discord.File(dir_path +'/Pictures/gif_temp.gif')
                                await message.channel.send(file = file)
                                    
                
                
                
        if message.author.id == int(sukvatID):
            if ctr ==9:
                await message.channel.send("Please refrain from spamming R6S/Dotard contents, %s." %sukvat)
                time.sleep(1)
                ctr =0;
            else:
                ctr = ctr +1
                
            if text.find('bot') !=-1 and text.find('ngu') !=-1:
                await message.channel.send("Không m mới ngu ý.")
            
        '''elif message.author.id == int(kiaraID):
            await message.channel.send("Slap %s" %kiara)'''
                
        if message.author.id == int(ikarosID):
            #print(message)
            if message.content.lower().find('%s exploded' %kiara) !=-1:
                file = discord.File(dir_path +'/Pictures/nuked.png')
                await message.channel.send(file = file)
            
    # cog commands   
    @commands.command()
    async def tcog(self, ctx):
        await ctx.send("Hmmm")
        
#needs to be on the same indent as the Class     
def setup(bot):
    #for main bot to add the cog
    bot.add_cog(TrackMessage(bot))
    
    # importing the variables in main for cog to use
    # !!! this only happens at the setup of the cogs, so anytime you changes the imported variable, it needs to be reloaded
    # was going to use json to read and write into the main but you will have to load json every now and then, so meh.
    from tamamo import dir_path, sukvat, tamamo, remine, sukvatID, kiara, kiaraID, ikarosID
    global dir_path, sukvat, tamamo, remine, sukvatID, kiara, kiaraID, ikarosID
    global ctr
    ctr = 0
    