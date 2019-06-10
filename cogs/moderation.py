import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from command_checks import settings_created, in_pm

import datetime, time

import sql

class ModTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def kick(self, ctx, user : discord.User, *, reason=None):
        await ctx.guild.kick(user, reason)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def ban(self, ctx, user: discord.User, *, reason=None):
        await ctx.guild.ban(user, reason=reason)


    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def purge(self, ctx, count=1000000):
        await ctx.channel.purge(limit=int(count))
        await ctx.channel.send("Channel purged", delete_after=5)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def delete(self, ctx, count):
        counter = 0
        async for msg in ctx.channel.history(limit=int(count)):
            await msg.delete()
            counter += 1
        await ctx.channel.send(f"{counter} messages deleted!", delete_after=5)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def unban(self, ctx, user, *, reason=None):
        user, disc = user.split("#")

        banlist = await ctx.guild.bans()

        for entry in banlist:
            if entry[1].name == user and entry[1].discriminator == disc:
                duser = await self.bot.fetch_user(int(entry[1].id))
                await ctx.guild.unban(duser, reason=reason)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def warn(selfs, ctx, user: discord.Member, *, reason):
        now = datetime.datetime.now().timestamp()

        sql.warn(str(user), user.id, reason, now)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def get_warns(selfs, ctx, user: discord.Member):
        warnlist = sql.get_warns(user.id)

        embed = discord.Embed(title=f"Warns of {str(user)}", description=f"Total: {len(warnlist)}")
        embed.set_author(name=str(user), icon_url=user.avatar_url)

        for warn in warnlist:
            ltime = time.gmtime(warn[1])
            rtime = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            embed.add_field(name=f"{warn[0]} | ID: {warn[3]}", value=f"at {rtime} UTC", inline=False)

        await ctx.channel.send(embed=embed)


    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def del_warn(selfs, ctx, warnid):
        sql.del_warn(warnid)

    @in_pm()
    @commands.cooldown(1, 60, BucketType.user)
    @commands.command(pass_ctx=True)
    async def report(self, ctx, mlink):
        dsid = int(mlink.split("/")[4])

        if sql.settings_created(dsid) == False:
            return

        reportchid = sql.get_settings(dsid)["reportchid"]
        reportch = self.bot.get_channel(reportchid)

        embed = discord.Embed(
            title=f"{ctx.message.author} reported a message on this guild", url=mlink)
        embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

        await reportch.send(content="@nothere", embed=embed)

    @report.error
    async def report_error(self, ctx, error):
        await ctx.send("This command can only be used in DMs once per minute", delete_after=10)



def setup(bot):
    bot.add_cog(ModTools(bot))