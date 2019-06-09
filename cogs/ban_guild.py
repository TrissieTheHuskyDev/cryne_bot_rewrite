import discord
from discord.ext import commands

import sql

class BanMechanics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(pass_ctx=True)
    async def ban_guild(self, ctx, dgid):
        sql.ban_guild(dgid)
        banned_guild = discord.utils.get(self.bot.guilds, id=int(dgid))

        await banned_guild.leave()

    @commands.is_owner()
    @commands.command(pass_ctx=True)
    async def unban_guild(self, ctx, dgid):
        sql.unban_guild(dgid)

def setup(bot):
    bot.add_cog(BanMechanics(bot))