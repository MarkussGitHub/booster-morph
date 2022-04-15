import discord
import random, requests
from io import BytesIO
from discord.ext import commands
from apps.covidLATVIA import get_covid
from apps.embeds import Embed
from discord import Spotify
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

embed = Embed()


class Fun(commands.Cog):
    def __init__(self, morph):
        self.morph = morph

    @commands.command(name="poll", help="Make a poll")
    async def poll(self, ctx, *, question: str):
        embed.info(
            title="Poll",
            description=question
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

    @commands.command(name="avatar")
    async def avatar(self, ctx, *, user: discord.User = None):
        if user == None:
            r = requests.get(ctx.author.avatar_url)
        else:
            r = requests.get(user.avatar_url)
        avatar = Image.open(BytesIO(r.content))
        buffer = BytesIO()
        avatar.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, "avatar.png")
        await ctx.send(file=file)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed.error(title="Couldnt find that member")
            await ctx.send(embed=embed)

    @commands.command(name="spotify", aliases=["sp"], help="Flex with your music, or check out what others listen to")
    async def spotify(self, ctx, *, user: discord.Member = None):
        sp = None
        if user == None:
            user = ctx.author
        
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    sp = activity

        if sp == None:
            if user == ctx.author:
                embed.error(description="You arent listening to anything")
                await ctx.send(embed=embed)
            else:
                embed.error(description=f"{user.display_name} isn't listening to anything")
                await ctx.send(embed=embed)
        else:
            spotify = Image.new("RGBA", (500, 220), "white")
            line = Image.open("src/line.png")
            songFont = ImageFont.truetype("src/arialUnicode.ttf", 24, encoding="unic")
            artistFont = ImageFont.truetype("src/arialUnicode.ttf", 16, encoding="unic")
            timeFont = ImageFont.truetype("src/arialUnicode.ttf", 12, encoding="unic")

            r = requests.get(sp.album_cover_url)
            bg = Image.open(BytesIO(r.content)).filter(ImageFilter.GaussianBlur(radius=6))
            enhancer = ImageEnhance.Brightness(bg)
            newBG = enhancer.enhance(0.55)
            album_cover = Image.open(BytesIO(r.content)).resize((100 ,100))
            spotify.paste(newBG, (-80, -150))
            spotify.paste(album_cover, (200, 20))

            if len(sp.title) >= 37:
                title = f"{sp.title[:37]}..."
            else:
                title = sp.title

            artist = sp.artist.replace(";", ", ")

            if len(sp.artist) >= 60:
                artist = f"{artist[:60]}..."
            else:
                artist = artist

            draw = ImageDraw.Draw(spotify)
            w, h = draw.textsize(title, font=songFont)
            draw.text(((500-w)/2, 130), u"{}".format(title), font=songFont, fill="white")

            w, h = draw.textsize(artist, font=artistFont)
            draw.text(((500-w)/2, 160), u"{}".format(artist), font=artistFont, fill="white")

            ongoing = sp.end - datetime.utcnow()
            ongoing = str((sp.duration - ongoing).total_seconds()).split(".")[0]
            ongoingMinutes = int(ongoing) // 60
            ongoingSeconds = int(ongoing) % 60
            ongoingSeconds = f"{ongoingSeconds:02d}"
            ongoing = f"{ongoingMinutes}:{ongoingSeconds}"
            draw.text((90, 190), ongoing, font=timeFont, fill="white")

            duration = str(sp.duration.total_seconds()).split(".")[0]
            maxMinutes = int(duration) // 60
            maxSeconds = int(duration) % 60
            maxSeconds = f"{maxSeconds:02d}"
            duration = f"{maxMinutes}:{maxSeconds}"
            draw.text((385, 190), duration, font=timeFont, fill="white")

            spotify.paste(line, (0, 175), line)

            buffer = BytesIO()
            spotify.save(buffer, format="PNG")
            buffer.seek(0)
            file = discord.File(buffer, "spotify.png")
            embed.info(description=f"[Listen on spotify](https://open.spotify.com/track/{sp.track_id})")
            embed.set_image(url="attachment://spotify.png")
            await ctx.send(embed=embed, file=file)


    @commands.command(name="meme", help="Generate meme")
    async def meme(self, ctx: commands.Context):
        image = requests.get("https://meme-api.herokuapp.com/gimme").json()
        embed.info()
        embed.set_image(url=image["url"])
        await ctx.send(embed=embed)

    @commands.command(name="covid", help="Shows covid cases for past 24 hours in latvia.")
    async def covid(self, ctx: commands.Context):
        embed.info(description=get_covid())
        await ctx.send(embed=embed)

    @commands.command(name="morph", help="Ask yes/no question to the AI himself.") #this is just an 8ball
    async def morph(self, ctx: commands.Context, *, question):
        responses = [
            "yes",
            "most likely",
            "as i see it, yes",
            "my sources say no",
            "very doubtful",
            "no lol",
            "no, fucking dumbass",
            "the fuck you talking bout",
            "shut yo bitch ass up",
            "there is a huge possibility that you are correct",
            "ask someone else, im busy",
        ]

        embed.info(description=f"{ctx.author.mention} {random.choice(responses)}")
        await ctx.send(embed=embed)

    @morph.error
    async def morph_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed.error(description="You didnt ask anything")
            await ctx.send(embed=embed)

    @commands.command(name="roll", help="Rolls a number 0-100")
    async def roll(self, ctx: commands.Context):
        embed.info(description=f"{ctx.author.mention} rolled {random.randrange(100)}")
        await ctx.send(embed=embed)

    @commands.command(name="flip", help="Flips a coin") #this command flips a coin
    async def flip(self, ctx: commands.Context):
        coins = [
            "HEADS",
            "TAILS",
        ]
        embed.info(description=f"**{random.choice(coins)}**")
        await ctx.send(embed=embed)

def setup(morph):
    morph.add_cog(Fun(morph))