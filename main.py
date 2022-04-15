import discord
import os
import logging

from discord.ext import commands, tasks
from datetime import datetime
from apps import covidLATVIA, weatherAPI
from dotenv import load_dotenv
from apps.embeds import Embed

if __name__ == "__main__":
    load_dotenv()
    embed = Embed()
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    morph = commands.Bot(
        command_prefix=".",
        case_insensitive=True,
        intents=discord.Intents.all(),
    )
    morph.remove_command("help")

    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            morph.load_extension(f"cogs.{cog[:-3]}")


@morph.event
async def on_ready():
    users = len(set(morph.get_all_members()))
    await morph.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{users} retards"))
    logging.info("Thot slayer ready")
    dailybrief.start()


@tasks.loop(minutes=1)
async def dailybrief():
    if datetime.utcnow().hour == 6 and datetime.utcnow().minute == 0:
        message_channel = morph.get_channel(401071542110388257)
        embed.info(
            title="Goodest morning cotton pickers!",
            description=f"\n{covidLATVIA.get_covid()}\n\n \
                         :thermometer: Today average temperature is gonna be {weatherAPI.temperature()}\n\n \
                         :cloud_rain: There is {weatherAPI.rain_chance()} chance of rain and\n\n \
                         :snowflake: {weatherAPI.snow_chance()} chance of snow\n\n \
                         Good luck picking cotton today  :woozy_face:"
        )
        await message_channel.send(embed=embed)


morph.run(os.environ["TOKEN"])
