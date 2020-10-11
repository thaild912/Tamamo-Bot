import discord
from discord.ext import commands
import time
import json
import os
import asyncio
import redis
from user import *
r = redis.from_url(os.environ.get("REDIS_URL"))


    
    
    
class Servant:
    name = ''
    color = 0
    url = ''
    ctx = None
    dir_path =''
    channel = None
    
    def __init__(self, ctx, name, channel = None):
        self.ctx = ctx
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = dir_path
        self.channel = channel
        with open(dir_path + "/Database/info.json") as f:
            data = json.loads(f.read())
            self.name = name
            self.color = int(data["Persona"][name]["Color"],16)
            self.url = data["Persona"][name]["Expression"]["Normal"]["URL"]
    
        
    def changeEx(self, ex):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + "/Database/info.json") as f:
            data = json.loads(f.read())
            self.url = data["Persona"][self.name]["Expression"][ex]["URL"]
     
                    
    async def dialogbox(self, message, footer = None):
        embed=discord.Embed(title=" " , color=self.color)
        embed.set_author(name=self.name)
        embed.set_thumbnail(url=self.url)
        embed.add_field(name="\u200b", value = message, inline=False)
        if footer:
            embed.set_footer(text = footer)
        if self.ctx:
            await self.ctx.send(embed = embed)
        elif self.channel:
            await self.channel.send(embed =embed)
    
    
    
    async def convbox(self, message, footer = None):
        embed = discord.Embed(title = message, color = self.color)
        if footer:
            embed.set_footer(text = footer)
        if self.ctx:
            await self.ctx.send(embed = embed)
        elif self.channel:
            await self.channel.send(embed =embed)
        
    
    
    async def rabbitbox(self, message, tag, punct = '', footer = None,):
        embed = discord.Embed(title = "", color = self.color)
        embed.add_field(name=message, value = "*%s-kun*" %tag + "_%s_" %punct, inline=False)
        if footer:
            embed.set_footer(text = footer)
        if self.ctx:
            await self.ctx.send(embed = embed)
        elif self.channel:
            await self.channel.send(embed =embed)
        
        
    async def imagebox(self,message, url, footer = None):
        embed = discord.Embed(title = message, color = self.color)
        embed.set_image(url=url)
        if footer:
            embed.set_footer(text = footer)
        if self.ctx:
            await self.ctx.send(embed = embed)
        elif self.channel:
            await self.channel.send(embed =embed)
        
        
        
    async def boorubox(self, source, file_url, message = None):
        embed = discord.Embed(title='', color = self.color)
        embed.set_author(name = self.name, icon_url = self.url)
        if message:
            embed.add_field(name=message, value = "\u200b", inline=False)
        if source.find("e-hentai") != -1:
            embed.add_field(name = "\u200b", value = "Please use _[SauceNao](https://saucenao.com/index.php)_ for source.", inline = False )
        else:
            embed.add_field(name = "\u200b", value = "***[Source](%s)***" %source, inline = False )
        embed.set_image(url = file_url)
        await self.ctx.send(embed = embed)
        
#---------------------------------------------------------------------------------------------------------------------------
async def henshindiag(servant, tag, discovered = False):
    ctx = servant.ctx
    bond = getbond(ctx.author.id)
    mname = (ctx.guild.get_member(ctx.author.id).display_name)
    if servant.name == 'Tamamo no Mae':
        await servant.dialogbox("Greetings Master %s." %mname)
        await enhsleep(ctx, 1)
        if not discovered:
            await servant.convbox("Tamamo no Mae, reporting!~")
        else:
            await servant.convbox("Your beloved Casko has come back.")
            await enhsleep(ctx, 1)
            await servant.convbox("I will continue to try to be the best wife ever for you, Mikon!")
            
            
    elif servant.name == "Tamamo Cat":
        await servant.dialogbox("Woof! Cat is here, Master %s!" %mname, "ʷᵃᵍ ʷᵃᵍ")
        await enhsleep(ctx, 1)
        await servant.imagebox("Please pet me Master! =uwu=", 'https://i.imgur.com/2qaXLhF.jpg', "ʷᵃᵍ ʷᵃᵍ")
        
    
    elif servant.name == "Tamamo Summer":
        if bond<80:
            await servant.dialogbox("Hello Master %s! Tamamo Summer is here~!" %mname)
            await enhsleep(ctx, 1)
            await servant.convbox("The weather is beautifu today, so why not change into swimsuit and enjoy ourselves on the beach, Master!")
            await enhsleep(ctx, 1)
        elif bond>=80:
            await servant.dialogbox("Hello Master %s! Tamamo Shark is here~!" %mname)
            await enhsleep(ctx, 1)
            await servant.convbox("What? You are asking why I used the nickname 'Tamamo Shark' instead of 'Tamamo Summer'?")
            await enhsleep(ctx, 1)
            await servant.convbox("You know shark likes to eat people riiight?")
            await enhsleep(ctx, 1)
            await servant.convbox("Well, the same goes for me...")
            await enhsleep(ctx, 1)
            await servant.convbox("Master...you look too delicious....")
            await enhsleep(ctx, 1)
            await servant.imagebox("It would be a waste...to not devour you all...m.a.s.t.e.r...", 'https://i.imgur.com/3pXbUlU.png', 'ᵘᶠᵘᶠᵘ♡')
        
        
    elif servant.name == "Tamamo Vicchi":
        await servant.dialogbox("Rest assured, Master %s, for your Tamamo Vicchi is here." %mname)
        await enhsleep(ctx, 1)
        await servant.convbox("Whether it's office works, infiltration, espionage or assassinations, I will get it done.")
        
    else:
        if bond<80:
            await servant.dialogbox("Caster Tamamo Rabbit, your personal Strategist is here.")
            await enhsleep(ctx, 1)
            await servant.convbox("I guess you didn't just call me out for shits and giggles right?")
            await enhsleep(ctx, 1)
            await servant.convbox("So speak up, what kind of bussiness do you need my help with?")
            await enhsleep(ctx, 1)
        elif bond>=80:
            await servant.dialogbox("Caster Tamamo Rabbit, your personal Strategist/Girlfriend is here.")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("Ara, I see that you have been acting unbelievably stupid and reckless since I were gone, right ", tag, "?")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("As expected of you, having become totally dependent on me, you are not able to do anything properly anymore, ", tag, ".")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("But please refrain yourself from acting rashly from now on, as it would be troubling to the medical staff and Mashu, and other Tamamo if you get injured in the middle of you action, ", tag, ".")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("Otherwise I will not forgive you the next time you injured yourself due to not using your brain, ", tag, ".")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("What, I'm being to harsh on you, ", tag, "?")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("Are you perhaps expecting me to be sweeter toward you because I'm your girlfriend, ", tag, "?")
            await enhsleep(ctx, 1)
            await servant.convbox("Then it's impossible, I'm a tsundere after all.")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("And isn't that a Strategist/Girlfriend 's responsibility is to keep their loved one, in this case, you, alive, right ", tag, "?")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("So stop complaining, be grateful and do as I said, ", tag, ".")
            await enhsleep(ctx, 1)
            await servant.convbox("Idiot.")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("Just kidding. Did you think I would really say that, ", tag, "?")
            await enhsleep(ctx, 1)
            await servant.rabbitbox("On the second thought, I might actually say that. Since your IQ is indeed that low after all, ", tag, ".")
        


