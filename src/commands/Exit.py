""" Exit Tsumikitty """
import discord, subprocess, os
from discord.ext import commands
from src.util.Config import Config

class Exit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()
                
    @commands.command(name="exit", description="Shuts down Tsumikitty.")
    @commands.is_owner()
    async def exit(self, ctx):
        # === Config ===
        self.allow_exit = self.cfg.get_bool("Debug", "allow_exit")
        
        if self.allow_exit:
            print("Shutting Down")
            await ctx.send("Goodbye!")
            await self.bot.close()
        

async def setup(bot):
    await bot.add_cog(Exit(bot))