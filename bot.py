from discord.ext import commands
import discord

import sql
from sqlalchemy.exc import IntegrityError

import os
import datetime

token = os.environ['TOKEN']

def prefix(bot, message):
    if not message.guild:
        return "cb-"
    id = message.guild.id
    prefix_lst = sql.get_servers()
    prefix = prefix_lst[id][1]
    return prefix

bot = commands.Bot(command_prefix=prefix)

bot.load_extension("cogs.edit_settings")
bot.load_extension("cogs.misc_commands")
bot.load_extension("cogs.cog_handler")

@bot.event
async def on_message(message):
    now = datetime.datetime.now().timestamp()

    if len(message.mentions) > 0:
        if message.mentions[0] == bot.user:
            await message.channel.send("The prefix for this server currently is: " + str(sql.get_servers()[message.guild.id][1]))

    sql.log_msg(message.id, message.guild.id, message.channel.id, now, message.content, message.author.id)

    await bot.process_commands(message)


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