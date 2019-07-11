import discord
from discord.ext import commands, tasks

import feedparser

import re

import time, datetime

import sql

class RSS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.rss.start()

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    @tasks.loop(minutes=30)
    async def rss(self):
        await self.bot.wait_until_ready()
        servers = sql.get_servers()
        sids = list(servers.keys())

        for sid in sids:
            settings = sql.get_settings(sid)

            if settings is None:
                continue


            chid = settings["rsschid"]
            feed_url = settings["rssurl"]


            rfeed = feedparser.parse(feed_url)

            now = datetime.datetime.now().timestamp()
            pub_time = time.mktime(rfeed.entries[0].published_parsed)
            tolc = now - 1800

            if pub_time < tolc:
                continue
            if not rfeed.entries:
                continue

            title = rfeed.entries[0].title
            url = rfeed.entries[0].link

            channel = self.bot.get_channel(chid)

            await channel.send(f":newspaper: | **{title}**")
            await channel.send(url)

        def cog_unload():
            self.rss.stop()


def setup(bot):
    bot.add_cog(RSS(bot))