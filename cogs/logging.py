import discord
from discord.ext import commands

import sql

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if sql.settings_created(int(before.guild.id)) != True:
            return

        logchid = sql.get_settings(before.guild.id)["logchid"]
        logch = self.bot.get_channel(logchid)

        embed = discord.Embed(title="Message edited", url = after.jump_url, description = f"A message in {after.channel.mention} was edited by {after.author.mention}", color = 0xfff500)
        embed.set_author(name=after.author, icon_url=after.author.avatar_url)
        embed.add_field(name="Before edit", value = before.content, inline = True)
        embed.add_field(name="After edit", value = after.content, inline = True)

        await logch.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if sql.settings_created(int(message.guild.id)) != True:
            return

        logchid = sql.get_settings(message.guild.id)["logchid"]
        logch = self.bot.get_channel(logchid)

        embed = discord.Embed(title="Message deleted", description = f"A message in {message.channel.mention} was deleted", color = 0xff0000)
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.add_field(name="Content", value = message.content, inline = True)

        await logch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if sql.settings_created(int(guild.id)) != True:
            return
        banmsgchid = sql.get_settings(guild.id)["banmsgchid"]
        banmsgch = self.bot.get_channel(banmsgchid)

        embed = discord.Embed(title="User banned",
                              description=f"{user.mention} was banned from this server", color=0xff0000)
        embed.set_author(name=user, icon_url=user.avatar_url)
        print("hammer")
        await banmsgch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild

        if sql.settings_created(int(guild.id)) != True:
            return
        kickmsgchid = sql.get_settings(guild.id)["kickmsgchid"]
        kickmsgch = self.bot.get_channel(kickmsgchid)

        leavemsgchid = sql.get_settings(guild.id)["kickmsgchid"]
        leavemsgch = self.bot.get_channel(leavemsgchid)

        als = guild.audit_logs(limit=1)
        async for entry in als:
            if entry.action == discord.AuditLogAction.kick:
                if entry.target == member:

                    embed = discord.Embed(title="User was kicked",
                                      description=f"{member.mention} was kicked from this server", color=0xff9000)
                    embed.set_author(name=member, icon_url=member.avatar_url)

                    await kickmsgch.send(embed=embed)

                else:
                    embed = discord.Embed(title="User left",
                                          description=f"{member.mention} left from this server", color=0xfff500)
                    embed.set_author(name=member, icon_url=member.avatar_url)

                    await leavemsgch.send(embed=embed)
            else:
                embed = discord.Embed(title="User left",
                                      description=f"{member.mention} left from this server", color=0xfff500)
                embed.set_author(name=member, icon_url=member.avatar_url)

                await leavemsgch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = before.guild

        if sql.settings_created(int(guild.id)) != True:
            return
        rcmsgchid = sql.get_settings(guild.id)["rcmsgchid"]
        rcmsgch = self.bot.get_channel(rcmsgchid)

        if before.roles != after.roles:
            before_roles = [y.name.lower() for y in before.roles]
            after_roles = [y.name.lower() for y in after.roles]

            removed_roles = [elem for elem in before_roles if elem not in after_roles]
            added_roles = [elem for elem in after_roles if elem not in before_roles]

            if len(removed_roles) == 0:
                embed = discord.Embed(title="Role was added",
                                      description=f"{after.mention} received role {added_roles[0]}", color=0x006400)
                embed.set_author(name=after, icon_url=after.avatar_url)

                await rcmsgch.send(embed=embed)

            elif len(added_roles) == 0:
                embed = discord.Embed(title="Role was removed",
                                      description=f"{after.mention} lost role {removed_roles[0]}", color=0xfff500)
                embed.set_author(name=after, icon_url=after.avatar_url)

                await rcmsgch.send(embed=embed)


        if before.nick != after.nick:
            embed = discord.Embed(title="Nickname changed",
                                  description=f"{after.mention} changed their nick",
                                  color=0x006400)
            embed.set_author(name=after, icon_url=after.avatar_url)
            embed.add_field(name="Old nick", value=before.nick, inline=True)
            embed.add_field(name="New nick", value=after.nick, inline=True)

            await rcmsgch.send(embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))