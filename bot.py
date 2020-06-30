import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import io
import aiohttp
import time

bot = commands.Bot(command_prefix='$', case_insensitive=True)
TOKEN = 'NjQyNTM4NzAxNzgzODI2NDQ5.XuJyAQ.gSpE6gr7EyvejZuQpZH57GNjiws'

@bot.event
async def on_ready():
    print ("Bot is ready")


@bot.command(pass_context=True)
async def gib(ctx, arg):
    """Usuage: $gib *ticker symbol*
    \nFor US stocks, Please add :US after the ticker. For example for TSLA (Tesla Inc), it would be TSLA:US
    \nNote: All prices are in CAD$"""

    ticker = arg.upper()
    price = calculate(ticker)
    imgUrl = getImg(ticker, '5d')

    await ctx.send(price)
    async with aiohttp.ClientSession() as session:
        async with session.get(imgUrl) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'output.png'))

@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}")


@bot.command(pass_context=True)
async def chart(ctx, ticker, duration):
    """Usuage: $chart *ticker symbol* *duration*
    duration can be either of these; 1d, 2d, 3d, 4d, 5d, 1m, 3m, 6m, 1y
    """
    imgUrl = getImg(ticker, duration)
    async with aiohttp.ClientSession() as session:
        async with session.get(imgUrl) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'output.png'))

@bot.command(pass_context=True)
async def timer(ctx, ticker, freq):
    while (True and int(freq)>=10):
        price = calculate(ticker)
        await ctx.send(price)
        time.sleep(int(freq))

        

def calculate(ticker):
        url = "https://web.tmxmoney.com/quote.php?qm_symbol={}".format(ticker)
        r = requests.get(url)

        only_class = SoupStrainer(class_="dq-card")
        soup = BeautifulSoup(r.text, "lxml", parse_only=only_class)
        soup2 = BeautifulSoup(r.text, "lxml")

        name = soup2.find(class_="quote-company-name").h4.text
        price = soup2.find(class_="price").span.text

        if (price == ""):
            return "Error. Refer type '$help gib' to view info on how to use"
        else:
            Open = soup.contents[1].find("strong").text
            High = soup.contents[2].find("strong").text
            Prev_close = soup.contents[6].find("strong").text
            Low = soup.contents[7].find("strong").text
            Market_cap = soup.contents[9].find("strong").text
            Dividend = soup.contents[11].find("strong").text
            Div_freq = soup.contents[12].find("strong").text
            Ex_div_date = soup.contents[16].find("strong").text
            Exchange = soup.contents[18].find("strong").text

            statement = f"The current price of {ticker} ({name}) is: {price}."

            if Dividend == "N/A":
                pass;
            else:
                statement = statement + f"\nTheir Dividend payout is {Dividend} and they payout {Div_freq}"
            return statement

def getImg(ticker, duration):
    #duration = '5d'
    label = 'true'
    #220x120. 11/6 ratio
    imgW = 770
    imgH = 420

    imgURL = f'https://app.quotemedia.com/quotetools/getChart?webmasterId=101020&snap=true&symbol={ticker}&chscale={duration.lower()}&chtype=line&chwid={imgW}&chhig={imgH}&chmrg=0&chfrmon=off&chton={label}&chlgdon=off&ch52on=on&chgrd=D8DCE5&chbdr=D8DCE5&chln=313942&chaaon=true&locale=en'
    return imgURL

bot.run(TOKEN)
