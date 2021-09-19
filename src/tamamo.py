import discord
from discord.ext import commands
from discord.ext import tasks
import json
import os
import asyncio
import redis
from discord.utils import get
import youtube_dl
import glob
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))
intents = discord.Intents(messages=True,
                          guilds=True,
                          members=True,
                          presences=True,
                          reactions=True,
                          typing=True,
                          voice_states=True)

debug = False
if debug:
    with open(dir_path + "/Database/info.json") as f:
        data = json.loads(f.read())
        os.environ["REDIS_URL"] = data['Server']['Redis']

from user import *
from tamaLINE import *
from tamAPI import *
from tamaDB import *
from tamaGuild import *
from tamaSing import *

version = 'v.0.9.8'
bot = commands.Bot(command_prefix=['<3', '!'], intents=intents)
bot.remove_command("help")
guild_music_objs = {}

with open(dir_path + "/Database/info.json") as f:
    data = json.loads(f.read())

    ikaros = data['People']['Ikaros']['Callable']
    ikarosID = data['People']['Ikaros']['ID']
    luella = data['People']['Luella']['Callable']
    zeeees = data['People']['Zeeees']['Callable']
    remine = data['People']['Remine The Cat']['Callable']
    remineID = data['People']['Remine The Cat']['ID']
    kypxz = data['People']['KypxZ']['Callable']
    amagiri = data['People']['AmagiriAyato']['Callable']
    sukvat = data['People']['SukvatELuck']['Callable']
    sukvatID = data['People']['SukvatELuck']['ID']

    tamamo = data['Bots']['TamamoBot']['ID']
    kiara = data['Bots']['KiaraBot']['Callable']
    kiaraID = data['Bots']['KiaraBot']['ID']

    token = data['Server']['BotToken']

    if debug:
        token = data['Server']['DebugClientToken']

    clientID = data['Server']['ClientID']
    testID = data['Server']['PrimTestID']
    channelID = data['Server']['PrimChannelID']

if not debug:
    bot.load_extension("cogs.trackmessage")
bot.load_extension("cogs.trackstatus")


@bot.event
async def on_ready():
    print("Tamamo bot %s \nTo serve and will be of service." % version)
    if debug:
        print("Logged in as Tamamo Dev")

    check_audio.start()


@commands.cooldown(1.0, 5.0, commands.BucketType.user)
@bot.command(aliases=['halp'])
async def help(ctx):
    servant = Servant(ctx, "Tamamo of Knowledge")

    color = servant.color
    url = servant.url

    embed = discord.Embed(title="Tamamo help", description="Commands: either '<3' or '!' prefix is ok.", color=color)
    embed.set_author(name="Tamamo of Knowledge")
    embed.set_thumbnail(url=url)
    embed.add_field(name="<3intro", value="**A brief introduction about us. Please be serious.**\n120s cooldown.",
                    inline=False)
    embed.add_field(name="<3welcome", value="**Send a heart warming welcome, not from me.**\n30s cooldown.",
                    inline=False)
    embed.add_field(name="<3henshin <persona>",
                    value="**Changes persona. Set parameter empty to change to the next available persona. In the case that you need help, which is almost a certainty, then remember that <3henshin help exists.**\n30s cooldown.",
                    inline=False)
    embed.add_field(name="<3help", value="**You are already here. What are you expecting?\n5s cooldown.", inline=False)
    embed.add_field(name="<3purge <limit>",
                    value="**Vicchi's cleanup service. Parameter is the number of targets.**\n5s cooldown.",
                    inline=False)
    embed.add_field(name="<3upcomingbanner <number>",
                    value="**Show <number> of upcoming banner in FGONA.**\n60s cooldown", inline=False)
    embed.add_field(name="<3selfie",
                    value="**Show a cute picture of the cutest creature in the universe, which happens to share the same appearance as me.**\n10s cooldown",
                    inline=False)
    embed.add_field(name="<3fetchPDT", value="**Return PDT time for FGONA coordination.**\n5s cooldown", inline=False)
    embed.add_field(name="<3rateup <servant name>",
                    value="**Show upcomming rateup for a specific servant. Do me a favor and consult <3rateup help before doing anything stupid, will you?**\n30s cooldown.",
                    inline=False)
    embed.set_footer(text="Tamamo bot %s by Ikaros#5345" % version)

    # send embeded message
    await ctx.send(embed=embed)

    # deleting command
    await ctx.message.delete()


