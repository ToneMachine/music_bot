import subprocess
from discord.ext import commands
import discord
from setting import token
from discord import FFmpegPCMAudio
import os
import re
import time

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
playing = False
queue = []
audio_path = "C:/Users/anton/OneDrive/Desktop/Codes/song.mp3"


# gets length of audio
def audio_duration(file_path):

    result = subprocess.run(['ffmpeg', '-i', file_path], capture_output=True, text=True)
    output = result.stderr
    duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", output)
    if duration_match:
        hours, minutes, seconds = map(float, duration_match.groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        return None

# status of bot
@bot.event
async def on_ready():
    print('bot is live')

# play command
@bot.command(name='play')
async def play(ctx, url):
    global voice

    # join the server
    user = ctx.author.voice
    if user is not None:

        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            subprocess.run(['spotdl', url])

        except:
            # download song from spotify
            subprocess.run(['spotdl', url])

        # renames mp3
        for file in os.listdir():
            if file.endswith(".mp3"):
                try:
                    os.rename(file, "song.mp3")

                except:
                    os.remove("C:/Users/anton/OneDrive/Desktop/Codes/song.mp3")
                    os.rename(file, "song.mp3")

        # plays song       
        song = FFmpegPCMAudio(executable="C:/ffmpeg-2024-02-22-git-76b2bb96b4-full_build/bin/ffmpeg.exe", source=r"C:\Users\anton\OneDrive\Desktop\Codes\song.mp3")
        while True:
            try:
                voice.play(song)
                break

            except:
                continue

    else:
        await ctx.send("(Be in a voice channel please)")

bot.run(token)