""" Start Server Command """
import discord, logging, asyncio
from discord.ext import commands
from src.util.Config import Config
from src.util.Server import Server

import os, subprocess

logger = logging.getLogger(__name__)


class StartServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()
        self.srv = Server()
               
    @commands.command(name="start_server", description="Boots the server")
    async def startServer(self, ctx):
        logger.info(f"{ctx.author} requested server startup")
        
        #Get server run.bat file path
        self.start_path = self.cfg.get_str("Setup", "start_path")
        
        #Verify the path is valid
        if not os.path.isfile(self.start_path):
            logger.error(f"{self.start_path} does not exist!")
            raise FileNotFoundError(f"{self.start_path} does not exist!")
            
        try:
            await ctx.send("Starting server now, please be patient...")
            process = subprocess.Popen([self.start_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            if await self.srv.waitUntilRunning():
                logger.info("Server succesfuly started")
                await ctx.send("Server is now online!")
            else:
                logger.error("Server failed to start in time")
                await ctx.send("Server failed to start in time")
            

        except subprocess.CalledProcessError as e:
            logger.error(f"Error with run.bat: {e}")
            await ctx.send("Server start failed, check run.bat")
        
                   
async def setup(bot):
    await bot.add_cog(StartServer(bot))