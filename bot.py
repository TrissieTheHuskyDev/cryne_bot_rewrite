import discord
from discord.ext import commands
from discord.utils import get
from discord import opus

from sql import create_server, create_ssettings, get_servers
from sqlalchemy.exc import IntegrityError

import os

token = os.environ['TOKEN']

bot = commands.Bot("#")
bot.remove_command("help")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            create_server(guild.name, guild.id)
        except IntegrityError as e:
            print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))



@bot.event
async def on_command_error(ctx):
    pass



def get_guilds(): #get the guilds the bot is connected to
    bot_guilds = []
    for guild in bot.guilds:
        bot_guilds.append((guild.name, guild.id))
    print(bot_guilds)
    return bot_guilds

bot.run(token)

