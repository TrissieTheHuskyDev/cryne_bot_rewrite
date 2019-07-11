import discord
from discord.ext import commands
import datetime
import sql
from sqlalchemy.exc import IntegrityError
from discord.utils import get

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.datetime.now().timestamp()

        if len(message.mentions) > 0:
            if message.mentions[0] == self.bot.user:
                await message.channel.send("The prefix for this server currently is: " + str(sql.get_servers()[message.guild.id][1]))

        if not isinstance(message.channel, discord.DMChannel):
            if message.content == "":
                sql.log_msg(message.id, message.guild.id, message.channel.id, now, "<EMBED>", message.author.id, str(message.author))
            else:
                sql.log_msg(message.id, message.guild.id, message.channel.id, now, message.content, message.author.id, str(message.author))

    @commands.Cog.listener()
    async def on_ready(self):
        print("cryne_bot is ready for disaster")

        rpstr = f"on {len(self.bot.guilds)} guilds"
        await self.bot.change_presence(activity=discord.Game(name=rpstr))

        for guild in self.bot.guilds:
            try:
                sql.create_server(guild.name, guild.id, "cb-")
            except IntegrityError as e:
                print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))

        for member in self.bot.users:
            sql.delete_user(member.id)

        for member in self.bot.users:
            sql.register_user(member.id, member.name)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        rpstr = f"on {len(self.bot.guilds)} guilds"
        await self.bot.change_presence(activity=discord.Game(name=rpstr))

        if sql.guild_is_banned(guild.id):
            await guild.leave()
            return

        await guild.owner.send(f"It seems like you or something from your team has invited me to your Server `{guild.name}` Use `cb-createsettings` to configure me - then I'll be ready!")

        try:
            sql.create_server(guild.name, guild.id, "cb-")
        except IntegrityError as e:
            print("WARN: IntegrityError! Konnte Server {} | {} nicht erstellen!".format(guild.name, guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        rpstr = f"on {len(self.bot.guilds)} guilds"
        await self.bot.change_presence(activity=discord.Game(name=rpstr))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        set = sql.get_settings(member.guild.id)
        jr_name = set["roleonjoin"]

        jr = get(member.guild.roles, name=jr_name)

        await member.add_roles(jr)

        if sql.joinmsg_set(member.guild.id):

            mention = member.mention
            name = member.name
            guild = member.guild.name

            joinmsg = sql.get_joinmsg(member.guild.id)
            await member.send(joinmsg.format(name=name, mention=mention, guild=guild))

        else:
            await member.send("Welcome to {}".format(member.guild.name))



def setup(bot):
    bot.add_cog(Events(bot))
