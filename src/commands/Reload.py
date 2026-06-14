""" Reloads Tsumikitty Configs """
import discord, subprocess, os
from discord.ext import commands
import configparser as cp
from src.util.Config import Config

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()  

    @commands.command(name="reload", description="Reloads Tsumikitty's configuration files.")
    @commands.is_owner()
    async def reload(self, ctx, cog: str = None):
        
        # === Configs ===
        self.allow_reload = self.cfg.get_bool("Debug", "allow_reload")
        
        if self.allow_reload:
            
            print("Restarting...")
            await ctx.send("Reloading Configs")

            if cog:
                await self.bot.reload_extension(f"commands.{cog}")
                await ctx.send(f"Reloaded {cog}!")
            else:
                for ext in list(self.bot.extensions.keys()):
                    await self.bot.reload_extension(ext)
                await ctx.send("🔄 Reloaded all cogs!")
        

async def setup(bot):
    await bot.add_cog(Reload(bot))