import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        cname = f"{str(member)}s Channel"


        if before.channel is not None:
            if before.channel.name == cname:
                await before.channel.delete()

    #TODO: Implement DB
        jchannel = self.bot.get_channel(575657057064189971)

        if after.channel is not None:
            for channel in after.channel.category.voice_channels:
                if channel.name == cname:
                    return

        if after.channel == jchannel:
            cchannel = await member.guild.create_voice_channel(cname, category=after.channel.category)

            perms = discord.PermissionOverwrite(connect=True, speak=True, use_voice_activation=True, deafen_members=True, mute_members=True, manage_channels=True, administrator=True)
            await cchannel.set_permissions(member, overwrite=perms)

            await member.move_to(cchannel)

def setup(bot):
    bot.add_cog(Voice(bot))