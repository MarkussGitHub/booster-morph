import discord
from discord.ext import commands
import os, random
from pymongo import MongoClient
from datetime import datetime, timedelta

login = os.environ['mongo_login']

client = MongoClient("mongodb+srv://{}@cluster0.1budm.mongodb.net/Morph_Users?retryWrites=true&w=majority".format(login))
db = client.DiscordServers

def data_add(discord_id, server):
    economy = {
        'discord_id' : discord_id,
        'server' : server,
        'cash' : 0,
        'bank' : 0,
    }
    user = db.economy.find_one( {'discord_id': discord_id, 'server' : server} )
    if user == None:
        db.economy.insert_one(economy)
        return

def cash_add(discord_id, server):
    user = db.economy.find_one( {'discord_id': discord_id, 'server'  : server} )
    if user == None:
        data_add(discord_id, server)
    user = db.economy.find_one( {'discord_id': discord_id, 'server'  : server} )
    db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "cash": user['cash'] + 100 } })
    db.dailybonus.insert_one( {"createdAt": datetime.utcnow(), "discord_id" : discord_id, 'server': server} )
    user = db.economy.find_one( {'discord_id': discord_id, 'server'  : server} )
    db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "balance": user['cash']+user['bank'] } })
    return 'Daily bonus claimed!'

def balance(discord_id, server):
    user = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
    if user == None:
        data_add(discord_id, server)
    user = db.economy.find_one( {'discord_id': discord_id, 'server'  : server})
    
    return user['cash'], user['bank']

def balance_top(server):
    server_found = db.economy.find({'server' : server}).sort("balance", -1)
    if db.economy.count_documents({}) < 0:
        return 'No one has money'
    if db.economy.count_documents({}) > 0:
        return server_found

def send(discord_id, server, who, amount):
    sender = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
    if sender == None:
        data_add(discord_id, server)
    receiver = db.economy.find_one( {'discord_id': who, 'server' : server})
    if receiver == None:
        data_add(who, server)
    sender = db.economy.find_one( {'discord_id': discord_id, 'server' : server} )
    receiver = db.economy.find_one( {'discord_id': who, 'server' : server})
    cash = sender['cash']
    if amount > cash <=0 or amount > cash:
        return 'You dont have enough funds to do that!'
    else:
        receivercash = receiver['cash']
        newcash = cash - amount
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "cash": newcash } })
        newcash = receivercash + amount
        db.economy.update_one({'discord_id': who, 'server'  : server},{ '$set': { "cash": newcash } })
        sender = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
        receiver = db.economy.find_one( {'discord_id': who, 'server' : server})
        db.economy.update_one({'discord_id': who, 'server'  : server},{ '$set': { "balance": receiver['cash']+receiver['bank'] } })
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "balance": sender['cash']+sender['bank'] } })
        return 'Sent **{}**$ to <@{}>'.format(amount, who)

def deposit(discord_id, server, amount):
    user = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
    if user == None:
        data_add(discord_id, server)
    user = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
    if user['cash'] <= 0 or amount > user['cash']:
        return 'You dont have funds to do that!'
    else:
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "bank": user['bank'] + amount } })
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "cash": user['cash'] - amount } })
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "balance": user['cash']+user['bank'] } })

        return 'Deposit into bank was successful!'

def withdraw(discord_id, server, amount):
    user = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
    if user == None:
        data_add(discord_id, server)
    user = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
    if user['bank'] <= 0 or amount > user['bank']:
        return 'You dont have funds to do that!'
    else:
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "bank": user['bank'] - amount } })
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "cash": user['cash'] + amount } })
        db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "balance": user['cash']+user['bank'] } })
        
        return 'Withdrawal was successful!'

