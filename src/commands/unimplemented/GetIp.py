""" Command For retriving IP """
import discord
from discord.ext import commands
import subprocess

class GetIp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ip", description="grabs the servers current IP address.")
    @commands.guild_only()
    async def getIp(self, ctx):
        
        server_ip = subprocess.check_output("ipconfig | findstr /i \"ipv4\"", shell=True, text=True).strip()
        
        embed = discord.Embed(
            title="Server IP",
            color=discord.Color.dark_blue()
            
        )
        embed.add_field(name = "IP: ", value=server_ip, inline=True)
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(GetIp(bot))