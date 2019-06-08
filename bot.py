from discord.ext import commands
import discord

import sql
from sqlalchemy.exc import IntegrityError

import os

token = os.environ['TOKEN']

def prefix(bot, message):
    id = message.guild.id
    prefix_lst = sql.get_servers()
    prefix = prefix_lst[id][1]
    return prefix

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            sql.create_server(guild.name, guild.id, "cb-")
        except IntegrityError as e:
            print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))

@bot.event
async def on_guild_join(guild):
    try:
        sql.create_server(guild.name, guild.id, "cb-")
    except IntegrityError as e:
        print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_prefix(ctx, prefix):
    print(prefix)
    sid = ctx.guild.id
    sql.edit_prefix(sid, prefix)
    await ctx.channel.send("Prefix changed to `{}`".format(prefix))


@edit_prefix.error
async def prefix_error(ctx, error):
    print(error)
    await ctx.send("An error occured whilst editing this setting! Check your command")

@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def createsettings(ctx, logchid, botcchid, remoj, rcount, belvchid, banmsgchid, leavemsgchid, kickmsgchid, rcmsgchid, adminrole, roleonjoin, rssurl, rsschannelid):
    valid_channels = []
    ch_ids = [logchid, botcchid, belvchid, banmsgchid, leavemsgchid, kickmsgchid, rcmsgchid, rsschannelid]

    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))

    for channel in ch_ids:
        if int(channel) not in valid_channels:
            raise ValueError

    sql.create_ssettings(ctx.guild.id, logchid, botcchid, remoj, rcount, belvchid, banmsgchid, leavemsgchid, kickmsgchid, rcmsgchid, adminrole, roleonjoin, rssurl, rsschannelid)

@createsettings.error
async def createsettings_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the permissons to create server settings!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A required argument is missing!")
    if "TypeError" in str(error):
        await ctx.send("One of the arguments has got the wrong type (mixed up arguments?)")
    if "ValueError" in str(error):
        await ctx.send("One of the channel IDs are invalid or the bot cant see the channel")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_logchid(ctx, logchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(logchid) not in valid_channels:
        raise ValueError
    sql.edit_logchid(sid, logchid)

@edit_logchid.error
async def logchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_botcchid(ctx, botcchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(botcchid) not in valid_channels:
        raise ValueError
    sql.edit_botcchid(sid, botcchid)

@edit_botcchid.error
async def botcchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_remoj(ctx, remoj):
    sid = ctx.guild.id
    sql.edit_remoj(sid, remoj)

@edit_remoj.error
async def remoj_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_rcount(ctx, rcount):
    sid = ctx.guild.id
    sql.edit_rcount(sid, rcount)


@edit_rcount.error
async def rcount_error(ctx, error):
    print(error)
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_belvchid(ctx, belvchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(belvchid) not in valid_channels:
        raise ValueError
    sql.edit_belvchid(sid, belvchid)


@edit_belvchid.error
async def belvchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_banmsgchid(ctx, banmsgchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(banmsgchid) not in valid_channels:
        raise ValueError
    sql.edit_banmsgchid(sid, banmsgchid)


@edit_banmsgchid.error
async def banmsgchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_leavemsgchid(ctx, leavemsgchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(leavemsgchid) not in valid_channels:
        raise ValueError
    sql.edit_leavemsgchid(sid, leavemsgchid)


@edit_leavemsgchid.error
async def leavemsgchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_kickmsgchid(ctx, kickmsgchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(kickmsgchid) not in valid_channels:
        raise ValueError
    sql.edit_kickmsgchid(sid, kickmsgchid)


@edit_kickmsgchid.error
async def kickmsgchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_rcmsgchid(ctx, rcmsgchid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(rcmsgchid) not in valid_channels:
        raise ValueError
    sql.edit_rcmsgchid(sid, rcmsgchid)


@edit_rcmsgchid.error
async def rcmsgchid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_adminrole(ctx, adminrole):
    sid = ctx.guild.id
    sql.edit_adminrole(sid, adminrole)


@edit_adminrole.error
async def adminrole_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_roleonjoin(ctx, roleonjoin):
    sid = ctx.guild.id
    sql.edit_roleonjoin(sid, roleonjoin)


@edit_roleonjoin.error
async def roleonjoin_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_rssurl(ctx, rssurl):
    sid = ctx.guild.id
    sql.edit_rssurl(sid, rssurl)


@edit_rssurl.error
async def rssurl_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
@commands.has_permissions(administrator=True)
async def edit_rsschannelid(ctx, rsschannelid):
    sid = ctx.guild.id
    valid_channels = []
    for channel in ctx.guild.channels:
        valid_channels.append(int(channel.id))
    if int(rsschannelid) not in valid_channels:
        raise ValueError
    sql.edit_rsschannelid(sid, rsschannelid)


@edit_rsschannelid.error
async def rsschannelid_error(ctx, error):
    await ctx.send("An error occured whilst editing this setting! Check your command")


@bot.command(pass_ctx=True)
async def info(ctx):
    paddi = bot.get_user(369129934917992450)
    tb = bot.get_user(583738641503879184)
    embed = discord.Embed(title="Info: cryne_bot",
                          url="https://github.com/itsCryne/cryne_bot_rewrite/blob/master/README.md", description = "cryne_bot, programmed by " + paddi.mention, color=0xffb82b)
    embed.set_author(name="cryne_bot", url="https://github.com/itsCryne/cryne_bot_rewrite", icon_url = tb.avatar_url)
    embed.set_footer(text="Licensed under CC BY-NC-SA 4.0")
    embed.add_field(name="A simple moderation bot", value="Currently present on " + str(len(bot.guilds)) + " guilds")
    await ctx.send(embed=embed)



def get_guilds(): #get the guilds the bot is connected to
    bot_guilds = []
    for guild in bot.guilds:
        bot_guilds.append((guild.name, guild.id))
    print(bot_guilds)
    return bot_guilds

def in_guild(gid):
    guilds = get_guilds()

    for tup in guilds:
        for elem in tup:
            if gid == elem:
                return True
    return False



if __name__ == "__main__":
    bot.run(token)