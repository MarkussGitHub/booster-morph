import discord
from discord.ext import commands

import requests, os
from bs4 import BeautifulSoup
from pymongo import MongoClient

login = os.environ["mongo_login"]
client = MongoClient("mongodb+srv://{}@cluster0.1budm.mongodb.net/Morph_Users?retryWrites=true&w=majority".format(login))
db = client.Users

def data_add(discord_id, valname, valid):
    valorant = {
        'discord_id' : discord_id,
        'valname' : valname,
        'valid' : valid
    }

    user = db.valorant.find_one( {'discord_id': discord_id} )

    if user == None:
        db.valorant.insert_one(valorant)
        return 'Added successfully'
    else:
        db.valorant.update_one({'discord_id': discord_id},{ '$set': { "valname": valname } })
        db.valorant.update_one({'discord_id': discord_id},{ '$set': { "valid": valid } })
        return 'Valorant name and id updated successfully'

def get_name(discord_id):
    user = db.valorant.find_one({'discord_id': discord_id})
    if user == None:
        valorant_name = None
        valorant_id = None
    else:
        valorant_name = user['valname']
        valorant_id = user['valid']
    return valorant_name, valorant_id

def get_rank(valname, valid):
    page = requests.get("https://tracker.gg/valorant/profile/riot/{}%23{}/overview".format(valname, valid))
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='app')
    rankspan = results.find_all('span', class_='valorant-highlighted-stat__value')
    if len(rankspan) == 2:
        rank = rankspan[0]

        ranking = (rank.text.strip())
        return '{}'.format(ranking)

    if len(rankspan) == 0:
        return "You haven't logged into tracker.gg or your added account doesn't exist "

def get_stats(valname, valid):
    page = requests.get("https://tracker.gg/valorant/profile/riot/{}%23{}/overview".format(valname, valid))
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='app')
    agent = results.find_all('span', class_='agent__name')
    if len(agent) == 3:
        first_agent = agent[0]
        topAGENT = (first_agent.text.strip())

        time = results.find_all('div', class_='text')
        time_total = time[0]
        time_played = (time_total.text.strip())

        kd = results.find_all('span', class_='value')
        big_kd = kd[4]
        kdratio = (big_kd.text.strip())

        big_hs = kd[5]
        headshots = (big_hs.text.strip())

        big_wr = kd[6]
        winrate = (big_wr.text.strip())

        rank_url = results.find_all('img', class_='valorant-rank-icon')
        rank_text = rank_url[0]
        rank_image = rank_text['src']

    return topAGENT, time_played, kdratio, headshots, winrate, rank_image

class Valorant(commands.Cog):
    @commands.group(invoke_without_command=True, name="valorant", help="Commands connected with game 'Valorant'")
    async def valorant(self, ctx: commands.Context):
        embed=discord.Embed(color=0xFF0000, title='**.valorant** <command>', description='Commands:\n  **add**   Example: .valorant add morph 25925\n  **rank**  Shows your current valorant rank\n  **stats** Get your valorant stats')
        await ctx.send(embed=embed)

    @valorant.command(name='stats', help='Get your valorant stats')
    async def stats(self, ctx: commands.Context):
        valname, valid = get_name(ctx.author.id)
        if (valname == None and valid == None):
            embed = discord.Embed(description='I dont have your valorant name and id, you can add it using .valorant add', color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                valorantRANKING = get_rank(valname, valid)
                if 'logged into' in valorantRANKING:
                    embed = discord.Embed(description=valorantRANKING, color=0xFF0000)
                else:
                    agent, time_played, kdratio, headshots, winrate, rank_image = get_stats(valname, valid)
                    embed = discord.Embed(title="VALORANT STATS", color=0x00bfff)
                    embed.set_thumbnail(url=rank_image)
                    embed.set_author(name=valname, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Most played agent", value=f'{agent} {time_played}', inline=False)
                    embed.add_field(name="Rank", value=valorantRANKING, inline=True)
                    embed.add_field(name="Winrate", value=winrate, inline=True)
                    embed.add_field(name="KD Ratio", value=kdratio, inline=False)
                    embed.add_field(name="Headshots", value=f'{headshots}%', inline=False)
                    embed.set_footer(text="Stats provided by tracker.gg")
            await ctx.send(embed=embed)

    @valorant.command(name='rank', help='Shows your current valorant rank')
    async def rank(self, ctx: commands.Context):
        valname, valid = get_name(ctx.author.id)
        if (valname == None and valid == None):
            embed = discord.Embed(description='I dont have your valorant name and id, you can add it using .valorant add', color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                valorantRANKING = get_rank(valname, valid)
            embed = discord.Embed(description=valorantRANKING, color=0x00bfff)
            await ctx.send(embed=embed)

    @valorant.command(name='add', help='Example: .valorant add morph 25925')
    async def add(self, ctx: commands.Context, valname, valid):
        status = data_add(ctx.author.id, valname, valid)
        embed = discord.Embed(description=status, color=0x90ee90)
        await ctx.send(embed=embed)

    @add.error
    async def add_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='**.valorant add** <riot name> <riot id>', color=0xFF0000)
            await ctx.send(embed=embed)
    
def setup(morph):
    morph.add_cog(Valorant(morph))