import discord
from discord.ext import commands, tasks
from datetime import datetime
from apps import covidLATVIA, weatherAPI
import os
morph = commands.Bot('.', description='MorphBOT COMMANDS', case_insensitive=True, intents=discord.Intents.all())
morph.remove_command('help')
message_channel = morph.get_channel(401071542110388257)

for cog in os.listdir('./cogs'):
    if cog.endswith('.py'):
        morph.load_extension(f'cogs.{cog[:-3]}')          

@morph.event #just to know that bot started
async def on_ready():
    users = len(set(morph.get_all_members()))
    await morph.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{users} retards'))
    print('Thot slayer ready')
    dailybrief.start()

@tasks.loop(minutes=1)
async def dailybrief():
    if datetime.utcnow().hour == 6 and datetime.utcnow().minute == 0:
        message_channel = morph.get_channel(401071542110388257)
        embed=discord.Embed(title="Goodest morning cotton pickers!", description=f'\n{covidLATVIA.get_covid()}\n\n:thermometer: Today average temperature is gonna be {weatherAPI.temperature()}\n\n:cloud_rain: There is {weatherAPI.rain_chance()} chance of rain and\n\n:snowflake: {weatherAPI.snow_chance()} chance of snow\n\nGood luck picking cotton today  :woozy_face:', color=0x00bfff)
        embed.set_author(name="Morph BOT", icon_url="https://i.imgur.com/tVGDT8m.png")
        await message_channel.send(embed=embed)

@morph.command(hidden='True')
@commands.is_owner()
async def off(ctx):
    await ctx.bot.logout()
morph.run(os.environ['TOKEN'])
