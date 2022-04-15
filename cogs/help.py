from discord.ext import commands
from apps.embeds import Embed

embed = Embed()


class Help(commands.Cog):
    def __init__(self, morph):
        self.morph = morph

    def cmd_list(self, cog) -> str:
        """Returns command list for given cog as string."""
        cmdlist = []
        for cmd in self.morph.commands:
            if not cmd.hidden and cmd.cog_name == cog:
                cmdlist.append(cmd.name)

        cmdlist = ", ".join(sorted(cmdlist))
        return cmdlist

    @commands.command(name="help", help="Everyone needs a bit of help", hidden=True)
    async def help(self, ctx, command=None):
        if command:
            try:
                cmd = [cmd for cmd in self.morph.commands if cmd.name == command][0]

            except IndexError:
                embed.error(description="There is no such command")

            else:
                embed.info(
                    title=f"{command.capitalize()} Help",
                    description=cmd.help if cmd.help else None
                )

                params = cmd.clean_params.keys()
                params_string = ""

                if params:
                    for p in params:
                        params_string += f"<{p}> "

                field_value = f".{command} {params_string}".strip()

                embed.add_field(
                    name="Usage",
                    value=f"```{field_value}```"
                )

                if cmd.aliases:
                    aliaslist = ", ".join(cmd.aliases)

                    embed.add_field(
                        name="Aliases",
                        value=f"```{aliaslist}```",
                        inline=False
                    )

        else:
            embed.info(title="Morph Help")
            for ctgry in sorted(self.morph.cogs):
                if ctgry not in ["Owner", "Help"]:
                    embed.add_field(
                        name=ctgry,
                        value=f"```{self.cmd_list(ctgry)}```",
                        inline=False
                    )
            embed.set_footer(
                text=".help <command name> to see info on specific command")

        await ctx.send(embed=embed)


def setup(morph):
    morph.add_cog(Help(morph))
