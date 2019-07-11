import discord
from discord.ext import commands
from io import BytesIO

class FunCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_ctx=True)
    async def sleep(self, ctx):
        await ctx.send("**Days without ppl using lack of sleep as an execuse:** 0")

    @commands.command(pass_ctx=True)
    async def rtfm(self, ctx):
        embed = discord.Embed(title="Documentations", description="Just rtfm and be happy!", color=0xd24949)
        embed.add_field(name="discord.py", value="[readthedocs](https://discordpy.readthedocs.io/en/latest/index.html)", inline = True)
        embed.add_field(name="discord.js", value="[d.js page](https://discord.js.org/#/docs/main/stable/general/welcome)", inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_ctx=True)
    async def avatar(self, ctx, member : discord.Member = None):
        if member == None:
            member =  ctx.message.author

        av = BytesIO(await member.avatar_url.read())

        await ctx.send(f"Hey {member.mention}, hier ist dein Avatar:", file=discord.File(av, filename="avatar.png"))



def setup(bot):
    bot.add_cog(FunCMD(bot))