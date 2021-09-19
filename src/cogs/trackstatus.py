import discord
from discord.ext import commands
import time

class TrackStatus(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        global ctr
        '''if before.id == int(ikarosID):
            if after.activities and after.activities[0].name == "Rainbow Six Siege":
                if ctr == 2:
                    await before.guild.get_channel(int(channelID)).send("Stop playing R6S and go learn Python.")
                    ctr = 0
                else:
                    ctr+=1'''
        
        '''if before.id == int(remineID) and after.activities:
            print(after.activities[0])'''
            
        '''if after.guild.get_member(int(sukvatID)).activities[0].name == "Rainbow Six Siege":
            print('y')
    '''
def setup(bot):
    bot.add_cog(TrackStatus(bot))
    from tamamo import remineID, sukvatID, ikarosID, channelID, testID
    global remineID, sukvatID, ikarosID, channelID, testID
    global ctr
    ctr = 0
    