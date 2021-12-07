import discord
import traceback
import sys
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, morph):
        self.morph = morph

    @commands.command(name='eval', hidden=True)
    @commands.is_owner()
    async def eval_(self, ctx, *, code):
        code = code[6:-4]
        try:
            exec("async def toEval():\n"
                + "".join(f"\n  {line}" for line in code.split("\n")),
                locals())
            await locals()["toEval"]()
        except Exception:
            embed = discord.Embed(
                title="Error",
                description=f"```{traceback.format_exc()}```",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='speak', hidden=True)
    @commands.is_owner()
    async def speak(self, ctx, channel: discord.TextChannel, *, msg):
        await channel.send(msg)

    @commands.command(name='react')
    @commands.is_owner()
    async def react(self, ctx, msg: discord.Message, emoji):
        await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.morph.get_channel(793570196614545450)
        embed = discord.Embed(title='morph has been added to new server!')
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='Server name', value=f'``{guild.name}``', inline=True)
        embed.add_field(name='Server member count', value=f'``{guild.member_count}``', inline=True)
        await channel.send(embed=embed)
        await channel.send(f'morph is now in {len(self.morph.guilds)} servers')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title='Member not found!',
                                  description='Couldnt find member that you specified!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog):
        """Reload cog"""
        try:
            self.morph.unload_extension(cog)
            self.morph.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title='RELOAD FAILED!', description=f'**`ERROR:`** {e}', color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='RELOAD SUCCESFFUL!', description=f'**``{cog}``** has been reloaded!', color=0x90ee90)
            await ctx.send(embed=embed)

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog):
        """Load cog"""
        try:
            self.morph.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title='LOAD FAILED!', description=f'**`ERROR:`** {e}', color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='LOAD SUCCESSFUL!', description=f'**``{cog}``** has been loaded!', color=0x90ee90)
            await ctx.send(embed=embed)

def setup(morph):
    morph.add_cog(Owner(morph))