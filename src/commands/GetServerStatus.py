""" Check Server Status Commads """
import discord, subprocess, logging, platform
from discord.ext import commands
from src.util.Config import Config
from src.util.Server import Server

logger = logging.getLogger(__name__)


class GetServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = Config()
        self.srv = Server()
        
    @commands.command(name="server", description="Checks if the server is currently online.")
    @commands.guild_only()
    async def getServerStatus(self, ctx):

        logger.info(f"{ctx.author} requested server status")
        
        # === Configs ===
        self.server_name = self.cfg.get_str("Setup", "server_name")
        
        #Get server IP from curl
        cur_IP = subprocess.check_output("curl ifconfig.me", shell = True, universal_newlines=True)

        #Check if the server is online!
        is_online = self.srv.isRunning()

        if not is_online:
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