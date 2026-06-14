""" Retrieve Biome Coords """
import discord
from discord.ext import commands

class LocateBiome(commands.Cog, cfg: Config):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = cfg
               
    @commands.command(name="locate", description="Gets the coordinates of the nearest biome of specified type")
    async def getBiomeLocation(self, ctx):
        
        # === Configs ===   
        self.allow_locate_biomes = self.cfg.get_bool("Rules", "allow_locate_biomes")
           
        if not self.allow_locate_biomes:
            color = discord.Color.red()
            embed_name = "Notice:"
            embed_value = "Biome Locator is disabled on this server."
        else:
            color = discord.Color.green()
            embed_name = "XYZ:"
            embed_value = "0, 0, 0"
        
        embed = discord.Embed(title='Biome Locator', description=None, color=color)  
        embed.add_field(name=embed_name, value=embed_value, inline=False)
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(LocateBiome(bot))