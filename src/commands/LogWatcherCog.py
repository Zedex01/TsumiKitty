""" List Players Command - Lists the # of players on the server """

import discord, os, subprocess, logging, asyncio
from discord.ext import commands, tasks
from src.util.LogWatcher import LogWatcher

#Setup
logger = logging.getLogger(__name__)


class LogWatcherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watcher = LogWatcher(bot)
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        #start background task when bot is ready
        self.bot.loop.create_task(self.watcher.watch())
        
    async def cog_unload(self):
        #stop watcher when cog is unloaded
        self.watcher.stop()
        
async def setup(bot):
    await bot.add_cog(LogWatcherCog(bot))