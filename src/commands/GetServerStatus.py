""" Check Server Status Commads """
import discord, subprocess, logging
from discord.ext import commands
from src.util.Config import Config

logger = logging.getLogger(__name__)


class GetServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()
        
        
    @commands.command(name="server", description="Checks if the server is currently online.")
    @commands.guild_only()
    async def getServerStatus(self, ctx):
        logger.info(f"{ctx.author} requested server status")
        
        # === Configs ===
        self.server_name = self.cfg.get_str("Setup", "server_name")
        
        #Get Server data:
        cur_IP = subprocess.check_output("curl ifconfig.me", shell = True, universal_newlines=True)

        try:
            StatReturn = subprocess.check_output('tasklist | find "java"', shell=True, universal_newlines=True)
        except:
            StatReturn = ''
        
        if StatReturn == '':
            Status = "OFFLINE"
            color = discord.Color.red()

        else:
            Status = "ONLINE"
            color = discord.Color.green()

        embed = discord.Embed(title='Server Details', description=None, color=color)
        embed.add_field(name='Name', value=self.server_name, inline=True)
        embed.add_field(name='IP', value= cur_IP, inline=True)
        embed.add_field(name='Status', value= Status, inline=True)
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(GetServerStatus(bot))