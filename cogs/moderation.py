import discord
from discord.ext import commands
import os
from pymongo import MongoClient
from typing import Union
from random import choice

login = os.environ['mongo_login']
client = MongoClient("mongodb+srv://{}@cluster0.1budm.mongodb.net/Morph_Users?retryWrites=true&w=majority".format(login))
db = client.DiscordServers

def data_add(owner_id, server_id, role_name):
    Servers = {
        'owner_id' : owner_id,
        'server_id' : server_id,
        'role_name' : role_name
    }

    owner = db.Servers.find_one( {'owner_id': owner_id} )

    if owner == None:
        db.Servers.insert_one(Servers)
        return
    else:
        db.Servers.update_one({'owner_id': owner_id},{ '$set': { "server_id": server_id } })
        db.Servers.update_one({'owner_id': owner_id},{ '$set': { "role_name": role_name } })
        return

def get_role(server_id):
    owner = db.Servers.find_one({'server_id': server_id})
    if owner == None:
        role_name = None
    else:
        role_name = owner['role_name']
    return role_name

def channel_add(owner_id, server_id, channel_name):
    Channels = {
        'owner_id' : owner_id,
        'server_id' : server_id,
        'channel_name' : channel_name
    }

    owner = db.Channels.find_one( {'owner_id': owner_id} )

    if owner == None:
        db.Channels.insert_one(Channels)
        return
    else:
        db.Channels.update_one({'owner_id': owner_id},{ '$set': { "server_id": server_id } })
        db.Channels.update_one({'owner_id': owner_id},{ '$set': { "role_name": channel_name } })
        return

def get_channel(server_id):
    owner = db.Channels.find_one({'server_id': server_id})
    if owner == None:
        channel_name = None
    else:
        channel_name = owner['channel_name']
    return channel_name