async def enhsleep(ctx, second):
    await ctx.channel.trigger_typing()
    time.sleep(second)
    
    
    
    
async def splitpage(bot, ctx, page, maxpage):
    servant = Servant(ctx, "Tamamo Rabbit")
    await servant.dialogbox('This is the end of part %d/%d.' %(page, maxpage))
    await enhsleep(ctx, 1)
    await servant.convbox('Do you want to continue reading?(y/n)', 'ᵗᶦᵐᵉᵒᵘᵗ ¹⁵ˢ')
    
    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', check=pred, timeout =15.0)
    except asyncio.TimeoutError:
        await servant.dialogbox("I understand.")
        return False
    else:
        if msg.content.lower() == 'y' or msg.content.lower() == 'yes':
            await servant.dialogbox("Thank you. I will continue playing the intro.")
            return True
        elif msg.content.lower() == 'n' or msg.content.lower() == 'no':
            await servant.dialogbox("I understand.")
            await enhsleep(ctx, 1)
            await servant.convbox("The intro will be stopped and process will be saved.")
            return False
        else:
            await servant.dialogbox("...")
            return False
    

async def pagesethelper(bot, ctx, maxpage):
    Rabbit = Servant(ctx, "Tamamo Rabbit")
    
    await Rabbit.dialogbox("Looks like what you've entered is not a number or an invalid number. Please try again.")
    await enhsleep(ctx,1)
    await Rabbit.convbox("Please enter a number after this line (max page number is %d):" %maxpage, '²⁰ˢ ᶜᵒᵒˡᵈᵒʷⁿ ⁻ ᶠᵃᶦˡ ᵗᵒ ᵉⁿᵗᵉʳ ᵗʰᵉ ʳᶦᵍʰᵗ ᶠᵒʳᵐᵃᵗ ʷᶦˡˡ ᵇᵉ ʰᵉᵃᵛʸ ˢᵃⁿᶜᵗᶦᵒⁿᵉᵈ')
    
    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel

    
    try:
        msg = await bot.wait_for('message', check=pred, timeout =20.0)
    except asyncio.TimeoutError:
        await Rabbit.dialogbox("No input received. Please try again later.")
        await enhsleep(ctx,1)
    else:
        
        try:
            pnum = int(msg.content)
        except ValueError:
            await Rabbit.dialogbox("Wrong format.")
            await enhsleep(ctx,1)
            await Rabbit.convbox("You are not fit to be our Master.")
            sanction(ctx.author.id)
            return False
        else:
            if pnum <0:
                await Rabbit.dialogbox("Done playing around?")
                await enhsleep(ctx,1)
                await Rabbit.convbox("You are not fit to be our Master.")
                sanction(ctx.author.id)
                return False
            elif pnum==0 or pnum >maxpage:
                await Rabbit.dialogbox("Page number should be between 1 and %d." %maxpage)
                await enhsleep(ctx,1)
                await Rabbit.convbox("Please try again later.")
                return False
            else:
                setpage(ctx.author.id, pnum)
                await Rabbit.dialogbox("Page set.")
                return True
            
async def checkpoint(ctx,bondreq):
    servant = Servant(ctx,"Tamamo Rabbit")
    adopted = getadopt(ctx.author.id)
    bond = getbond(ctx.author.id)
    if not adopted:
        await enhsleep(ctx, 1)
        await servant.dialogbox('Sorry, but you will need to adopt us first for us to use this function.', 'Consult <3adopt for more information.')
        return False
    if bond<bondreq:
        if bond == 0:
            pass
        await enhsleep(ctx, 1)
        await servant.dialogbox("Sorry, you need to reach bond level %d to use this function." %(bondreq//10), 'Consult <3bond for more information.')
        return False
    return True
    