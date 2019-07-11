import datetime
import time

import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType

import sql
from command_checks import settings_created, in_pm, muterole_created


class ModTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.untempban.start()
        self.untempmute.start()

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
    async def warn(self, ctx, user: discord.Member, *, reason):
        now = datetime.datetime.now().timestamp()

        sql.warn(str(user), user.id, reason, now, ctx.guild.id)

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def get_warns(selfs, ctx, user: discord.Member):
        warnlist = sql.get_warns(user.id, ctx.guild.id)

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
        sql.del_warn(warnid, ctx.guild.id)

    @in_pm()
    @commands.cooldown(1, 60, BucketType.user)
    @commands.command(pass_ctx=True)
    async def report(self, ctx, mlink):
        dsid = int(mlink.split("/")[4])

        if not sql.settings_created(dsid):
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

    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def tempban(self, ctx, member: discord.Member, d : int, h : int, m : int, s : int, *, reason=None):
        user = await self.bot.fetch_user(member.id)


        now = datetime.datetime.now().timestamp()
        conv_d = d * 86400
        conv_h = h * 3600
        conv_m = m * 60
        conv_s = s

        tend = now + conv_d + conv_h + conv_m + conv_s

        sql.tban(user.id, user.name, tend, ctx.guild.id)

        await user.send(f"You have been temporarily ({d} days, {h} hours, {m} Minutes, {s}, seconds) banned from {ctx.guild.name} for the reason \"{reason}\"!")
        await ctx.guild.ban(user, reason=reason)


    @tasks.loop(seconds=10)
    async def untempban(self):
        tbans = sql.get_tbans()
        now = datetime.datetime.now().timestamp()

        if tbans is None:
            return

        for elem in tbans:
            if elem[2] < now:
                user = self.bot.get_user(elem[0])
                guild = self.bot.get_guild(elem[3])

                sql.utban(elem[0], elem[3])
                await guild.unban(user, reason="Auto unban (Tempban)")

    @muterole_created()
    @settings_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def tempmute(self, ctx, member: discord.Member, d : int, h : int, m : int, s : int, *, reason=None):
        user = self.bot.get_user(member.id)


        now = datetime.datetime.now().timestamp()
        conv_d = d * 86400
        conv_h = h * 3600
        conv_m = m * 60
        conv_s = s

        tend = now + conv_d + conv_h + conv_m + conv_s

        sql.tmute(user.id, user.name, tend, ctx.guild.id)

        await user.send(f"You have been temporarily ({d} days, {h} hours, {m} Minutes, {s}, seconds) muted in {ctx.guild.name} for the reason \"{reason}\"!")

        muteroleid = sql.get_muterole(ctx.guild.id)
        muterole = ctx.guild.get_role(muteroleid)

        await member.add_roles(muterole)

    @tasks.loop(seconds=10)
    async def untempmute(self):

        await self.bot.wait_until_ready()

        tmutes = sql.get_tmutes()
        now = datetime.datetime.now().timestamp()

        if tmutes is None:
            return

        for elem in tmutes:
            print(elem)
            if elem[2] < now:
                guildid = elem[3]
                guild = self.bot.get_guild(guildid)

                userid = elem[0]
                member = guild.get_member(userid)

                muteroleid = sql.get_muterole(guildid)
                muterole = guild.get_role(muteroleid)

                await member.remove_roles(muterole)

                sql.utmute(elem[0], elem[3])


    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def create_muterole(self, ctx):
        color = discord.Color.darker_grey()
        muterole = await ctx.guild.create_role(name="Muted", colour=color, reason="cryne_bot Mute")

        overwrite = discord.PermissionOverwrite(add_reactions=False, send_messages=False)
        voice_overwrite = discord.PermissionOverwrite(speak=False)

        sql.create_mrole(ctx.guild.id, muterole.id)

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(muterole, overwrite=overwrite)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(muterole, overwrite=voice_overwrite)

        if sql.get_tmutes() is not None:
            for mute in sql.get_tmutes():
                now = datetime.datetime.now().timestamp()
                if mute[3] == ctx.guild.id:
                    if mute[2] > now:
                        userid = mute[0]
                        member = ctx.guild.get_member(userid)

                        await member.add_roles(muterole, reason="Auto remute at role creation")


    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def delete_muterole(self, ctx):
        muteroleid = sql.get_muterole(ctx.guild.id)
        print(muteroleid)
        muterole = ctx.guild.get_role(muteroleid)

        await muterole.delete(reason="cryne_bot Mute")

        sql.delete_muterole(ctx.guild.id)


    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def recreate_muterole(self, ctx):
        muteroleid = sql.get_muterole(ctx.guild.id)
        muterole = ctx.guild.get_role(muteroleid)

        print(muterole)
        print(muteroleid)

        sql.delete_muterole(ctx.guild.id)

        await muterole.delete(reason="cryne_bot Mute")


        color = discord.Color.darker_grey()
        muterole = await ctx.guild.create_role(name="Muted", colour=color, reason="cryne_bot Mute")

        sql.create_mrole(ctx.guild.id, muterole.id)

        overwrite = discord.PermissionOverwrite(add_reactions=False, send_messages=False)
        voice_overwrite = discord.PermissionOverwrite(speak=False)

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(muterole, overwrite=overwrite)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(muterole, overwrite=voice_overwrite)

        if sql.get_tmutes() is not None:
            for mute in sql.get_tmutes():
                now = datetime.datetime.now().timestamp()
                if mute[3] == ctx.guild.id:
                    if mute[2] > now:
                        userid = mute[0]
                        member = ctx.guild.get_member(userid)

                        await member.add_roles(muterole, reason="Auto remute at role creation")


    @muterole_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def mute(self, ctx, member : discord.Member):
        muteroleid = sql.get_muterole(ctx.guild.id)
        muterole = ctx.guild.get_role(muteroleid)
        await member.add_roles(muterole)


    @muterole_created()
    @commands.has_permissions(administrator=True)
    @commands.command(pass_ctx=True)
    async def unmute(self, ctx, member : discord.Member):

        muteroleid = sql.get_muterole(ctx.guild.id)
        muterole = ctx.guild.get_role(muteroleid)

        await member.remove_roles(muterole)

    def cog_unload(self):
        self.untempban.stop()
        self.untempmute.stop()


def setup(bot):
    bot.add_cog(ModTools(bot))