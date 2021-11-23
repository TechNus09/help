import discord
import os, binascii
import pytube
from discord.ext import commands
from pytube import YouTube

bot = commands.Bot(command_prefix = '$')
filedirectory = os.getcwd()
bot.remove_command('help')



@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.command()
async def help(ctx):
    await ctx.send("Use $ before a youtube link to download it as an mp3. Just make sure the embed isn't hidden!")

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

""" to ping the author:
await message.channel.send("{}".format(message.author.mention)

to ping another user:
await message.channel.send("<@![user id]>")

to add an emoji:
await message.channel.send("<:[emoji name]:[emoji id]>")
"""

"""
async def on_message(message):


    link = message.content
    video = YouTube(link)
    stream = video.streams.get_highest_resolution()
    stream.download()
    with open(stream.download, 'rb') as f:
        picture = discord.File(f)
        await message.channel.send(file=discord.File(stream.download))
"""
