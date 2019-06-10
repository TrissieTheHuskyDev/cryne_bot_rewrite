import discord
from discord.ext import commands

from command_checks import settings_created

import sql

class Belv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @settings_created()
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        remoj = sql.get_settings(reaction.message.guild.id)["remoj"]

        rcount = sql.get_settings(reaction.message.guild.id)["rcount"]

        belvchid = sql.get_settings(reaction.message.guild.id)["belvchid"]
        belvch = self.bot.get_channel(belvchid)

        if str(reaction.emoji) == str(remoj):
            if reaction.count >= rcount:
                embed = discord.Embed(title="Nice message detected",
                                      description=f"A message in {reaction.message.channel.mention} was hyped!", color=0xff0000)
                embed.set_author(name=user, icon_url=user.avatar_url)
                embed.add_field(name="Content", value=reaction.message.content, inline=True)

                await belvch.send(embed=embed)

        #print(str(reaction.emoji) == str(remoj))


def setup(bot):
    bot.add_cog(Belv(bot))