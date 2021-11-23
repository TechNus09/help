import asyncio
import discord
import os, binascii
import pytube
from discord.ext import commands
from pytube import YouTube

bot = commands.Bot(command_prefix = '$')
filedirectory = os.getcwd()
"""
remove the pre-defined help command
"""
bot.remove_command('help')


"""
client = discord.client()
already called bot, no need to call client, change all the client's mentions in the code to 'bot'
"""

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

""""
@bot.event
async def on_message(message):
    #Doesn't reply to itself
    if message.author == bot.user:
        return
    
    #Command help
    if message.content.startswith("$help"):
        await message.channel.send("Use '$youtube [link] [mp3/mp4]' . Just make sure the embed isn't hidden!")
"""

"""can change the previous lines to just : """
@bot.command()
async def help(ctx):
    await ctx.send("Use '$youtube [link] [mp3/mp4]' . Just make sure the embed isn't hidden!")


"""
@bot.event should be changed to @bot.command() so you can interact with the bot
"""
@bot.command()
async def youtube(ctx, link, filetype):
    await ctx.send('Please wait a moment...')

    # it takes the link argument and makes it compatible with pytube
    url = pytube.YouTube(link)
    # declares the fname variable and sets it to equal a random hex
    fname = str(binascii.b2a_hex(os.urandom(30)))

    if filetype == 'mp4':
        # finds the first stream in the list that is progressive (meaning it has both video and audio) and is an mp4 file
        video = url.streams.filter(progressive = True, file_extension = 'mp4').first()
        await ctx.send('Successfully found video. Downloading...')
        
        # and finally it sends the video file thru discord
        video.download(filedirectory, filename=fname + '.mp4')
        await ctx.send(file=discord.File(f'{filedirectory}/{fname}.mp4'))
    elif filetype == 'mp3':
        # finds the first stream that is audio. this is guaranteed to always be a mp3 file.
        video = url.streams.filter(only_audio=True).first()
        await ctx.send('Successfully found audio. Downloading...')
        # and finally it sends the audio file thru discord
        video.download(filedirectory, filename=fname + '.mp3')
        await ctx.send(file=discord.File(f'{filedirectory}/{fname}.mp3'))
    else:
        await ctx.send("Not a supported filetype!!!")

bot.run(os.environ.get("TOKEN"))
