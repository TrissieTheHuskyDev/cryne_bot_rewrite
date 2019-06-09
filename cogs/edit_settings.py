import discord
from discord.ext import commands

import sql

from command_checks import settings_created

class Edit(commands.Cog):

    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_prefix(self, ctx, prefix):
        print(prefix)
        sid = ctx.guild.id
        sql.edit_prefix(sid, prefix)
        await ctx.channel.send("Prefix changed to `{}`".format(prefix))

    @edit_prefix.error
    async def prefix_error(self, ctx, error):
        print(error)
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def createsettings(self, ctx, logchid, botcchid, remoj, rcount, belvchid, banmsgchid, leavemsgchid, kickmsgchid,
                             rcmsgchid, adminrole, roleonjoin, rssurl, rsschannelid):
        valid_channels = []
        ch_ids = [logchid, botcchid, belvchid, banmsgchid, leavemsgchid, kickmsgchid, rcmsgchid, rsschannelid]

        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))

        for channel in ch_ids:
            if int(channel) not in valid_channels:
                raise ValueError

        sql.create_ssettings(ctx.guild.id, logchid, botcchid, remoj, rcount, belvchid, banmsgchid, leavemsgchid,
                             kickmsgchid, rcmsgchid, adminrole, roleonjoin, rssurl, rsschannelid)

    @createsettings.error
    async def createsettings_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You dont have the permissons to create server settings!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("A required argument is missing!")
        if "TypeError" in str(error):
            await ctx.send("One of the arguments has got the wrong type (mixed up arguments?)")
        if "ValueError" in str(error):
            await ctx.send("One of the channel IDs are invalid or the bot cant see the channel")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_logchid(self, ctx, logchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(logchid) not in valid_channels:
            raise ValueError
        sql.edit_logchid(sid, logchid)

    @edit_logchid.error
    async def logchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_botcchid(self, ctx, botcchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(botcchid) not in valid_channels:
            raise ValueError
        sql.edit_botcchid(sid, botcchid)

    @edit_botcchid.error
    async def botcchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_remoj(self, ctx, remoj):
        sid = ctx.guild.id
        sql.edit_remoj(sid, remoj)

    @edit_remoj.error
    async def remoj_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_rcount(self, ctx, rcount):
        sid = ctx.guild.id
        sql.edit_rcount(sid, rcount)

    @edit_rcount.error
    async def rcount_error(self, ctx, error):
        print(error)
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_belvchid(self, ctx, belvchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(belvchid) not in valid_channels:
            raise ValueError
        sql.edit_belvchid(sid, belvchid)

    @edit_belvchid.error
    async def belvchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_banmsgchid(self, ctx, banmsgchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(banmsgchid) not in valid_channels:
            raise ValueError
        sql.edit_banmsgchid(sid, banmsgchid)

    @edit_banmsgchid.error
    async def banmsgchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_leavemsgchid(self, ctx, leavemsgchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(leavemsgchid) not in valid_channels:
            raise ValueError
        sql.edit_leavemsgchid(sid, leavemsgchid)

    @edit_leavemsgchid.error
    async def leavemsgchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_kickmsgchid(self, ctx, kickmsgchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(kickmsgchid) not in valid_channels:
            raise ValueError
        sql.edit_kickmsgchid(sid, kickmsgchid)

    @edit_kickmsgchid.error
    async def kickmsgchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_rcmsgchid(self, ctx, rcmsgchid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(rcmsgchid) not in valid_channels:
            raise ValueError
        sql.edit_rcmsgchid(sid, rcmsgchid)

    @edit_rcmsgchid.error
    async def rcmsgchid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_adminrole(self, ctx, adminrole):
        sid = ctx.guild.id
        sql.edit_adminrole(sid, adminrole)

    @edit_adminrole.error
    async def adminrole_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_roleonjoin(self, ctx, roleonjoin):
        sid = ctx.guild.id
        sql.edit_roleonjoin(sid, roleonjoin)

    @edit_roleonjoin.error
    async def roleonjoin_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_rssurl(self, ctx, rssurl):
        sid = ctx.guild.id
        sql.edit_rssurl(sid, rssurl)

    @edit_rssurl.error
    async def rssurl_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")

    @settings_created()
    @commands.guild_only()
    @commands.command(pass_ctx=True)
    @commands.has_permissions(administrator=True)
    async def edit_rsschannelid(self, ctx, rsschannelid):
        sid = ctx.guild.id
        valid_channels = []
        for channel in ctx.guild.channels:
            valid_channels.append(int(channel.id))
        if int(rsschannelid) not in valid_channels:
            raise ValueError
        sql.edit_rsschannelid(sid, rsschannelid)

    @edit_rsschannelid.error
    async def rsschannelid_error(self, ctx, error):
        await ctx.send("An error occured whilst editing this setting! Check your command")


def setup(bot):
    bot.add_cog(Edit())