class Moderation(commands.Cog):
    def __init__(self, morph):
        self.morph = morph

    class BannedUser(commands.Converter):
        async def convert(self, ctx, id: int):
            bot = ctx.bot
            try:
                user = await bot.fetch_user(id)
            except discord.errors.HTTPException:
                return None
            else:
                return user

    @commands.command(name='checkperms')
    async def checkperms(self, ctx, member: Union[discord.Member, discord.Role] = None):
        if member == None:
            member = ctx.author
        if type(member).__name__ == 'Member':
            rolelist=[]
            for perm in member.guild_permissions:
                if perm[1] == True:
                    rolelist.append(perm[0])
            embed = discord.Embed(title=f"{member.display_name}`s permissions",
                                  description=f"```{', '.join(rolelist)}```")
        else:
            rolelist=[]
            for perm in member.permissions:
                if perm[1] == True:
                    rolelist.append(perm[0])
            embed = discord.Embed(title=f"{member.name}`s permissions",
                                  description=f"```{', '.join(rolelist)}```")
        await ctx.send(embed=embed)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, id: BannedUser, reason: str = 'None'):
        if id != None:
            embed = discord.Embed(title='Ban remove successful!', 
                                    description=f'{ctx.author.mention} unbanned **{id.display_name}**!',
                                    color=0xF2F2F2)
            embed.add_field(name='Reason', value=f'``{reason}``')
            await ctx.guild.unban(user=id, reason=reason)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='ID not found!',
                                  description='You gave me incorrect id, or the person isnt banned!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Member not specified!',
                                  description='You didnt specify member to unban!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing permissions!',
                                  description='You dont have permissions to unban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='Bot is missing permissions!',
                                  description='Bot doesnt have permissions to unban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = 'None'):
        if ctx.author.guild_permissions > member.guild_permissions < ctx.guild.me.guild_permissions:
            embed = discord.Embed(title='Ban successful!', 
                                  description=f'{ctx.author.mention} banned **{member.display_name}**!',
                                  color=0xF2F2F2)
            embed.add_field(name='Reason', value=f'``{reason}``')
            await ctx.guild.ban(user=member, reason=reason)
            await ctx.send(embed=embed)
        elif ctx.author.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Ban unsuccessful!', 
                                  description=f'Couldnt ban **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than you!``')
            await ctx.send(embed=embed)
        elif ctx.guild.me.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Ban unsuccessful!', 
                                  description=f'Couldnt ban **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than me!``')


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Member not specified!',
                                  description='You didnt specify member to ban!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing permissions!',
                                  description='You dont have permissions to ban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='Bot is missing permissions!',
                                  description='Bot doesnt have permissions to ban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title='Member not found!',
                                  description='Couldnt find member that you specified!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = 'None'):
        if ctx.author.guild_permissions > member.guild_permissions < ctx.guild.me.guild_permissions:
            embed = discord.Embed(title='Kick successful!', 
                                  description=f'{ctx.author.mention} kicked **{member.display_name}**!',
                                  color=0xF2F2F2)
            embed.add_field(name='Reason', value=f'``{reason}``')
            await ctx.guild.kick(user=member, reason=reason)
            await ctx.send(embed=embed)
        elif ctx.author.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Kick unsuccessful!', 
                                  description=f'Couldnt kick **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than you!``')
            await ctx.send(embed=embed)
        elif ctx.guild.me.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Kick unsuccessful!', 
                                  description=f'Couldnt kick **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than me!``')


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Member not specified!',
                                  description='You didnt specify member to kick!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing permissions!',
                                  description='You dont have permissions to kick people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='Bot is missing permissions!',
                                  description='Bot doesnt have permissions to kick people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title='Member not found!',
                                  description='Couldnt find member that you specified!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_name = get_channel(member.guild.id)
        channel = discord.utils.get(member.guild.channels, name=channel_name)
        embed=discord.Embed(description=f'Hey {member.mention}, welcome to **{member.guild}**!', color=0x00bfff)
        await channel.send(embed=embed)
        role_name = get_role(member.guild.id)
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role != None:
            await member.add_roles(role)
        if role == None:
            pass
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_name = get_channel(member.guild.id)
        channel = discord.utils.get(member.guild.channels, name=channel_name)
        embed=discord.Embed(description=f"We didn't want **{member.name}** anyways, fucking loser", color=0x00bfff)
        await channel.send(embed=embed)

    @commands.command(name='welcome', help='Set welcome message channel (case sensitive)')
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, *, channel_name):
        channel_add(ctx.author.id, ctx.guild.id, channel_name)
        embed=discord.Embed(description='Welcome message channel is set to "{}"!'.format(channel_name), color=0x00bfff)
        await ctx.send(embed=embed)

    @welcome.error
    async def welcome_error(self , ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='You dont have permissions to do that', color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='You forgot to tell me which channel', color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='autorole', help='Set role which new users get')
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, *, role_name):
        data_add(ctx.author.id, ctx.guild.id, role_name)
        embed=discord.Embed(description='New member role is set to "{}"!'.format(role_name), color=0x00bfff)
        await ctx.send(embed=embed)

    @autorole.error
    async def autorole_error(self , ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description='You dont have permissions to do that', color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='You forgot to tell me which role', color=0xFF0000)
            await ctx.send(embed=embed)
    
    @commands.command(name='suggest', help='Suggest a feature or report a bug.')
    async def suggest(self, ctx, *, message):
        user = self.morph.get_user(201651700753367040)
        await user.send(f'{message}\nFrom {ctx.author.mention} in server {ctx.guild.name}')
        embed = discord.Embed(description='Your suggestion was sent, thank you for your feedback!', color=0x90ee90)
        await ctx.send(embed=embed)

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          embed = discord.Embed(description='Please write a message if u want to suggest something.', color=0xFF0000)
        await ctx.send(embed=embed)

    @commands.command(name="wakeup")
    async def wakeup(ctx, member: discord.Member):
        if ctx.author.id in [369539585342177286,201651700753367040]:
            ch1 = member.voice.channel
            ch_list = ctx.guild.voice_channels
            ch_list.remove(ch1)
            for _ in range(5):
                ch2 = choice(ch_list)
                await member.move_to(ch2)
            await member.move_to(ch1)
        else:
            await ctx.send("fuck off")

def setup(morph):
    morph.add_cog(Moderation(morph))