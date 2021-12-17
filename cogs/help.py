import discord
from discord.ext import commands, tasks

class Help(commands.Cog):
    def __init__(self, morph):
        self.morph = morph

    def cmd_list(self, cog):
        cmdlist = []
        for cmd in self.morph.commands:
            if cmd.cog_name == cog:
                if cmd.hidden == False:
                    cmdlist.append(cmd.name)

        cmdlist = ', '.join(cmdlist)
        return cmdlist

    def ctgry_list(self):
        ctgrylist = []
        forbidden = ['Owner', 'Help']
        for ctgry in self.morph.cogs:
            if ctgry not in forbidden:
                ctgrylist.append(ctgry)

        ctgrylist = ', '.join(ctgrylist)
        return ctgrylist

    @commands.command(name='help', help='Everyone needs a bit of help', hidden=True)
    async def help(self, ctx, cmd = None):
        if cmd == None:
            page1 = discord.Embed(title='Morph Help', color=0xF2F2F2)
            page1.add_field(name='Fun', value=f'```{self.cmd_list("Fun")}```', inline=False)
            page1.add_field(name='Music', value=f'```{self.cmd_list("Music")}```', inline=False)
            page1.add_field(name='Dota', value=f'```{self.cmd_list("Dota")}```', inline=False)
            page1.add_field(name='Moderation', value=f'```{self.cmd_list("Moderation")}```', inline=False)
            page1.add_field(name='Economy', value=f'```{self.cmd_list("Economy")}```', inline=False)
            page1.set_footer(text='.help <command name> to see info on specific command')
            await ctx.send(embed=page1)
        else:
            for command in self.morph.commands:
                if command.name == cmd:
                    for key, value in command.clean_params.items():
                        arg = key
                        break
                    else:
                        arg = None
                    embed = discord.Embed(title=f'{cmd.capitalize()} Help', description=command.help if command.help != None else "No usage description")
                    if arg != None:
                        embed.add_field(name='Usage', value=f'```.{cmd} <{arg}>```')
                    else:
                        embed.add_field(name='Usage', value=f'```.{cmd}```')

                    if len(command.aliases) > 0:
                        aliaslist = ', '.join(command.aliases)
                    else:
                        aliaslist = None

                    embed.add_field(name='Aliases', value=f'```{aliaslist}```', inline=False)
                    await ctx.send(embed=embed)
                    break
            else:
                embed = discord.Embed(description='There is no such command', color=0xFF0000)
                await ctx.send(embed=embed)

def setup(morph):
    morph.add_cog(Help(morph))