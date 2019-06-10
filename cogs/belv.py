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

        if sql.get_belmsg(reaction.message.id) != None:
            bel_id = sql.get_belmsg(reaction.message.id)
            bel_chid = sql.get_belmsg(reaction.message.id)[1]
            bel_ch = self.bot.get_channel(bel_chid)
            bel_msg = await bel_ch.fetch_message(bel_id[0])

            embed = discord.Embed(title="Nice message detected",
                                  description=f"A message in {reaction.message.channel.mention} was hyped!",
                                  color=0x000066)
            embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
            embed.add_field(name="Content", value=reaction.message.content, inline=True)
            embed.add_field(name="Hype-Count", value=reaction.count, inline=True)

            await bel_msg.edit(embed=embed)
        else:
            remoj = sql.get_settings(reaction.message.guild.id)["remoj"]

            rcount = sql.get_settings(reaction.message.guild.id)["rcount"]

            belvchid = sql.get_settings(reaction.message.guild.id)["belvchid"]
            belvch = self.bot.get_channel(belvchid)

            if str(reaction.emoji) == str(remoj):
                if reaction.count >= rcount:
                    embed = discord.Embed(title="Nice message detected",
                                          description=f"A message in {reaction.message.channel.mention} was hyped!",
                                          color=0x000066)
                    embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
                    embed.add_field(name="Content", value=reaction.message.content, inline=True)
                    embed.add_field(name="Hype-Count", value=reaction.count, inline=True)

                    msg = await belvch.send(embed=embed)

                    sql.set_belmsg(reaction.message.id, msg.id, msg.channel.id)

    @settings_created()
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.count >= sql.get_settings(reaction.message.guild.id)["rcount"]:
                bel_id = sql.get_belmsg(reaction.message.id)
                bel_chid = sql.get_belmsg(reaction.message.id)[1]
                bel_ch = self.bot.get_channel(bel_chid)
                bel_msg = await bel_ch.fetch_message(bel_id[0])

                embed = discord.Embed(title="Nice message detected",
                                      description=f"A message in {reaction.message.channel.mention} was hyped!",
                                      color=0x000066)
                embed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
                embed.add_field(name="Content", value=reaction.message.content, inline=True)
                embed.add_field(name="Hype-Count", value=reaction.count, inline=True)

                await bel_msg.edit(embed=embed)
        else:
            bel_id = sql.get_belmsg(reaction.message.id)
            bel_chid = sql.get_belmsg(reaction.message.id)[1]
            bel_ch = self.bot.get_channel(bel_chid)
            bel_msg = await bel_ch.fetch_message(bel_id[0])

            await bel_msg.delete()


def setup(bot):
    bot.add_cog(Belv(bot))