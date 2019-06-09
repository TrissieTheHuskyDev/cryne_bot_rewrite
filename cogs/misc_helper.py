import discord
from discord.ext import commands

class MiscHelper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_guilds(self):  # get the guilds the bot is connected to
        bot_guilds = []
        for guild in self.bot.guilds:
            bot_guilds.append((guild.name, guild.id))
        print(bot_guilds)
        return bot_guilds

    def in_guild(self, gid):
        guilds = self.get_guilds()

        for tup in guilds:
            for elem in tup:
                if gid == elem:
                    return True
        return False

def setup(bot):
    bot.add_cog(MiscHelper(bot))