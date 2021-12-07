import discord
from discord.ext import commands
import requests, os
from pymongo import MongoClient

login = os.environ["mongo_login"]
client = MongoClient("mongodb+srv://{}@cluster0.1budm.mongodb.net/Morph_Users?retryWrites=true&w=majority".format(login))
db = client.Users

ranks = {"1": "Herald",
         "2": "Guardian",
         "3": "Crusader",
         "4": "Archon",
         "5": "Legend",
         "6": "Ancient",
         "7": "Divine",
         "8": "Immortal"}

def data_add(discord_id, steamid_64, steamid_32):
    dota = {
        'discord_id' : discord_id,
        'steamid_64' : steamid_64,
        'steamid_32' : steamid_32
    }

    user = db.dota.find_one( {'discord_id': discord_id} )

    if user == None:
        db.dota.insert_one(dota)
        return 'Added successfully'
    else:
        db.dota.update_one({'discord_id': discord_id},{ '$set': { "steamid_64": steamid_64 } })
        db.dota.update_one({'discord_id': discord_id},{ '$set': { "steamid_32": steamid_32 } })
        return 'Steam id updated successfully'

def get_steam(discord_id):
    user = db.dota.find_one({'discord_id': discord_id})
    if user == None:
        steamid32 = None
    else:
        steamid32 = user['steamid_32']
    return steamid32

class Profile:
    def __init__(self, steamid32):
        self.steamid32 = steamid32

    def get_rank(self):
        response = requests.get("https://api.opendota.com/api/players/{}".format(self.steamid32))
        text = response.json()
        rank_tier = text['rank_tier']
        if rank_tier == None:
            return 'private profile'
        else:
            stars = rank_tier%10
            name = int(rank_tier/10)
            actual_rank = ranks[f'{name}']
            if name == 8:
                leaderboard = text['leaderboard_rank']
                return f'{actual_rank} [{leaderboard}]'
            else:
                return f'{actual_rank} {stars}'

    def get_name(self):
        response = requests.get("https://api.opendota.com/api/players/{}".format(self.steamid32))
        text = response.json()
        if text['profile']['name'] == None:
            player_name = text['profile']['personaname']
        else:
            player_name = text['profile']['name']
        return f'{player_name}'

    def get_avatar(self):
        response = requests.get("https://api.opendota.com/api/players/{}".format(self.steamid32))
        text = response.json()
        avatar_url = text['profile']['avatarfull']
        return avatar_url

class Dota(commands.Cog):
    def __init__(self, morph):
        self.morph = morph       
    
    @commands.group(name='dota', invoke_without_command=True)
    async def dota(self, ctx):
        await ctx.send('Using dota group')
    
    @dota.command(name='add')
    async def add(self, ctx, steamid: int):
        steamid_64 = steamid
        steamid_32 = steamid - 76561197960265728
        status = data_add(ctx.author.id, steamid_64, steamid_32)
        embed = discord.Embed(description=status, color=0x90ee90)
        await ctx.send(embed=embed)

    @dota.command(name='profile')
    async def profile(self, ctx, steamid: int = None):
        if steamid == None:
            steamid = get_steam(ctx.author.id)
        else:
            steamid -= 76561197960265728
        status = Profile(steamid).get_rank()
        if status != None:
            embed = discord.Embed(description=f'**Rank**: ``{Profile(steamid).get_rank()}``')
            embed.set_author(name=f"{Profile(steamid).get_name()}'s profile", icon_url=f'{Profile(steamid).get_avatar()}')
            await ctx.send(embed=embed)
        else:
            await ctx.send(status)

def setup(morph):
    morph.add_cog(Dota(morph))