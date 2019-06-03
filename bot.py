from discord.ext import commands

import sql
from sqlalchemy.exc import IntegrityError

import os

token = os.environ['TOKEN']

bot = commands.Bot("+")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            sql.create_server(guild.name, guild.id)
        except IntegrityError as e:
            print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))



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


def get_guilds(): #get the guilds the bot is connected to
    bot_guilds = []
    for guild in bot.guilds:
        bot_guilds.append((guild.name, guild.id))
    print(bot_guilds)
    return bot_guilds


if __name__ == "__main__":
    bot.run(token)