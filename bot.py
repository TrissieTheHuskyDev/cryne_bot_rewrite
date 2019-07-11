import discord
from discord.ext import commands

import sql

import os

import logging


def prefix(bot, message):
    if not message.guild:
        return "cb-"
    id = message.guild.id
    prefix_lst = sql.get_servers()
    prefix = prefix_lst[id][1]
    return prefix


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    bot = commands.Bot(command_prefix=prefix, max_messages=1000000000)

    token = os.environ['TOKEN']

    cog_dir = "cogs."
    base_cogs = ["cog_handler", "edit_settings", "events", "misc_commands", "misc_helper", "ban_guild", "logging", "moderation", "belv", "rss", "voice", "fun"]

    for cog in base_cogs:
        bot.load_extension(cog_dir + cog)

    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("Exiting")