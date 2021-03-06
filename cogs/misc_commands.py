import discord
from discord.ext import commands

import sql

import os

import command_checks

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_ctx=True)
    async def info(self, ctx):
        '''Bot information'''
        paddi = self.bot.get_user(369129934917992450)
        tb = self.bot.get_user(583738641503879184)
        embed = discord.Embed(title="Info: cryne_bot",
                              url="https://github.com/itsCryne/cryne_bot_rewrite",
                              description="cryne_bot, programmed by " + paddi.mention, color=0xffb82b)
        embed.set_author(name="cryne_bot", url="https://github.com/itsCryne/cryne_bot_rewrite", icon_url=tb.avatar_url)
        embed.add_field(name="A (more or less) simple moderation bot",
                        value="Currently present on " + str(len(self.bot.guilds)) + " guilds with " + str(len(self.bot.users)) + " members")
        embed.set_footer(text=f"Programmed in discord.py {discord.__version__}")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(pass_ctx=True)
    async def register_users(self, ctx):
        for member in self.bot.users:
            sql.delete_user(member.id)

        for member in self.bot.users:
            sql.register_user(member.id, member.name)

    @commands.command(pass_ctx=True)
    async def get_mlogs(self, ctx):
        guild = ctx.guild.id

        msglist = sql.get_gmsgs(guild)

        with open(str(guild) + ".txt", "w") as logfile:
            for entry in msglist:
                logfile.writelines(entry)

        with open(str(guild) + ".txt", "r") as logfile:
            await ctx.author.send("Here is your message log:", file=discord.File(logfile, str(guild) + ".txt"))

        os.remove(str(guild) + ".txt")

    @commands.command(pass_ctx=True)
    async def f(self, ctx):
        await ctx.send("GH6Knc7")

    @command_checks.joinmsg_unset()
    @commands.command(pass_ctx=True)
    async def set_joinmsg(self, ctx, *, msg):
        sql.set_joinmsg(ctx.guild.id, msg)

    @command_checks.joinmsg_set()
    @commands.command(pass_ctx=True)
    async def edit_joinmsg(self, ctx, *, msg):
        sql.edit_joinmsg(ctx.guild.id, msg)


def setup(bot):
    bot.add_cog(Misc(bot))