






#-------------------------------------------------UNUSED--------------------------------------------------------#







from discord.ext import tasks, commands
import redis
import json
import pickle
import os

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.r = redis.from_url(os.environ.get("REDIS_URL"))
        self.bot = bot
        self.update.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=300.0)
    async def update(self):
        print(self.index)
        self.index += 1

    @update.before_loop
    async def before_update(self):
        await self.bot.get_channel(671742964749303827).send('5 min to update')
        await self.bot.wait_until_ready()