@commands.cooldown(1.0, 30.0, commands.BucketType.user)
@bot.command()
async def welcome(ctx):
    try:
        adopted = getadopt(ctx.author.id)
    except KeyError:
        pass
    mode = getmode(ctx.author.id)
    discovered = getuserdisc(ctx.author.id)
    mname = (ctx.guild.get_member(ctx.author.id).display_name)
    bond = getbond(ctx.author.id)
    incbond(ctx.author.id)

    Tamamo = Servant(ctx, "Tamamo no Mae")
    Cat = Servant(ctx, "Tamamo Cat")
    Shark = Servant(ctx, "Tamamo Summer")
    Vicchi = Servant(ctx, "Tamamo Vicchi")
    Knowledge = Servant(ctx, "Tamamo of Knowledge")

    if not await checkpoint(ctx, adopted, bond, 30):
        return

    if mode == 'OG':

        if not discovered:
            await Tamamo.dialogbox("Mikon! Welcome home Master!")
        else:
            await Tamamo.dialogbox("Mikon! Welcome home My Husband %s." % mname)
            await enhsleep(ctx, 1)
            await Tamamo.convbox("Do you want dinner first?")
            await Tamamo.convbox("Or bath first?");
            await enhsleep(ctx, 1)
            await Tamamo.convbox("Or perhaps...");
            await enhsleep(ctx, 1)
            await Tamamo.convbox("わ。");
            await enhsleep(ctx, 1)
            await Tamamo.convbox("た。");
            await enhsleep(ctx, 1)
            await Tamamo.convbox("し。", "ᵘᶠᵘᶠᵘ♡")

            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = ''
                msg = await bot.wait_for('message', check=pred, timeout=30.0)
            except asyncio.TimeoutError:
                return
            else:
                if msg.content.lower().find('dinner') != -1:
                    await Tamamo.dialogbox('Yes, Tamamo will gladly show My Husband the power of my housewife skill.')
                    await enhsleep(ctx, 1)
                    await Tamamo.convbox("Time to put these lesson I've learned in Benni-enma's class into action!")

                elif msg.content.lower().find('bath') != -1:
                    await Tamamo.dialogbox("I've prepared the water and the bath for you, My Husband. Please get in.")
                    await enhsleep(ctx, 1)
                    # blush

                    await Tamamo.dialogbox(
                        "Or..perhaps...you want us to get in together and clean each other's back, My Husband...?")
                    try:
                        msg = await bot.wait_for('message', check=pred, timeout=30.0)
                    except asyncio.TimeoutError:
                        await Tamamo.dialogbox("Still indecisive?")
                        await enhsleep(ctx, 1)
                        await Tamamo.convobox(
                            "Then it's decided. Tamamo will be the one to give My Husband the best back cleaning ever.")
                        await enhsleep(ctx, 1)
                        await Tamamo.convbox("And you know it's not limited to back either right?", '*ʷᶦⁿᵏ ʷᶦⁿᵏ')

                    else:

                        if msg.content.lower().find('yes') != -1:
                            # still blush
                            await Tamamo.dialogbox(
                                "Then it's decided. Tamamo will be the one to give My Husband the best back cleaning ever.")
                            await enhsleep(ctx, 1)
                            await Tamamo.convbox("And you know it's not limited to back either right?", '*ʷᶦⁿᵏ ʷᶦⁿᵏ')

                        elif msg.content.lower().find('no') != -1:
                            # sad
                            await Tamamo.convbox(
                                "*sob sob. And I was going to give you the best back cleaning ever, My Husband.")
                            # change expression to normal
                            await Tamamo.dialogbox("But well, that alone won't be able to discourage me.")
                            await enhsleep(ctx, 1)
                            await Tamamo.convbox(
                                'Please get in the bath, My Husband, and in the meanwhile I will prepare you a dinner.')
                            await enhsleep(ctx, 1)
                            await Tamamo.convbox(
                                "If I can't take down you with my superior housewife back-cleaning skill then I will do it with my cooking skill.")
                            await enhsleep(ctx, 1)
                            await Tamamo.convbox("Please look forward to it, My Husband!")


                elif msg.content.lower().find('you') != -1 or msg.content.lower().find(
                        'tamamo') != -1 or msg.content.lower().find('wife') != -1:
                    await Tamamo.convbox("Gasp! My Husband has finally awoken his libido.", 'ᵍʳᵉᵃᵗ ʲᵒᵇ ᵐʸ ˢᵉˡᶠ')
                    await enhsleep(ctx, 1)
                    await Tamamo.convbox("But my heart isn't ready for this! Kyaa!")
                    # change to blush
                    await enhsleep(ctx, 1)
                    await Tamamo.dialogbox("So if you don't mind, %s..." % mname)
                    await enhsleep(ctx, 1)
                    await Tamamo.convbox("...could you please take the lead...?")




    elif mode == 'Cat':

        await Cat.dialogbox("Woof! Welcome back, Master %s. How was your day?" % mname, "ʷᵃᵍ ʷᵃᵍ")
        await enhsleep(ctx, 1)
        await Cat.convbox(
            "You must be hungry. But don't worry because Cat has already cooked you a dinner! Sit down and eat up, Master!",
            "ʷᵃᵍ ʷᵃᵍ")
        await enhsleep(ctx, 1)



    elif mode == 'Vicchi':

        await Vicchi.dialogbox("Welcome, Master %s. Looks like you have worked hard today." % mname)
        await enhsleep(ctx, 1)
        await Vicchi.convbox("I've taken the liberty of booking a table for us at the nearby formal restaurant.")
        await enhsleep(ctx, 1)
        await Vicchi.convbox("Now if you'll excuse me, I'll help you change your attire, and then we will go out.",
                             "ʰᵃⁿᵈ ʷᵃⁿᵈᵉʳˢ")



    elif mode == 'Knowledge':
        if bond < 80:
            await Knowledge.dialogbox("Ara, isn't that my stupid master?")
            await enhsleep(ctx, 1)
            await Knowledge.convbox("Welcome home.")

        elif bond >= 80:
            await Knowledge.dialogbox("Ara, looks who have done messing around, %s-kun." % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox("Ara, I do not look like I'm was awaiting to your return, you say?")
            await enhsleep(ctx, 1)
            await Knowledge.convbox("Why should I, %s-kun?" % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox("It's becaise I'm your girlfriend, %s-kun?" % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox(
                "Very well. Since you have said such sincere thing, and since I'm such an awesome girlfriend, I will let you go this time.",
                "ᵈᵒⁿ'ᵗ ᵖᵘˢʰ ʸᵒᵘʳ ˡᵘᶜᵏ ᵃᵍᵃᶦⁿ")
            await enhsleep(ctx, 1)
            await Knowledge.convbox(
                "Then, for dinner, your wonderful girlfriend, me, in particular, have prepared the ingredients for your favorite meal. Be grateful, %s-kun." % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox(
                "Also, I've gone out of my way prepared the bath for you, so hurry up and get in so I can clean your back, %s-kun." % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox(
                "After bath, I shall grant you the privilege to fluff my tail all you want while I cook your dinner, so look forward to it, %s-kun." % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox("What will we have for dessert? Ara, aren't you greedy, %s-kun?" % mname)
            await enhsleep(ctx, 1)
            await Knowledge.convbox("It will be Me, with chocolate on top, of course.")
            await enhsleep(ctx, 1)



    elif mode == 'Summer':
        if bond < 80:
            await Shark.dialogbox("Mikon! Welcome home Master!")
            await enhsleep(ctx, 1)
            await Shark.convbox(
                "Looks like you've had a hardworking day. Perhaps you would want a back massage, Master?")

            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await bot.wait_for('message', check=pred, timeout=30.0)
            except asyncio.TimeoutError:
                await Shark.dialogbox("Poor Master, he must be really tired.")
            else:
                if msg.content.lower().find('yes') != -1:
                    await Shark.dialogbox('Mikon! Roger that!')
                    incbond(ctx.author.id)
                elif msg.content.lower().find('no') != -1:
                    await Shark.dialogbox('Well if you ever need one then I will always be available!')

        elif bond >= 80:
            await Shark.dialogbox("Panpakapan! Welcome back to our love nest, Master %s!" % mname)
            await enhsleep(ctx, 1)
            await Shark.convbox("Heavens me, you must be tired form all the works.")
            await enhsleep(ctx, 1)
            await Shark.convbox("Don't worry, I know something that can relieve your stress! It's Bathing!")
            await enhsleep(ctx, 1)
            await Shark.convbox("So come on Master! Let's get into the bath!")
            await enhsleep(ctx, 1)
            await Shark.convbox("I will make sure that you drown in heavenly pleasure! Mikon!", "ʰᵉʰᵉʰᵉʰ")
            await enhsleep(ctx, 1)
            await Shark.convbox(
                "Now, please don't make a lady wait and get in the bath, Master. Else, you will why people called me 'Beast of Summer ♡'.")


@commands.cooldown(1.0, 30.0, commands.BucketType.user)
@bot.command(aliases=['transform'])
async def henshin(ctx, message=None):
    mode = getmode(ctx.author.id)
    discovered = getuserdisc(ctx.author.id)
    mname = (ctx.guild.get_member(ctx.author.id).display_name)
    incbond(ctx.author.id, 1)

    Tamamo = Servant(ctx, "Tamamo no Mae")
    Cat = Servant(ctx, "Tamamo Cat")
    Shark = Servant(ctx, "Tamamo Summer")
    Vicchi = Servant(ctx, "Tamamo Vicchi")
    Knowledge = Servant(ctx, "Tamamo of Knowledge")

    if not await checkpoint(ctx, 0):
        return

    if message:
        if not message.lower() in ['og', 'vicchi', 'cat', 'summer', 'knowledge', 'x', 'help']:

            await Knowledge.dialogbox("Henshin failed.", "ʳᵉᵃˡˡʸˀ")
            await enhsleep(ctx, 1)
            await Knowledge.convbox(
                "There is only a few of us, and most of our names are cutesy, yet you can't remember them.",
                "ᴴᵒʷ ᵘᵗᵗᵉʳˡʸ ᵈᵉˢᵖᶦᶜᵃᵇˡᵉ")
            await enhsleep(ctx, 1)
            await Knowledge.convbox("We are dissapointed.", "ᵖˡᵉᵃˢᵉ ᵇᵉᵍᵒⁿᵉ")
            await enhsleep(ctx, 1)
            await Knowledge.convbox("Go consult !help for more information regarding this command.")
            incbond(ctx.author.id, -2)

        elif message.lower() == 'help':
            color = Knowledge.color
            url = Knowledge.url
            name = Knowledge.name

            embed = discord.Embed(title="Henshin.help",
                                  description="Well at least this time that decorative brain of yours know how to ask for help. So I will do you a favor out of kindness and give you the parameters:",
                                  color=color)
            embed.set_author(name=name)
            embed.set_thumbnail(url=url)
            embed.add_field(name="Knowledge", value="**Changes persona to the smart, lovable and superior Tamamo.**",
                            inline=False)
            embed.add_field(name='OG', value='**Changes persona to the inferior Tamamo.**', inline=False)
            embed.add_field(name='Cat', value='**Changes persona to that Cat.**', inline=False)
            embed.add_field(name='Vicchi', value='**Changes persona to Bicchi.**', inline=False)
            embed.add_field(name='Summer or Shark', value='**Changes persona to the horny Original.**', inline=False)
            embed.add_field(name='Leave the field blank to', value='**Changes persona to the next one available.**',
                            inline=False)
            embed.set_footer(
                text="And in case that little brain of you forget, all the parameters are not case sensitive.")
            await ctx.send(embed=embed)
            await enhsleep(ctx, 2)

            await Tamamo.dialogbox("Wait, why am I the only one getting the inferior treatment!")

        elif message.lower() == 'og':
            mode = 'OG'
            await henshindiag(Tamamo, ikaros, discovered)

        elif message.lower() == 'cat':
            mode = 'Cat'
            await henshindiag(Cat, ikaros)

            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await bot.wait_for('message', check=pred, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send('<@%s> left without petting Cat.' % str(ctx.author.id))
                incbond(ctx.author.id, -1)
            else:
                if msg.content.lower().find('pet') != -1 or msg.content.lower().find('pat') != -1:
                    await Cat.dialogbox('Thank you Master! I love you!', 'ʷᵃᵍ ʷᵃᵍ')
                    incbond(ctx.author.id, 1)
                else:
                    await ctx.send('<@%s> left without petting Cat.' % str(ctx.author.id))
                    incbond(ctx.author.id, -1)
                    # change expression

        elif message.lower() == 'summer' or message.lower() == 'shark':
            mode = 'Summer'
            await henshindiag(Shark, ikaros)

        elif message.lower() == 'vicchi':
            mode = 'Vicchi'
            await henshindiag(Vicchi, ikaros)

        elif message.lower() == 'knowledge':
            mode = 'Knowledge'
            await henshindiag(Knowledge, ikaros)

    else:
        x = 0
        if mode == 'OG':
            x = 0
        elif mode == 'Cat':
            x = 1
        elif mode == 'Summer':
            x = 2
        elif mode == 'Vicchi':
            x = 3
        elif mode == 'Knowledge':
            x = 4
        x += 1
        if x >= 5:
            x = 0

        if x == 0:
            mode = 'OG'
            await henshindiag(Tamamo, ikaros, discovered)

        elif x == 1:
            mode = 'Cat'
            await henshindiag(Cat, ikaros)

            def pred(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await bot.wait_for('message', check=pred, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.send('<@%s> left without petting Cat.' % str(ctx.author.id))
                incbond(ctx.author.id, -1)
            else:
                if msg.content.lower().find('pet') != -1 or msg.content.lower().find('pat') != -1:
                    await Cat.dialogbox('Thank you Master! I love you!', 'ʷᵃᵍ ʷᵃᵍ')
                    incbond(ctx.author.id, 1)
                else:
                    await ctx.send('<@%s> left without petting Cat.' % str(ctx.author.id))
                    incbond(ctx.author.id, -1)

            # change expression

        elif x == 2:
            mode = 'Summer'
            await henshindiag(Shark, ikaros)

        elif x == 3:
            mode = 'Vicchi'
            await henshindiag(Vicchi, ikaros)

        else:
            mode = 'Knowledge'
            await henshindiag(Knowledge, ikaros)

    changemode(ctx.author.id, mode)

    bot.reload_extension("cogs.trackmessage")


@bot.event
async def on_command_error(ctx, error):
    await bot.get_channel(671742964749303827).send(error)

    Knowledge = Servant(ctx, "Tamamo of Knowledge")
    if isinstance(error, commands.CommandOnCooldown):
        await Knowledge.dialogbox("Ara, looks like you can't just stay still for a few second huh?")
        await Knowledge.convbox("Always tampering everywhere..., how childist.", )
        await Knowledge.convbox("Have you ever consider acting like a normal human?")
        print(re.findall(r'\d\d*.\d\d+', str(error))[0])

    elif isinstance(error, commands.CommandNotFound):
        await Knowledge.dialogbox("Ara, Congratulations.")
        await Knowledge.convbox("Your stupidity has successfuly exceeded my expectation.")
        await Knowledge.convbox("There are only a few commands, it is that hard to remember?")
        await Knowledge.convbox("...I'm sorry for being so harsh.")
        await Knowledge.convbox("Sorry. I didn't know that the commands's information exceed your brain's capacity.")
        await Knowledge.convbox("To make up for that, I've made a whole new section for the disabled.", "ⁿᵒ ᴵ ᵈᶦᵈⁿ'ᵗ")
        await Knowledge.convbox("Please consult <3help for commands that you can copy and paste,", "ˡᵒʷ⁻ᶜᵃᵖᵃᶜᶦᵗᶦᵉˢ")

    elif isinstance(error, commands.MissingRequiredArgument):
        await Knowledge.dialogbox("Hmm? You have finally able to remember the command but not the parameters?")
        await Knowledge.convbox("You know very well that a command is useless without its parameters right?")
        await Knowledge.convbox("Just like how you are in real life.")

    raise error


@commands.cooldown(1.0, 10.0, commands.BucketType.user)
@bot.command()
async def selfie(ctx, message=None):
    try:
        mode = getmode(ctx.author.id)
    except KeyError:
        pass
    incbond(ctx.author.id, 1)
    if message:
        if message.lower() != 'nsfw':
            servant = Servant(ctx, "Tamamo of Knowledge")
            await servant.dialogbox(
                "Has watching porn too much hinders your ability to recognize the right parameter to type?")
            incbond(ctx.author.id, -1)
    if mode == 'Knowledge':
        servant = Servant(ctx, "Tamamo of Knowledge")
        if not message:
            await servant.dialogbox("I don't have any.")
            incbond(ctx.author.id, -1)
        elif message.lower() == 'nsfw':
            await servant.dialogbox(
                "If you ask this one more time then the only thing that is nsfw to look at here will be your corpse.")
            incbond(ctx.author.id, -10)
    else:
        if mode == 'OG':
            servant = Servant(ctx, "Tamamo no Mae")
        elif mode == 'Cat':
            servant = Servant(ctx, "Tamamo Cat")
        elif mode == 'Summer':
            servant = Servant(ctx, "Tamamo Summer")
        elif mode == 'Vicchi':
            servant = Servant(ctx, "Tamamo Vicchi")

        await fetch(servant, message)


@commands.cooldown(1.0, 3.0, commands.BucketType.user)
@bot.command(aliases=['PDT', 'pdt', 'fetchpdt'])
async def fetchPDT(ctx):
    try:
        incbond(ctx.author.id, 1)
    except KeyError:
        pass
    await getPDT(ctx)


@commands.cooldown(1.0, 6000, commands.BucketType.user)
@bot.command()
async def update(ctx):
    if ctx.author.id == int(ikarosID):
        t = time.process_time()
        await updateDB(ctx)
        elapsed_time = time.process_time() - t
        await ctx.send("Update took: %d seconds" % elapsed_time)
    else:
        await ctx.send("Only %s can do this." % ikaros)


@commands.cooldown(1.0, 60, commands.BucketType.user)
@bot.command(aliases=['upcoming', 'upcommingbanner', 'upcomingbanner', 'upcommingbanners'])
async def upcomingbanners(ctx, num=3):
    try:
        incbond(ctx.author.id, 1)
    except KeyError:
        pass
    if num > 10:
        servant = Servant(ctx, "Tamamo of Knowledge")
        await servant.dialogbox('...Did you just seriously tried to broke the channel?')
        await enhsleep(ctx, 1)
        await servant.convbox("I won't permit that.")
        await enhsleep(ctx, 1)
        await servant.convbox("Now please go away and make yourself less of a useless being, then come back.")

    now = datetime.datetime.now() + datetime.timedelta(days=7)
    curryear = now.year
    jpyear = curryear - 2
    cur = []
    next = []
    with open(dir_path + '/Database/gacha' + '.pkl', 'rb') as f:
        gacha = pickle.load(f)
        i = 0
        for item in gacha[str(jpyear)]:
            if gacha[str(jpyear)][item]['datetime'] > now:
                if i < num:
                    cur.append(gacha[str(jpyear)][item]['Name'])
                    i += 1
                else:
                    break

        if i < num:
            for item in gacha[str(jpyear + 1)]:
                if i < num:
                    next.append(gacha[str(jpyear + 1)][item]['Name'])
                    i += 1
                else:
                    break

        servant = Servant(ctx, "Tamamo of Knowledge")
        await servant.dialogbox("...You know the rate is only 0.7% right?")
        await enhsleep(ctx, 1)
        await servant.convbox("Well, if you are that dumb then I won't stop you from wasting your lifetime savings.")
        await enhsleep(ctx, 1)
        await servant.convbox("This is on you. Can't believe I'm wasting my Clairvoyance on this...")
        await enhsleep(ctx, 1)
        embed = discord.Embed(title="Upcomming %d banners for FGONA:" % num, color=servant.color)
        await ctx.send(embed=embed)
        for name in cur:
            embed = discord.Embed(title=gacha[str(jpyear)][name]['Name'], description=gacha[str(jpyear)][name]['Date'],
                                  color=servant.color)
            string = ''
            lstring = []
            count = 0
            for item in gacha[str(jpyear)][name]['Servants']:
                if count % 10 != 0 or count == 0:
                    string = string + "[%s]" % gacha[str(jpyear)][name]['Servants'][item]['Name'] + '(%s)' % \
                             gacha[str(jpyear)][name]['Servants'][item]['URL'] + '\n'
                else:
                    lstring.append(string)
                    string = ''
                    string = "[%s]" % gacha[str(jpyear)][name]['Servants'][item]['Name'] + '(%s)' % \
                             gacha[str(jpyear)][name]['Servants'][item]['URL'] + '\n'
                count += 1
            lstring.append(string)

            count2 = True
            for st in lstring:
                if count2:
                    embed.add_field(name='Servants', value=st, inline=False)
                    count2 = False
                else:
                    embed.add_field(name='\u200b', value=st, inline=False)

            if gacha[str(jpyear)][name]['CE']:
                string2 = ''
                for item in gacha[str(jpyear)][name]['CE']:
                    if gacha[str(jpyear)][name]['CE'][item]['Name'].find('3') == -1:
                        string2 = string2 + "[%s]" % gacha[str(jpyear)][name]['CE'][item]['Name'] + '(%s)' % \
                                  gacha[str(jpyear)][name]['CE'][item]['URL'] + '\n'

                if string2:
                    embed.add_field(name='CEs:', value=string2, inline=False)

            await ctx.send(embed=embed)

        if next:
            for name in next:
                embed = discord.Embed(title=gacha[str(jpyear + 1)][name]['Name'],
                                      description=gacha[str(jpyear + 1)][name]['Date'], color=servant.color)
                string = ''
                for item in gacha[str(jpyear + 1)][name]['Servants']:
                    if gacha[str(jpyear + 1)][name]['Servants'][item]['Name'].find('3') != -1:
                        continue
                    else:
                        string = string + "[%s]" % gacha[str(jpyear + 1)][name]['Servants'][item]['Name'] + '(%s)' % \
                                 gacha[str(jpyear + 1)][name]['Servants'][item]['URL'] + '\n'
                embed.add_field(name='Servants', value=string, inline=False)

                if gacha[str(jpyear + 1)][name]['CE']:
                    string2 = ''
                    for item in gacha[str(jpyear + 1)][name]['CE']:
                        if gacha[str(jpyear + 1)][name]['CE'][item]['Name'].find('3') == -1:
                            string2 = string2 + "[%s]" % gacha[str(jpyear + 1)][name]['CE'][item]['Name'] + '(%s)' % \
                                      gacha[str(jpyear + 1)][name]['CE'][item]['URL'] + '\n'

                    if string2:
                        embed.add_field(name='CEs:', value=string2, inline=False)

                await ctx.send(embed=embed)

        await servant.convbox("Special thanks to http://fate-go.cirnopedia.org/ for the information provided.")


@commands.cooldown(1.0, 30, commands.BucketType.user)
@bot.command(aliases=['rate'])
async def rateup(ctx, *, name):
    try:
        incbond(ctx.author.id, 1)
    except KeyError:
        pass
    servant = Servant(ctx, "Tamamo of Knowledge")
    if name.lower() == 'help':
        await servant.dialogbox(
            'This is the command to search for future banner of a certain banner, if you want to go bankrupt.')
        await servant.convbox('The syntax is simple: "<3rateup <servant name>".')
        await servant.convbox(
            "The most preferable format for the servant name is '<number of stars>★ <servant class> <servant full name>'.")
        await servant.convbox(
            "But of course, this is from you so I won't expect too much about you would be able to remember complicated things.")
        await servant.convbox(
            'So I had make another function that return multiple result if your search inquiry is too dumb.')
        await servant.convbox('Just press the number and I will sent the result.')
        await servant.convbox("But it's still kind of buggy at the moment, so don't rely on it too much though.")
        await servant.knowledgebox("As expected from my maker, ", ikaros, '.')
        await servant.dialogbox("Your coding skills is still as shitty as ever.")

    # name = name.split('_')
    # name = ' '.join(name)
    candidate = search(name)
    if len(candidate) <= 0:
        await servant.dialogbox(
            "No rateup found. Even if there is, you probably won't be able to summon what you want either, so don't waste my time trying again. ")
    elif len(candidate) == 1:
        await serrateup(ctx, candidate[0])
    else:
        string = ''
        for i in range(len(candidate)):
            string = string + '**%d. %s** \n' % (i + 1, candidate[i])
        await servant.dialogbox('Multiple servant found:')
        embed = discord.Embed(title='Results for %s' % name, color=servant.color)
        embed.add_field(name='Type the servant number to continue:', value=string, inline=False)
        embed.set_footer(text='Timeout in 30s.')
        await ctx.send(embed=embed)

        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=pred, timeout=30.0)
        except asyncio.TimeoutError:
            await servant.dialogbox('No request received. Please stop wasting my time.')
            await servant.convbox('Bye.')
        else:
            try:
                x = int(msg.content)
            except ValueError:
                await servant.dialogbox(
                    "The input isn't an integer number in integer number format. Stop wasting my time with your stupidity.")
                await servant.convbox('Bye.')
            else:
                if x > len(candidate) or x <= -1:
                    await servant.dialogbox(
                        "Even a 4 years old kid can count better than you. Go back to kindergarten and ask them to teach you.")
                    await servant.convbox('Bye.')
                elif x == 0:
                    await servant.dialogbox("This may be coded with the starting index as 0, but you are not.")
                    await servant.convbox('Bye.')
                else:
                    await serrateup(ctx, candidate[x - 1])


@commands.cooldown(1.0, 10, commands.BucketType.user)
@bot.command()
async def purge(ctx, limit: int = 10):
    def is_me(m):
        return m.author == bot.user

    await ctx.channel.purge(limit=limit, check=is_me)
    await ctx.message.delete()


@commands.cooldown(1.0, 60, commands.BucketType.user)
@bot.command()
async def mikon(ctx, message=''):
    def is_me(m):
        return m.author == bot.user

    await ctx.message.delete()

    for i in range(20):
        await ctx.send('Mikon!' + message)
        await ctx.channel.purge(limit=1, check=is_me)
        await enhsleep(ctx, 0.5)


@commands.cooldown(1.0, 120, commands.BucketType.user)
@bot.command()
async def intro(ctx, pagenum=None):
    try:
        adopted = getadopt(ctx.author.id)
    except KeyError:
        pass
    bond = getbond(ctx.author.id)
    page = getpage(ctx.author.id)
    tag = '<@' + str(ctx.author.id) + '>'
    maxpage = 5
    init = True
    cont = True

    Tamamo = Servant(ctx, "Tamamo no Mae")
    Cat = Servant(ctx, "Tamamo Cat")
    Shark = Servant(ctx, "Tamamo Summer")
    Vicchi = Servant(ctx, "Tamamo Vicchi")
    Knowledge = Servant(ctx, "Tamamo of Knowledge")

    if not await checkpoint(ctx, adopted, bond, 100):
        return

    if pagenum:
        try:
            pagenum = int(pagenum)
        except ValueError:
            cont = await pagesethelper(bot, ctx, maxpage)
        else:
            if pagenum < 0:
                cont = await pagesethelper(bot, ctx, maxpage)
            elif pagenum == 0 or pagenum > maxpage:
                cont = await pagesethelper(bot, ctx, maxpage)
            else:
                setpage(ctx.author.id, pagenum)
                await Knowledge.dialogbox("Page set.")
                cont = True

    if not cont:
        return
    else:
        page = getpage(ctx.author.id)

    if page == 1:
        await Tamamo.dialogbox("Servant Tamamo no Mae, Class Caster.")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("I'm also know as one of the 3 youkais of Japan, with one of the highest kill record.....")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("But Master, please don't hate me because of that...")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("Y..you won't?")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("Thank you very much, Master!")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("You are one of the few human that has said that to me.")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("...")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("If only I didn't meet him...")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("Then maybe.... maybe I would be able to....")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("Ah, please don't worry about that Master!")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("Please for get what I've just said.")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("Your soul is still very handsome itself!")
        await enhsleep(ctx, 1)
        await Tamamo.convbox(
            "I am sure that you will be able to find someone who will be a better wife for you more than me!")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("I've known to much to be able to live a normal life now.")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("It must be karma for all the bad things I've done, for all the people I've killed....")
        await enhsleep(ctx, 1)
        await Tamamo.convbox("But...Thank you for everything, Master!")
        await enhsleep(ctx, 1)

        embed = discord.Embed(title="Tamamo no Mae", color=Tamamo.color)
        embed.set_thumbnail(url=Tamamo.url)
        embed.add_field(name="Aliases:", value="Tamamo, Caster, Original Tamamo", inline=False)
        embed.add_field(name="Motto:", value="Your reliable Caster, specified in martial arts, magic and curses.",
                        inline=False)
        embed.set_image(url='https://i.imgur.com/mZBAa1E.jpg')
        await ctx.send(embed=embed)

        setpage(ctx.author.id, 2)
        init = False
        await enhsleep(ctx, 1)
        incbond(ctx.author.id, 5)

    if not init:
        if not await splitpage(bot, ctx, page, maxpage):
            return
        else:
            page = getpage(ctx.author.id)

    if page == 2:
        await Cat.dialogbox("Woof! Servant Tamamo Cat, Class Berseker. But you can just call me Cat!", 'ʷᵃᵍ ʷᵃᵍ')
        await enhsleep(ctx, 1)
        await Cat.convbox("I'm one of the Tamamo Nine, the Alter Egos of the original Tamamo no Mae.", 'ʷᵃᵍ ʷᵃᵍ')
        await enhsleep(ctx, 1)
        await Cat.convbox(
            "Since nine-tailed Tamamo splited into nine of us, each of us Alter Ego received aspects of the original.",
            'ʷᵃᵍ ʷᵃᵍ')
        await enhsleep(ctx, 1)
        await Cat.convbox("For me it's my purity nature and my talent in being a housewife!", 'ʷᵃᵍ ʷᵃᵍ')
        await enhsleep(ctx, 1)
        await Cat.convbox("So you can rely on me, this trusty maid, for meals and clean...Wait!", '*ˢᵗᵒᵖ ʷᵃᵍᵍᶦⁿᵍ')
        await enhsleep(ctx, 1)
        # serious
        await Cat.dialogbox("Is that the Original?")
        # riyo
        Cat.changeEx('Riyo')
        await Cat.dialogbox("Woof! Let's kill her, Master!")
        await enhsleep(ctx, 1)
        # serious
        await Tamamo.dialogbox("Hey what are you doing?")
        await enhsleep(ctx, 1)
        await Cat.dialogbox('Sansan nikkou hiruyasumi shuchinikurin!')
        await enhsleep(ctx, 0.5)
        await Cat.imagebox("Grmeeeeeeeeoooooooooooow!", 'https://i.imgur.com/DuKkcqs.png')
        await enhsleep(ctx, 0.5)
        await Tamamo.dialogbox("Ouch! Stoppu stoppu purizu!")
        await enhsleep(ctx, 1)
        # sleeping
        Cat.changeEx('Normal')
        await Cat.dialogbox("Now that Original...has been dealt with.....", 'ʷᵃᵍ ʷᵃᵍ')
        await enhsleep(ctx, 1)
        await Cat.convbox("Lucky...Original...not.....Master....I....kill....you.....", 'ʷᵃᵍ ʷᵃᵍ')
        await enhsleep(ctx, 1)
        await Cat.convbox("Z.....z..zzz....zzz....zzzz")
        await enhsleep(ctx, 1)

        embed = discord.Embed(title="Tamamo Cat", color=Cat.color)
        embed.set_thumbnail(url=Cat.url)
        embed.add_field(name="Aliases:", value="Woof woof, Beast IX, Catto", inline=False)
        embed.add_field(name="Motto:", value="Become Master's Pet, Maid and Homemaker.", inline=False)
        embed.set_image(url='')
        await ctx.send(embed=embed)

        setpage(ctx.author.id, 3)
        init = False
        await enhsleep(ctx, 1)
        incbond(ctx.author.id, 5)

    if not init:
        if not await splitpage(bot, ctx, page, maxpage):
            return
        else:
            page = getpage(ctx.author.id)

    if page == 3:
        await ctx.send('p3')


@bot.command()
# @commands.cooldown(1.0, 60, commands.BucketType.user)
async def adopt(ctx):
    status = getadopt(ctx.author.id)
    sanction = getsanction(ctx.author.id)

    Tamamo = Servant(ctx, "Tamamo no Mae")
    Cat = Servant(ctx, "Tamamo Cat")
    Shark = Servant(ctx, "Tamamo Summer")
    Vicchi = Servant(ctx, "Tamamo Vicchi")
    Knowledge = Servant(ctx, "Tamamo of Knowledge")

    if status:
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("You have already adopted us.")
        return

    if 10 >= sanction >= 8:
        await Knowledge.dialogbox("Get lost.")
        decsanction(ctx.author.id)

    elif 7 >= sanction >= 5:
        await Knowledge.dialogbox("You still have the nerve to hang around us? After all of that?")
        decsanction(ctx.author.id)

    elif 4 >= sanction >= 2:
        await Knowledge.dialogbox(
            "We are dissapointed in you. We've tried to be serious, but you didn't take us seriously.")
        decsanction(ctx.author.id)

    elif sanction == 1:
        decsanction(ctx.author.id)
        await Knowledge.dialogbox(
            "Very well. The Tamamo Council have passed an agreement to give you permission to adopt us again.")
        await enhsleep(ctx, 1)
        await Knowledge.convbox("Please be sincere this time, and don't make us revoke our change.")
        await enhsleep(ctx, 1)
        await Knowledge.knowledgebox("Welcome back, Master ", '<@%s>' % str(ctx.author.id), '.')
        setadopt(ctx.author.id)
        discovered = getuserdisc(ctx.author.id)

        if discovered:
            await Tamamo.dialogbox("Welcome back, Goshujin-sama!")
        else:
            await Tamamo.dialogbox("Welcome back, Master!")

        await enhsleep(ctx, 1)
        await Cat.dialogbox("Woof! Did you know how hurt it is to Cat's fragile heart?")
        await enhsleep(ctx, 1)
        await Cat.convbox("What you did is unforgivable, unless someone compensate me with pets...", 'ˢᵗᵃʳᵉ')

        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', check=pred, timeout=20.0)
        except asyncio.TimeoutError:
            await enhsleep(ctx, 1)
            await Cat.dialogbox("Cat is sad now.", 'ˢᵒᵇ ˢᵒᵇ')

        else:
            if msg.content.lower().find('pet') != -1 or msg.content.lower().find('pat') != -1:
                await enhsleep(ctx, 1)
                await Cat.dialogbox('Hmmm, passable, but one more would do the job.', 'ʷᵃᵍ ʷᵃᵍ')

                try:
                    msg = await bot.wait_for('message', check=pred, timeout=20.0)

                except asyncio.TimeoutError:
                    await enhsleep(ctx, 1)
                    await ctx.send("Cat forgive you a little bit.", 'ˢᵗᵃʳᵉ')

                else:
                    if msg.content.lower().find('pet') != -1 or msg.content.lower().find('pat') != -1:
                        await enhsleep(ctx, 1)
                        await Cat.dialogbox('Thank you Master! I forgive you! Welcome back, Woof!', 'ʷᵃᵍ ʷᵃᵍ ʷᵃᵍ')

                    else:
                        await enhsleep(ctx, 1)
                        await ctx.send("Cat forgive you a little bit.", 'ˢᵗᵃʳᵉ')
            else:
                await enhsleep(ctx, 1)
                await Cat.dialogbox("Cat is sad now.", 'ˢᵒᵇ ˢᵒᵇ')

        await enhsleep(ctx, 1)
        await Shark.dialogbox("What you did was not a élégant thing to do for a lady you know?")
        await enhsleep(ctx, 1)
        await Shark.convbox("But I'm glad you are all sincere now, Master!")
        await enhsleep(ctx, 1)
        await Shark.convbox("And I hope you know what awaits you if you do that again.", 'ʷᶦⁿᵏ ʷᶦⁿᵏ')
        await enhsleep(ctx, 1)
        await Shark.convbox(
            "The only different this time is instead of beach sandals, it will be APHE titanium high heels, Mikon!")

        await enhsleep(ctx, 1)
        await Vicchi.dialogbox("Ara, so you are back to being our Master?")
        await enhsleep(ctx, 1)
        await Vicchi.convbox("But we both know that what you've done can't be swept under the rug right?")
        await enhsleep(ctx, 1)
        await Vicchi.convbox("So...stay still. Bad boy need to be punished.")
        await enhsleep(ctx, 1)
        await Vicchi.convbox("If will only hurt if you try to move... or will it?")
        # insert vicchi malicious smirk




    elif sanction == 0:
        await enhsleep(ctx, 1)
        await Tamamo.dialogbox("Caster Tamamo no Mae, but you can just call me Tamamo, since it's much cuter!")
        '''Thank you Master!. I will do my best to serve you from now on!.")'''
        await enhsleep(ctx, 1)
        # TODO: fill the rest
        await Tamamo.convbox('')
        await enhsleep(ctx, 1)
        # await Cat.


@bot.command(aliases=['add'])
async def addemoji(ctx, emoji='', url=''):
    username = ctx.guild.get_member(int(ctx.author.id)).display_name
    Knowledge = Servant(ctx, "Tamamo of Knowledge")
    if not checkemoji(emoji) and not checkurl(url):
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("Congratulation %s, you have reached a new level of stupidity. Hooray." % username)
        await enhsleep(ctx, 1)
        await Knowledge.convbox(
            "Not only did you get the emoji syntax wrong, the 'thing' you inputted in url is not even a gif url.")
        return 0;

    elif not checkemoji(emoji):
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("...This is not even a emoji syntax.")
        return 0

    elif not checkurl(url):
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("I'm not going to waste my memory remembering your random shits.")
        await enhsleep(ctx, 1)
        await Knowledge.convbox("Gif URLs only, is it that hard to understand?")
        return 0

    if emoji.lower().find("padoru") != -1 or emoji.lower().find("pad0ru") != -1:
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("No padoru.")
        return 0

    # check if link is valid
    valid = True
    with open(dir_path + '/Pictures/gif_test.gif', 'wb') as g:
        try:
            g.write(requests.get(url).content)
        except:
            valid = False

    if valid and os.stat(dir_path + '/Pictures/gif_test.gif').st_size == 0:
        valid = False

    if not valid:
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("Invalid URL.")
        await enhsleep(ctx, 0.5)
        await Knowledge.convbox("Incompetent.")
        return 0

    res = 99
    try:
        res = addgif(ctx.guild.id, emoji, url)
    except KeyError:
        pass
    if res == 0:
        await ctx.send("%s added.\n" % emoji)
    else:
        await ctx.send("There is already another gif under this %s.\n" % emoji)


@bot.command(aliases=['del'])
async def deleteemoji(ctx, emoji=''):
    Knowledge = Servant(ctx, "Tamamo of Knowledge")
    if not checkemoji(emoji):
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("...This is not even a emoji syntax.")
        return 0

    res = 99
    try:
        res = deletegif(ctx.guild.id, emoji)
    except KeyError:
        pass
    if res == 0:
        await ctx.send("%s deleted.\n" % emoji)
    else:
        await enhsleep(ctx, 1)
        await Knowledge.dialogbox("There is no emoji under %s to be deleted." % emoji)
        await enhsleep(ctx, 1)
        await Knowledge.convbox("Perhaps that it's you that should be deleted?")


@bot.command(aliases=['stat'])
@commands.cooldown(1.0, 60, commands.BucketType.user)
async def stats(ctx):
    data = json.loads(r.get('user'))
    if not str(ctx.author.id) in data:
        inituser(ctx.author.id, data)
        jsonsave(data)

    user = data[str(ctx.author.id)]
    username = ctx.guild.get_member(ctx.author.id).display_name
    ava_url = ctx.guild.get_member(ctx.author.id).avatar_url
    Knowledge = Servant(ctx, "Tamamo of Knowledge")

    embed = discord.Embed(title="Stats for %s" % username, color=Knowledge.color)
    embed.set_author(name=Knowledge.name, icon_url=Knowledge.url)
    embed.set_thumbnail(url=ava_url)
    embed.add_field(name="Current persona:", value=user['mode'], inline=False)
    embed.add_field(name="Bonds level:", value=str(user['bond'] // 10), inline=False)
    embed.add_field(name="NSFW counts:", value=str(user['nsfw']), inline=False)
    embed.add_field(name="Emoji spammed:", value=str(user['emoji']), inline=False)
    await ctx.send(embed=embed)
    # await


@bot.command()
async def say(ctx, channel_id, *, mess):
    if str(ctx.author.id) != ikarosID:
        await ctx.send("Sorry, you are not authorized for this command.")
        return

    print(ctx.channel)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Sorry, you must use DM for this command.")
        return

    channel = bot.get_channel(int(channel_id))
    if not channel:
        await ctx.send("Invalid channel.")
        return

    await channel.send(mess)


@bot.command(aliases=['pley', 'Play', 'PLAY', 'plya'])
async def play(ctx, url: str, channel_id=None):
    # check if user is in voice channel
    Knowledge = Servant(ctx, "Tamamo of Knowledge")
    user_on_voice = ctx.author.voice

    # help section
    if url.lower() == 'help':
        await enhsleep(ctx, 0.5)
        await Knowledge.dialogbox("Your typical music bot. Has a lot of bugs (maybe), slapped together with alot of "
                                  "hacks and temporary fixes.")
        await enhsleep(ctx, 0.5)
        await Knowledge.convbox("May or may not corrupt your saves, deafen your ears or eat your first-born child. "
                                "I'm totally not responsible for any of this.")
        await enhsleep(ctx, 0.5)
        await Knowledge.convbox("Commands included: play, loop, stop, skip, pause, resume, queue. You know, typical "
                                "commands, self explanatory.")
        await enhsleep(ctx, 0.5)
        await Knowledge.convbox("Also 'play' can work with direct music links, requires end with full filename though.")
        await enhsleep(ctx, 0.5)
        await Knowledge.convbox("E.g.: 'https://static.wikia.nocookie.net/kancolle/images/1/16/Kongou-Attack.ogg', "
                                "'https://cdn.discordapp.com/attachments/684226101848965171/684226716402843755/AQUA_NEEE.mp3'.")
        return

    if not user_on_voice:
        if int(ctx.author.id) != int(ikarosID):
            await enhsleep(ctx, 0.5)
            await Knowledge.dialogbox("You can not use this command while not being in a voice channel.")
            await enhsleep(ctx, 0.5)
            await Knowledge.knowledgebox("Unless you are ", ikaros, " that is.")
            return
        else:
            if not channel_id:
                return
            voice_channel = discord.utils.get(ctx.guild.voice_channels, id=int(channel_id))
    else:
        voice_channel = ctx.author.voice.channel

    # check if link is a youtube link
    is_youtube = False
    if ''.join(re.findall(r'(\w+)', url.lower())).find('youtube') != -1:
        is_youtube = True
    elif ''.join(re.findall(r'(\w+)', url.lower())).find('soundcloud') != -1:
        await Knowledge.dialogbox('Soundclound is not supported yet? Or never will be, depends.')
        return

    if is_youtube:
        youtube_dl_query = []
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'outtmpl': dir_path + f'/Audio/{voice_channel.id}/1 - %(title)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)

            # unplayable tags
            is_live = False
            duration600 = False

            # is youtube playlist
            if 'entries' in result:
                for i in result['entries']:
                    if i['is_live']:
                        is_live = True
                        break
                    elif int(i['duration']) >600:
                        duration600 = True
                        break
                    youtube_dl_query.append(i["webpage_url"])
            else:
                if result['is_live']:
                    is_live = True
                elif int(result['duration']) > 600:
                    duration600 = True

            if is_live:
                await enhsleep(ctx, 0.5)
                await Knowledge.dialogbox("You know, I wish we could play live stuff on discord bot too.")
                await enhsleep(ctx, 0.5)
                await Knowledge.convbox("But alas.")
                return
            elif duration600:
                await enhsleep(ctx, 0.5)
                await Knowledge.dialogbox("Due to the F2P nature of this bot, I'm not permitted to play video with a "
                                          "duration over 600 seconds.")
                return




    # check if the bot is active on another voice channel
    # disconnect if the prev voice channel is different from the intended or the bot has not joined a channel
    # and move to the new channel.
    previous_voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    is_playing_in_cur_channel = False
    if previous_voice_client:
        if previous_voice_client.channel.id != voice_channel.id:
            await enhsleep(ctx, 0.5)
            await Knowledge.dialogbox(f"Adios, people of {previous_voice_client.channel.name}.")
            await previous_voice_client.disconnect()
            time.sleep(1)
            await voice_channel.connect()
            os.rmdir(dir_path + f'/Audio/{previous_voice_client.channel.id}')
        else:
            is_playing_in_cur_channel = True
    else:
        await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # set counter for playlist and queueing purpose
    start_pos = 0
    # if there is already music playing in current channel, get its counter
    if is_playing_in_cur_channel:
        list_of_files = glob.glob(dir_path + f'/Audio/{voice_channel.id}/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        start_pos = int(latest_file.split('\\')[-1].split('---')[0]) + 1
        await ctx.channel.send("`Song added to queue`")
    else:
        try:
            os.mkdir(dir_path + f'/Audio/{voice_channel.id}/')
        except FileExistsError:
            pass

    if is_youtube:
        # download each song separately so I can apply custom name
        for i in range(len(youtube_dl_query)):
            ydl_opts_sep = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'outtmpl': dir_path + f'/Audio/{voice_channel.id}/{start_pos + i}---%(title)s.%(ext)s'
            }
            with youtube_dl.YoutubeDL(ydl_opts_sep) as ydl:
                ydl.download([youtube_dl_query[i]])

    else:
        track_file_name = url.split('/')[-1]
        with open(dir_path + f'/Audio/{voice_channel.id}/{start_pos}---{track_file_name}', 'wb+') as track:
            track.write(requests.get(url).content)
            track_path = dir_path + f'/Audio/{voice_channel.id}/{start_pos}---{track_file_name}'
            #os.popen(f'ffmpeg -i "{track_path}" -vn -ar 44100 -ac 2 -b:a 192k "{track_path[:-4]}.mp3" -hide_banner -loglevel error')
            #os.popen()


    # play music if not already playing in current channel, otherwise just add more song to queue
    if not is_playing_in_cur_channel:
        play_obj = audioPlay(bot, ctx, voice, voice_channel.id)
        guild_music_objs[str(voice_channel.id)] = play_obj
        try:
            await play_obj.play(True)
        except (discord.errors.ClientException, FileNotFoundError) as e:
            if e.__str__() == "Not connected to voice." and isinstance(e, discord.errors.ClientException):
                pass
            else:
                raise e

# background task deleting unused voice playing object
@tasks.loop(seconds=0.5)
async def check_audio():
    for channel_id in list(guild_music_objs):
        if guild_music_objs[channel_id].stopped:
            del guild_music_objs[channel_id]


@bot.command()
async def stop(ctx):
    if not ctx.author.voice:
        await ctx.channel.send("`You are not even in a voice channel.`")
    try:
        await guild_music_objs[str(ctx.author.voice.channel.id)].stop()
    except KeyError:
        await ctx.channel.send("`There is no music currently playing in this voice channel.`")

@bot.command()
async def loop(ctx):
    if not ctx.author.voice:
        await ctx.channel.send("`You are not even in a voice channel.`")
    try:
        await guild_music_objs[str(ctx.author.voice.channel.id)].setloop()
    except KeyError:
        await ctx.channel.send("`There is no music currently playing in this voice channel.`")

@bot.command()
async def skip(ctx):
    if not ctx.author.voice:
        await ctx.channel.send("`You are not even in a voice channel.`")
    try:
        guild_music_objs[str(ctx.author.voice.channel.id)].skipping = True
    except KeyError:
        await ctx.channel.send("`There is no music currently playing in this voice channel.`")

@bot.command()
async def pause(ctx):
    if not ctx.author.voice:
        await ctx.channel.send("`You are not even in a voice channel.`")
    try:
        if guild_music_objs[str(ctx.author.voice.channel.id)].voice_client.is_playing():
            guild_music_objs[str(ctx.author.voice.channel.id)].paused = True
            guild_music_objs[str(ctx.author.voice.channel.id)].voice_client.pause()
        else:
            await ctx.channel.send("`The audio is already paused.`")
    except KeyError:
        await ctx.channel.send("`There is no music currently playing in this voice channel.`")

@bot.command()
async def resume(ctx):
    if not ctx.author.voice:
        await ctx.channel.send("`You are not even in a voice channel.`")
    try:
        if guild_music_objs[str(ctx.author.voice.channel.id)].voice_client.is_paused():
            guild_music_objs[str(ctx.author.voice.channel.id)].voice_client.resume()
            guild_music_objs[str(ctx.author.voice.channel.id)].paused = False
        else:
            await ctx.channel.send("`The audio is not paused.`")
    except KeyError:
        await ctx.channel.send("`There is no music currently playing in this voice channel.`")

@bot.command()
async def queue(ctx):
    if not ctx.author.voice:
        await ctx.channel.send("`You are not even in a voice channel.`")
    try:
        queue_str = '`'
        song_dir_list = os.listdir(dir_path + f'/Audio/{ctx.author.voice.channel.id}/')
        for i in range(len(song_dir_list)):
            queue_str += f'{i+1}. {song_dir_list[i][4:-4]} \n'
        queue_str += '`'
        await ctx.channel.send("**Queue:**")
        await ctx.channel.send(queue_str)
    except (FileNotFoundError, AttributeError) as e:
        if isinstance(e, AttributeError):
            if e.__str__() == "'NoneType' object has no attribute 'channel'":
                pass
            else:
                raise e
        await ctx.channel.send("`There is no music currently playing in this voice channel.`")

@bot.command()
async def t(ctx):
    os.mkdir('aaa')


@bot.command()
async def t2(ctx):
    inituser(ctx.author.id)
    # await bot.get_channel(671742964749303827).send(ctx.guild.voice_client)
    vc = ctx.guild.voice_client
    if vc:
        await vc.disconnect(force=True)


bot.run(token)
