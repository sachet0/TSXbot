import discord
from discord.ext import commands
import requests
import io
import aiohttp
import time
import random

bot = commands.Bot(command_prefix='$', case_insensitive=True)
TOKEN = 'ENTER YOUR BOT TOKEN HERE'


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}")


@bot.command(pass_context=True)
async def diamondhands(ctx):
    await ctx.send("https://media.discordapp.net/attachments/720701471741706285/806377976022433822/BrainStopMeme.png?width=730&height=566")


@bot.command(pass_context=True)
async def over(ctx):
    """Its over."""
    gifList = ["https://tenor.com/view/wagie-wojak-meme-mcdonalds-wage-cuckin-it-gif-18834548",
               "https://tenor.com/view/wagie-wojak-gif-18834646",
               "https://tenor.com/view/wagie-wojak-gif-18834642",
               "https://tenor.com/view/wagie-wojak-gif-18834650",
               "https://tenor.com/view/wojak-index-pink-levels-gif-16567170"]
    num = random.randint(0, len(gifList)-1)
    await ctx.send(gifList[num])


@bot.command(pass_context=True)
async def bog(ctx):
    """Bogdanoff"""
    await ctx.send("https://tenor.com/view/bogdanov-bogdanof-bitcoin-on-the-phone-gif-12411899")


@bot.command(pass_context=True)
async def chart(ctx, ticker, duration=""):
    """Usage: $chart *ticker symbol* *duration*
    duration can be either of these; 1d, 2d, 3d, 4d, 5d, 1m, 3m, 6m, 1y
    For US stocks, Please add :US after the symbol. For example for TSLA (Tesla Inc), it would be TSLA:US
    Note: All prices are in CAD$"""
    if duration == "":
        return await ctx.send('Error. Please try again, you missed the duration.')

    crypto = False

    if ticker.lower() in ['eos', 'eth', 'trx', 'xmr', 'ada', 'miota', 'btc', 'bch', 'bnb', 'bsv', 'xlm', 'xrp', 'doge', 'link', 'ltc', 'usdt']:
        imgUrl = getCrypt(ticker, duration)
        crypto = True
    else:
        imgUrl = getImg(ticker, duration)
        crypto = False

    if crypto: await ctx.send(imgUrl)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(imgUrl) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())                
                await ctx.send(file=discord.File(data, 'output.png'))


def getImg(ticker, duration):
    #duration = '5d'
    label = 'true'
    # 220x120. 11/6 ratio
    imgW = 770
    imgH = 420

    imgURL = f'https://app.quotemedia.com/quotetools/getChart?webmasterId=101020&snap=true&symbol={ticker}&chscale={duration.lower()}&chtype=line&chwid={imgW}&chhig={imgH}&chmrg=0&chfrmon=off&chton={label}&chlgdon=off&ch52on=on&chgrd=D8DCE5&chbdr=D8DCE5&chln=313942&chaaon=true&locale=en'
    return imgURL


def getCrypt(symbol, duration):
    day = 0
    month = 0
    year = 0
    if duration[-1] == 'm':
        if month <= 12:
            month == duration[:-1]
        else: month = 1
        day, year = 0, 0
    elif duration[-1] == 'd':
        day = duration[:-1]
        month, year = 0, 0
    elif duration[-1] == 'y':
        year = duration[:-1]
        day, month = 0, 0
    
    imgURL = f'https://stockcharts.com/c-sc/sc?s=%24{symbol.upper()}USD&p=D&yr={year}&mn={month}&dy={day}&i=t5756256453c&r=1613273314377'

    return imgURL


bot.run(TOKEN)
