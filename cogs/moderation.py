import discord
from discord.ext import commands

from command_checks import settings_created

class ModTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def kick(self, ctx, user : discord.User):
        await ctx.guild.kick(user)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def ban(self, ctx, user: discord.User):
        await ctx.guild.ban(user)


    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def purge(self, ctx, count=1000):
        await ctx.channel.purge(limit=int(count))
        await ctx.channel.send(f"{count} messages deleted!", delete_after=5)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def delete(self, ctx, count):
        async for msg in ctx.channel.history(limit=int(count)):
            await msg.delete()
        await ctx.channel.send(f"{count} messages deleted!", delete_after=5)

def setup(bot):
    bot.add_cog(ModTools(bot))