def rob(discord_id, server, who):
    victim = db.economy.find_one( {'discord_id': who, 'server' : server})
    if victim == None:
        data_add(who, server)
    victim = db.economy.find_one( {'discord_id': who, 'server' : server})
    if victim['cash'] <= 0:
        return "<@!{}>'s wallet is empty, you cant rob them!".format(who)
    else:
        robber = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
        if robber == None:
            data_add(discord_id, server)
        robber = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
        possibleScenarios = ['success',
                             'cops',
                             'played']
        scenario = random.choice(possibleScenarios)         
        if scenario == 'success':
            amount = random.randint(1, victim['cash'])
            db.economy.update_one({'discord_id': who, 'server'  : server},{ '$set': { "cash": victim['cash'] - amount } })
            victim = db.economy.find_one( {'discord_id': who, 'server' : server})
            db.economy.update_one({'discord_id': who, 'server'  : server},{ '$set': { "balance": victim['cash'] + victim['bank'] } })
            db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "cash": robber['cash'] + amount } })
            robber = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
            db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "balance": robber['cash'] + robber['bank'] } })
            return "<@!{}> stole **{}**$ from <@!{}>!".format(discord_id, amount, who)
        elif scenario == 'cops':
            db.robbery.insert_one( {"createdAt": datetime.utcnow(), "discord_id" : discord_id, 'server': server} )
            return "Morph patrol caught <@!{}>, trying to steal!.\n<@!{}> got 30 minutes prison time.".format(discord_id, discord_id)
        elif scenario == 'played':
            weapons = [':knife:',
                       ':gun:',
                       ':banjo:']
            weapon = random.choice(weapons)
            amount = random.randint(1, robber['cash'])
            db.economy.update_one({'discord_id': who, 'server'  : server},{ '$set': { "cash": victim['cash'] + amount } })
            victim = db.economy.find_one( {'discord_id': who, 'server' : server})
            db.economy.update_one({'discord_id': who, 'server'  : server},{ '$set': { "balance": victim['cash'] + victim['bank'] } })
            db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "cash": robber['cash'] - amount } })
            robber = db.economy.find_one( {'discord_id': discord_id, 'server' : server})
            db.economy.update_one({'discord_id': discord_id, 'server'  : server},{ '$set': { "balance": robber['cash'] + robber['bank'] } })
            return "Jokes on you! <@!{}> pulled out a {} and stole **{}**$ from you instead!".format(who, weapon, amount)

    
