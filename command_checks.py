import discord
from discord.ext import commands

import sql


# def is_owner(self):
# async def predicate(ctx):
#     return ctx.author.id == 123456789
# return commands.check(predicate)

def settings_created():
    async def predicate(ctx):
        return sql.settings_created(ctx.guild.id)
    return commands.check(predicate)

def in_pm():
    async def predicate(ctx):
        return isinstance(ctx.channel, discord.DMChannel)
    return commands.check(predicate)
