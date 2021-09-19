import discord
from discord.ext import commands
import time
import re
import json
import requests
import asyncio
import os
import shutil
dir_path = os.path.dirname(os.path.realpath(__file__))

class audioPlay():
    def __init__(self, bot, ctx, voice_client, channel_id):
        self.bot = bot
        self.ctx = ctx
        self.voice_client = voice_client
        self.channel_id = channel_id
        self.order = None
        self.loop = False
        self.stopped = False
        self.skipping = False
        self.paused = False

    async def play(self, start=False):
        """

        :param start: is just a mess at this point
        :return:
        """

        first_time_name_display = False
        # in case nothing was downloaded
        if not os.listdir(dir_path + f'/Audio/{self.channel_id}/'):
            await self.stop()

        while os.listdir(dir_path + f'/Audio/{self.channel_id}/'):
            # queue empty if loop is not set
            if len(os.listdir(dir_path + f'/Audio/{self.channel_id}/')) <= 1 and not self.loop and not start:
                break
            # handle loops or start of a playlist
            elif self.loop or start:
                now_playing = dir_path + f'/Audio/{self.channel_id}/' + \
                              os.listdir(dir_path + f'/Audio/{self.channel_id}/')[0]
                if not first_time_name_display:
                    await self.ctx.channel.send(f"`Now playing:` **{now_playing.split('/')[-1][4:-4]}**")
                    first_time_name_display = False
            # handle members of a playlist normally
            else:
                now_playing = dir_path + f'/Audio/{self.channel_id}/' + \
                              os.listdir(dir_path + f'/Audio/{self.channel_id}/')[1]
                await self.ctx.channel.send(f"`Now playing:` **{now_playing.split('/')[-1][4:-4]}**")

            # start playing
            self.voice_client.play(discord.FFmpegPCMAudio(now_playing))


            # wait for song to finish playing before next loop
            # also skip is handled here
            continue_flag = False # if skip then use this
            # handle pause
            while self.voice_client.is_playing() or self.paused:
                await asyncio.sleep(0.5)
                if self.skipping:
                    self.skipping = False
                    start = True
                    continue_flag = True
                    self.voice_client.stop()
                    await asyncio.sleep(1)
                    os.remove(dir_path + f'/Audio/{self.channel_id}/' +
                              os.listdir(dir_path + f'/Audio/{self.channel_id}/')[0])
                    break

            # usage of continue flag mentioned above
            if continue_flag:
                continue


            # handle song files
            if not start:
                # wait for ffmpeg to free its resources otherwise will lead to permission error while deleting file
                await asyncio.sleep(2)
                os.remove(dir_path + f'/Audio/{self.channel_id}/' +
                          os.listdir(dir_path + f'/Audio/{self.channel_id}/')[0])
                # in case of looping
                if self.loop:
                    start = True
            else:
                if not self.loop:
                    start = False

            # last stop handle:
            if self.stopped:
                break

        # no more song in queue
        # make sure not to call play() multiple time for the same object
        await self.stop()



    async def setloop(self):
        self.loop = not self.loop
        if self.loop:
            await self.ctx.channel.send("`Loop enabled.`")
        else:
            await self.ctx.channel.send("`Loop disabled.`")



    async def stop(self):
        self.stopped = True
        await self.ctx.channel.send("`Queue empty. Disconnecting...`")
        await self.voice_client.disconnect()
        while True:
            try:
                shutil.rmtree(dir_path + f'/Audio/{self.channel_id}/')
            except (PermissionError, FileNotFoundError):
                continue
            else:
                break
