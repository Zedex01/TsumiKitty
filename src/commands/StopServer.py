""" Stop Server Command """
#Imports
import discord, logging, os, subprocess
from discord.ext import commands
from src.util.Config import Config
from src.util.Server import Server

#Setup
logger = logging.getLogger(__name__)


class StopServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()
        self.srv = Server()
               
    @commands.command(name="stop_server", description="Saves then stops the server.")
    @commands.is_owner()
    async def stopServer(self, ctx):
        logger.info(f"{ctx.author} requested server shutdown.")
    
        #Forces a world save
        logger.info(f"Saving world")
        await ctx.send(self.srv.sendCmd("save-all"))
        
        #Shuts down the server
        logger.info(f"Shutting down")
        await ctx.send(self.srv.sendCmd("stop"))

                   
async def setup(bot):
    await bot.add_cog(StopServer(bot))