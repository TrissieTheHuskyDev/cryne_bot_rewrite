import discord
from discord.ext import commands
import asyncio

import sql

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_ctx=True)
    async def info(self, ctx):
        paddi = self.bot.get_user(369129934917992450)
        tb = self.bot.get_user(583738641503879184)
        embed = discord.Embed(title="Info: cryne_bot",
                              url="https://github.com/itsCryne/cryne_bot_rewrite/blob/master/README.md",
                              description="cryne_bot, programmed by " + paddi.mention, color=0xffb82b)
        embed.set_author(name="cryne_bot", url="https://github.com/itsCryne/cryne_bot_rewrite", icon_url=tb.avatar_url)
        embed.add_field(name="A (more or less) simple moderation bot",
                        value="Currently present on " + str(len(self.bot.guilds)) + " guilds with " + str(len(self.bot.users)) + " members")
        await ctx.send(embed=embed)

    @commands.command(pass_ctx=True)
    async def register_users(self, ctx):
        for member in self.bot.users:
            sql.delete_user(member.id)

        for member in self.bot.users:
            sql.register_user(member.id, member.name)

def setup(bot):
    bot.add_cog(Misc(bot))