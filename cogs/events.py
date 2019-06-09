import discord
from discord.ext import commands
import datetime
import sql
from sqlalchemy.exc import IntegrityError

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.datetime.now().timestamp()

        if len(message.mentions) > 0:
            if message.mentions[0] == self.bot.user:
                await message.channel.send(
                    "The prefix for this server currently is: " + str(sql.get_servers()[message.guild.id][1]))

        sql.log_msg(message.id, message.guild.id, message.channel.id, now, message.content, message.author.id)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            try:
                sql.create_server(guild.name, guild.id, "cb-")
            except IntegrityError as e:
                print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            sql.create_server(guild.name, guild.id, "cb-")
        except IntegrityError as e:
            print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))
            
def setup(bot):
    bot.add_cog(Events(bot))
