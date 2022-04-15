import discord
import traceback
import sys
from discord.ext import commands
from apps.embeds import Embed

embed = Embed()


class Owner(commands.Cog):
    def __init__(self, morph):
        self.morph = morph

    @commands.command(name="speak", hidden=True)
    @commands.is_owner()
    async def speak(self, ctx, channel: discord.TextChannel, *, msg):
        await channel.send(msg)

    @commands.command(name="react")
    @commands.is_owner()
    async def react(self, ctx, msg: discord.Message, emoji):
        await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.morph.get_channel(793570196614545450)
        embed.info(title="morph has been added to new server!")
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(
            name="Server name", 
            value=f"``{guild.name}``", 
            inline=True
        )
        embed.add_field(
            name="Server member count", 
            value=f"``{guild.member_count}``", 
            inline=True
        )
        await channel.send(embed=embed)
        await channel.send(f"morph is now in {len(self.morph.guilds)} servers")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed.info(
                title="Member not found!",
                description="Couldn't find member that you specified!",
            )
            await ctx.send(embed=embed)
        else:
            print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog):
        """Reload cog"""
        try:
            self.morph.unload_extension(cog)
            self.morph.load_extension(cog)
        except Exception as e:
            embed.error(
                title="RELOAD FAILED!", 
                description=f"**`ERROR:`** {e}",
            )
            await ctx.send(embed=embed)
        else:
            embed.info(
                title="RELOAD SUCCESFFUL!", 
                description=f"**``{cog}``** has been reloaded!",
            )
            await ctx.send(embed=embed)

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog):
        """Load cog"""
        try:
            self.morph.load_extension(cog)
        except Exception as e:
            embed.error(
                title="LOAD FAILED!", 
                description=f"**`ERROR:`** {e}",
            )
            await ctx.send(embed=embed)
        else:
            embed.info(
                title="LOAD SUCCESSFUL!", 
                description=f"**``{cog}``** has been loaded!",
            )
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="remrole", hidden=True)
    async def remrole(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)

    @commands.is_owner()
    @commands.command(name="addrole", hidden=True)
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)

def setup(morph):
    morph.add_cog(Owner(morph))