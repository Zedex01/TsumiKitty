""" List Players Command
 - Lists the # of players on the server
"""
import discord, os, subprocess, logging
from discord.ext import commands
from src.util.Server import Server
from src.util.Config import Config

#Setup
logger = logging.getLogger(__name__)


class ListPlayers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()
        self.srv = Server()
               
    @commands.command(name="list", description="List the # of players currently on the server")
    async def stopServer(self, ctx):
        logger.info(f"{ctx.author} requested player list")
    
        if self.srv.isRunning():
            #Sends plaintext output of command as a normal message
            response = self.srv.sendCmd("list").splitlines()
            for player in response:
                pass
            
            await ctx.send(self.srv.sendCmd("list"))
        else:
            await ctx.send("Server currently offline, unable to process request")
                   
async def setup(bot):
    await bot.add_cog(ListPlayers(bot))