import discord
from discord.ext import commands

class CogHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_ctx=True)
    async def reload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description=f':warning: {type(e).__name__} - {e} :warning:',
                                  color=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Success",
                                  description=f':white_check_mark:  {cog} reloaded :white_check_mark:',
                                  color=0x006400)
            await ctx.send(embed=embed)

    @commands.command(pass_ctx=True)
    async def load_cog(self, ctx, cog):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title="Error",
                                  description=f':warning: {type(e).__name__} - {e} :warning:',
                                  color=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Success",
                                  description=f':white_check_mark:  {cog} reloaded :white_check_mark:',
                                  color=0x006400)
            await ctx.send(embed=embed)

    @commands.command(pass_ctx=True)
    async def unload_cog(self, ctx, cog):
        if cog == "cogs.cog_handler":
            embed = discord.Embed(title="Error",
                                  description=":rotating_light: You can't unload the cog_handler cog! :rotating_light:",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            embed = discord.Embed(title="Success",
                                  description=f':warning: {type(e).__name__} - {e} :warning:',
                                  color=0xff0000)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f':white_check_mark:  {cog} unloaded :white_check_mark: ')


def setup(bot):
    bot.add_cog(CogHandler(bot))