class Economy(commands.Cog):
    @commands.group(invoke_without_command=True, name='balance', help='Check your balance')
    async def balance(self, ctx: commands.Context, user : discord.User):
        cash, card = balance(user.id, ctx.guild.id)
        embed = discord.Embed(description=f':dollar: **{cash}**$ in cash :credit_card: **{card}**$ in bank.', color=0x00bfff)
        embed.set_author(name=f'{user.name}`s Balance', icon_url=user.avatar_url)
        embed.set_footer(text='TIP: Be careful, if you keep money in cash someone might steal it from you.')
        await ctx.send(embed=embed)

    @balance.error
    async def balance_error(self, ctx: commands.context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            cash, card = balance(ctx.author.id, ctx.guild.id)
            embed = discord.Embed(description=f':dollar: **{cash}**$ in cash :credit_card: **{card}**$ in bank.', color=0x00bfff)
            embed.set_author(name=f'{ctx.author.name}`s Balance', icon_url=ctx.author.avatar_url)
            embed.set_footer(text='TIP: Be careful, if you keep money in cash someone might steal it from you.')
            await ctx.send(embed=embed)

    @balance.command(name='top', help='Balance top')
    async def top(self, ctx: commands.Context):
        server_top = balance_top(ctx.guild.id)
        top_list = []
        for item in server_top:
            try:
                print(item['discord_id'], item['balance'])
            except KeyError:
                pass

        #embed=discord.Embed(title='Balance top', description=f'**``1.``** <@!{top1}> **{balance1}**$\n**``2.``** <@!{top2}> **{balance2}**$\n**``3.``** <@!{top3}> **{balance3}**$\n**``4.``** <@!{top4}> **{balance4}**$\n**``5.``** <@!{top5}> **{balance5}**$')
        #await ctx.send(embed=embed)

    @commands.command(name='daily', help='Claim daily bonus')
    async def daily(self, ctx: commands.Context):
        user = db.dailybonus.find_one( {'discord_id': ctx.author.id, 'server' : ctx.guild.id} )
        if user == None:
            status = cash_add(ctx.author.id, ctx.guild.id)
            embed = discord.Embed(description=status, color=0x90ee90)
            await ctx.send(embed=embed)
        else:
            exp_date = user['createdAt'] + timedelta(hours=23, minutes=59, seconds=59)
            timer = (exp_date - datetime.utcnow()).seconds
            if timer > 3600:
                hours = int(timer // 3600)
                minutes = int(timer // 60) - int(hours * 60)
                embed=discord.Embed(title='Daily bonus already claimed!', description='**{}** hours, **{}** minutes until your next daily bonus!'.format(hours, minutes), color=0xFF0000)
                await ctx.send(embed=embed)
            if timer <= 3600:
                minutes = int(timer // 60)
                embed=discord.Embed(title='Daily bonus already claimed!', description='**{}** minutes until your next daily bonus!'.format(minutes), color=0xFF0000)
                await ctx.send(embed=embed)
            if timer <= 60:
                seconds = int(timer // 1)
                embed=discord.Embed(title='Daily bonus already claimed!', description='**{}** seconds until your next daily bonus!'.format(seconds), color=0xFF0000)
                await ctx.send(embed=embed)

    @commands.command(name='send', help ='Send money to someone')
    async def send(self, ctx: commands.Context, who : discord.User, amount: int):
        status = send(ctx.author.id, ctx.guild.id, who.id, amount)
        if status == 'You dont have enough funds to do that!':
            color=0xFF0000
        else:
            color=0x90ee90
        embed = discord.Embed(description=status, color=color)
        await ctx.send(embed=embed)

    
    @send.error
    async def send_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Example:', description='**.send** <@!701412134034341888> 200', color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='deposit', help='Deposit cash into a bank')
    async def deposit(self, ctx: commands.Context, amount: int):
        status = deposit(ctx.author.id, ctx.guild.id, amount)
        if status == 'You dont have enough funds to do that':
            color=0xFF0000
        else:
            color=0x90ee90
        embed = discord.Embed(description=status, color=color)
        await ctx.send(embed=embed)
    
    @deposit.error
    async def deposit_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='You didnt specify amount.', color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='withdraw', help='Withdraw money from bank')
    async def withdraw(self, ctx: commands.Context, amount: int):
        status = withdraw(ctx.author.id, ctx.guild.id, amount)
        if status == 'You dont have enough funds to do that':
            color=0xFF0000
        else:
            color=0x90ee90
        embed = discord.Embed(description=status, color=color)
        await ctx.send(embed=embed)

    @withdraw.error
    async def withdraw_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='You didnt specify amount.', color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='rob', help='U can try to steal from someone.')
    async def rob(self, ctx: commands.Context, who : discord.User):
        robber = db.robbery.find_one( {'discord_id': ctx.author.id, 'server' : ctx.guild.id})
        if who==ctx.author:
            embed = discord.Embed(description='Why would u want to rob yourself dumbass')
            await ctx.send(embed=embed)
        else:
            if robber == None:
                status = rob(ctx.author.id, ctx.guild.id, who.id)
                embed = discord.Embed(description=status)
                if 'Morph patrol caught' in status:
                    embed = discord.Embed(description=status)
                    embed.set_image(url='https://i.imgur.com/10nwYdV.png')
                elif 'Jokes on you' in status:
                    embed = discord.Embed(description=status)
                await ctx.send(embed=embed)
            else:
                exp_date = robber['createdAt'] + timedelta(minutes=30)
                timer = (exp_date - datetime.utcnow()).seconds
                if timer <= 1800:
                    minutes = int(timer // 60)
                    embed=discord.Embed(title='U are in jail!', description='**{}** minutes until you are let go!'.format(minutes), color=0xFF0000)
                    await ctx.send(embed=embed)
                if timer <= 60:
                    seconds = int(timer // 1)
                    embed=discord.Embed(title='U are in jail!', description='**{}** seconds until you are let go!'.format(seconds), color=0xFF0000)
                    await ctx.send(embed=embed)

    @rob.error
    async def rob_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='You didnt mention anyone to rob.', color=0xFF0000)
            await ctx.send(embed=embed)
    
def setup(morph):
    morph.add_cog(Economy(morph))