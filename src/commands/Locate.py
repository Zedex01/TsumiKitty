""" Locate """
import discord, logging, re
from discord.ext import commands
from src.util.Linker import Linker
from src.util.Server import Server

logger = logging.getLogger(__name__)

class Locate(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.lnkr = Linker()
        self.srv = Server()
        
    @commands.command(name="locate", description="locates a player in world")
    @commands.guild_only()
    async def Locate(self, ctx, member: discord.Member = None) -> None:
        
        #Can be used on either self or another member of the discord
        player = member or ctx.author
        
        #Get the players ID from the json file
        playerName = self.lnkr.getMinecraftName(player.id)
        
        #Catch if it is not a linked account
        if playerName == None:
            await ctx.send(f"{player.display_name}'s account is not linked.")
            return
     
            
        #check if player is online:
        if not self.srv.playerOnline(playerName):
            await ctx.send(f"Currently {player.display_name} is not online.")
            return
            
        
        #Send a request for players coords to the server
        recv = self.srv.sendCmd(f"data get entity {playerName} Pos")
        recv = re.findall(r"(-?\d+\.\d+)", recv)
        coords = []
        for value in recv:
            coords.append(f"{float(value):.1f}")       
        
        coords_formatted = ", ".join(coords)
        
        embed = discord.Embed(
            title=f"📍 **{playerName}**",
             color=discord.Color.blue()
        )
        embed.add_field(name="Coordinates: ",value=coords_formatted, inline=True)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Locate(bot))
        
            