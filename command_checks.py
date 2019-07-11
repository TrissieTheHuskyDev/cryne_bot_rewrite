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

def joinmsg_set():
    async def predicate(ctx):
        return sql.joinmsg_set(ctx.guild.id)
    return commands.check(predicate)

def joinmsg_unset():
    async def predicate(ctx):
        return sql.joinmsg_set(ctx.guild.id) == False
    return commands.check(predicate)

def muterole_created():
    async def predicate(ctx):
        return sql.get_muterole(ctx.guild.id) is not None

    return commands.check(predicate)