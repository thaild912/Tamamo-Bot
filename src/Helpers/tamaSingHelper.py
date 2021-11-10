import asyncio
import glob
import os
import time

import discord
import requests
import yt_dlp
from requests import get
from requests.exceptions import MissingSchema, InvalidSchema
import re

from tamaSing import audioPlay


async def download_and_play(ctx, path, servant, privileged, args, guild_music_objs):
    await ctx.channel.send('Downloading song(s)...')

    # check on command validity
    # combine args
    user_on_voice = ctx.author.voice
    if not user_on_voice:
        if not (privileged
                and args[-1].isnumeric()
                and discord.utils.get(ctx.guild.voice_channels, id=int(args[-1]))):
            await servant.dialogbox("You can not use this command while not being in a voice channel.")
            return
        else:
            voice_channel = discord.utils.get(ctx.guild.voice_channels, id=int(args[-1]))
            query = ' '.join(args[-1])
    else:
        voice_channel = ctx.author.voice.channel
        query = ' '.join(args)

    # change channel and get song pos
    playing_in_cur_channel = await is_playing_in_cur_channel(ctx, path, servant, voice_channel)
    if playing_in_cur_channel:
        pos = get_song_pos(ctx, path, voice_channel)
    else:
        pos = 0
        make_new_song_dir(path, voice_channel)

    # download songs
    is_youtube, url = await get_link(servant, query)
    # invalid urls
    if not url:
        return
    elif is_youtube:
        urls = await get_separate_yt_url(servant, privileged, url)
        if not urls:
            return

    if playing_in_cur_channel:
        if is_youtube:
            await download_yt_songs(path, voice_channel, urls[:1], pos)
            await voice_channel.connect()
            asyncio.ensure_future(download_yt_songs(path, voice_channel, urls[1:], pos + 1))
            await play(ctx, voice_channel, guild_music_objs)
        else:
            await download_direct_song_url(path, voice_channel, url, pos)
            await voice_channel.connect()
            await play(ctx, voice_channel, guild_music_objs)

    else:
        if is_youtube:
            await download_yt_songs(path, voice_channel, urls, pos)
        else:
            await download_direct_song_url(path, voice_channel, url, pos)

        await ctx.channel.send("Song(s) added to queue.")



async def get_link(servant, query):
    is_youtube = True
    try:
        get(query)
    except (MissingSchema, InvalidSchema) as e:
        with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}) as ydl:
            url = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]["webpage_url"]
    else:
        url = query
        if ''.join(re.findall(r'(\w+)', query.lower())).find('youtube') == -1:
            is_youtube = False
        elif ''.join(re.findall(r'(\w+)', query.lower())).find('soundcloud') != -1:
            await servant.dialogbox('Soundclound is not supported yet? Or never will be, depends.')
            return False, None

    return is_youtube, url


async def get_separate_yt_url(servant, privileged, url):
    youtube_dl_query = []
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)

        # unplayable tags
        is_live = False
        duration600 = False
        # is youtube playlist
        if 'entries' in result:
            for i in result['entries']:
                if 'is_live' in i.keys():
                    if i['is_live']:
                        is_live = True
                        break
                    elif int(i['duration']) > 600 and not privileged:
                        duration600 = True
                        break
                    youtube_dl_query.append(i["webpage_url"])

        else:
            if result['is_live']:
                is_live = True
            elif int(result['duration']) > 600 and not privileged:
                duration600 = True
            else:
                youtube_dl_query.append(url)

        if is_live:
            await servant.dialogbox("You know, I wish we could play live stuff on discord bot too.")
            await servant.convbox("But alas.")
            return None
        elif duration600:
            await servant.dialogbox("Due to the F2P nature of this bot, I'm not permitted to play video with a "
                                    "duration over 600 seconds.")
            return None

        return youtube_dl_query


async def is_playing_in_cur_channel(ctx, path, servant, voice_channel):
    # check if the bot is active on another voice channel
    # disconnect if the prev voice channel is different from the intended or the bot has not joined a channel
    # and move to the new channel.
    previous_voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if previous_voice_client:
        if previous_voice_client.channel.id != voice_channel.id:
            await servant.dialogbox(f"Adios, people of {previous_voice_client.channel.name}.")
            await previous_voice_client.disconnect()
            time.sleep(0.5)
            os.rmdir(path + f'/Audio/{previous_voice_client.channel.id}')
            return False
        else:
            return True
    else:
        return False


def get_song_pos(ctx, path, voice_channel):
    # get song's position if there is already a queue going on
    list_of_files = glob.glob(path + f'/Audio/{voice_channel.id}/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return int(re.findall(r'(\d+)---', latest_file)[0]) + 1


def make_new_song_dir(path, voice_channel):
    try:
        os.mkdir(path + f'/Audio/{voice_channel.id}/')
    except FileExistsError:
        pass


async def download_yt_songs(path, voice_channel, urls, start_pos):
    for i in range(len(urls)):
        ydl_opts_sep = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '192',
            }],
            #'quiet': True,
            'outtmpl': path + f'/Audio/{voice_channel.id}/{start_pos + i}---%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts_sep) as ydl:
            ydl.download([urls[i]])

async def download_direct_song_url(path, voice_channel, url, start_pos):
    track_file_name = url.split('/')[-1]
    with open(path + f'/Audio/{voice_channel.id}/{start_pos}---{track_file_name}', 'wb+') as track:
        track.write(requests.get(url).content)


async def play_after_first_download(ctx, voice_channel, downloaded_first_song_flag, guild_music_objs):
    # event loop
    while True:
        if downloaded_first_song_flag[0]:
            await play(ctx, voice_channel, guild_music_objs)
            break
        await asyncio.sleep(0.5)


async def play(ctx, voice_channel, guild_music_objs):
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    play_obj = audioPlay(ctx.bot, ctx, voice, voice_channel.id)
    guild_music_objs[str(voice_channel.id)] = play_obj
    try:
        await play_obj.play(True)
    except (discord.errors.ClientException, FileNotFoundError) as e:
        if e.__str__() == "Not connected to voice." and isinstance(e, discord.errors.ClientException):
            pass
        else:
            raise e
