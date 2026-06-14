""" List Players Command
 - Lists the # of players on the server
"""
import discord, os, subprocess, logging
from discord.ext import commands
from src.util.Server import Server
from src.util.Config import Config
from src.util.Linker import Linker

#Setup
logger = logging.getLogger(__name__)


class LinkAccount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lnkr = Linker()
               
    @commands.command(name="link", description="Link accounts")
    async def link(self, ctx, name):
        logger.info(f"{ctx.author} requested account link to: {name}")
        
        if self.lnkr.isLinked(ctx.author.id):
            await ctx.send(f"Your account is already linked to: \"{self.lnkr.getMinecraftName(ctx.author.id)}\"")
            self.lnkr.setMinecraftName(ctx.author.id, name)
            await ctx.send(f"Re-linked \"{name}\" to discord account.")
            logger.info(f"Re-linked \"{name}\" to discord account {ctx.author}:{ctx.author.id}")
        
        else:
            self.lnkr.setMinecraftName(ctx.author.id, name)
            await ctx.send(f"Linked \"{name}\" to discord account.")
            logger.info(f"Linked \"{name}\" to discord account {ctx.author}:{ctx.author.id}")
            

async def setup(bot):
    await bot.add_cog(LinkAccount(bot))