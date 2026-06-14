""" Locate """
import discord, logging, re
from discord.ext import commands
from src.util.Linker import Linker
from src.util.Server import Server

logger = logging.getLogger(__name__)


villages = [
    "village_desert",
    "village_plains",
    "village_savanna",
    "village_snowy",
    "village_taiga"
]

portals = [
    "ruined_portal",
    "ruined_portal_desert",
    "ruined_portal_jungle",
    "ruined_portal_mountain",
    "ruined_portal_nether",
    "ruined_portal_ocean",
    "ruined_portal_swamp"
]

class LocateStructure(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.lnkr = Linker()
        self.srv = Server()
        
    @commands.command(name="locate_structure", description="locates a stucture nearest the player who runs the command")
    async def locate_structure(self, ctx, structure) -> None:

        #Set to lower case
        structure = structure.lower()
        
        if structure == "list":
            embed = discord.Embed(
                title=f"Structures:",
                color=discord.Color.purple()
            )
            structures = [
                "ancient_city",
                "bastion_remnant",
                "buried_treasure",
                "desert_pyramid",
                "end_city",
                "fortress",
                "igloo",
                "jungle_pyramid",
                "mansion",
                "mineshaft",
                "mineshaft_mesa",
                "monument",
                "nether_fossil",
                "ocean_ruin_cold",
                "ocean_ruin_warm",
                "pillager_outpost",
                "ruined_portal",
                "ruined_portal_desert",
                "ruined_portal_jungle",
                "ruined_portal_mountain",
                "ruined_portal_nether",
                "ruined_portal_ocean",
                "ruined_portal_swamp",
                "shipwreck",
                "shipwreck_beached",
                "stronghold",
                "swamp_hut",
                "trail_ruins",
                "village_desert",
                "village_plains",
                "village_savanna",
                "village_snowy",
                "village_taiga"
            ]
            
            structure_list = "\n".join(structures)
            
            
            embed.add_field(name="List: ",value=structure_list, inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
            return
        
        
        #Can be used on either self or another member of the discord
        player = ctx.author
        
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
        

        #If it is a generic request, enter special mode
        if (structure == "village") or (structure == "portal"):

            #For village
            if structure == "village":
                nearest_village = self._list_search(playerName, villages)

                if not nearest_village:
                    await ctx.send(f"No villages nearby :(")
                else:
                    await ctx.send(f"Nearest village found by {playerName} is at {nearest_village[0]}. ({nearest_village[1]} blocks away)")

                return

            elif structure == "portal":
                nearest_portal = self._list_search(playerName, portals)

                if not nearest_portal:
                    await ctx.send(f"There are no nearby ruined portals")
                
                else:
                    await ctx.send(f"Nearest portal found by {playerName} is at {nearest_portal[0]}. ({nearest_portal[1]} blocks away)")
                return

            
        #Send a request for players coords to the server
        recv = self.srv.sendCmd(f"execute as {playerName} at @s run locate structure minecraft:{structure}")
        
        if recv == "":
            recv = "None could be found nearby..."
        
        else:
            recv = recv.replace("minecraft:","")
              
        
        embed = discord.Embed(
            title=f"📍 **{structure.capitalize()}**",
             color=discord.Color.purple()
        )
        embed.add_field(name="Search Results: ",value=recv, inline=True)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        await ctx.send(embed=embed)
    

    #searches from a provided list of structures and returns the one that is closest
    def _list_search(self, playerName, list) -> list:
        #Clear list
        nearest_stuct = []
    
        #Itterate through each sturcture in the list
        for struct in list:

            #Send a command to the server using the player as starting point and one the currect structure
            recv = self.srv.sendCmd(f"execute as {playerName} at @s run locate structure minecraft:{struct}")
            
            #If a response is recived 
            if not recv == "":

                #Pattern for grabbing Coordinates and diistance
                pattern = r'(?P<COORD>\[-?\d+, ~, -?\d+\]) \((?P<DIST>\d+).*\)'

                #Apply the pattern to the server response and save each value
                try:
                    s = re.search(pattern, recv)
                    location = s.group('COORD')
                    distance = int(s.group('DIST'))
                except Exception as e:
                    print(e)
                    continue

                #If the list is not empty, check which is closer ot the player
                if nearest_stuct:
                    if nearest_stuct[1] > distance:
                        #if the new structure is closer, save it as the nearest structure
                        nearest_stuct[0] = location
                        nearest_stuct[1] = distance

                #If this is the first itteration and the list is empty, save this result
                else:
                    nearest_stuct.append(location) 
                    nearest_stuct.append(distance)
        
        #Return the nearest structure
        return nearest_stuct
        
        

async def setup(bot):
    await bot.add_cog(LocateStructure(bot))
        
            