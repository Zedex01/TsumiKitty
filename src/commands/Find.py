""" find """
import discord, logging, re
from discord.ext import commands
from src.util.Linker import Linker
from src.util.Server import Server

logger = logging.getLogger(__name__)


struct_list = [
    "minecraft:ancient_city", 
    "minecraft:bastion_remnant", 
    "minecraft:buried_treasure", 
    "minecraft:desert_pyramid", 
    "minecraft:end_city", 
    "minecraft:fortress", 
    "minecraft:igloo", 
    "minecraft:jungle_pyramid", 
    "minecraft:mansion", 
    "minecraft:mineshaft", 
    "minecraft:mineshaft_mesa", 
    "minecraft:monument", 
    "minecraft:nether_fossil", 
    "minecraft:ocean_ruin_cold", 
    "minecraft:ocean_ruin_warm", 
    "minecraft:pillager_outpost", 
    "minecraft:ruined_portal", 
    "minecraft:ruined_portal_desert", 
    "minecraft:ruined_portal_jungle", 
    "minecraft:ruined_portal_mountain", 
    "minecraft:ruined_portal_nether", 
    "minecraft:ruined_portal_ocean", 
    "minecraft:ruined_portal_swamp", 
    "minecraft:shipwreck", 
    "minecraft:shipwreck_beached", 
    "minecraft:stronghold", 
    "minecraft:swamp_hut", 
    "minecraft:trail_ruins", 
    "minecraft:village_desert", 
    "minecraft:village_plains", 
    "minecraft:village_savanna", 
    "minecraft:village_snowy", 
    "minecraft:village_taiga"
    
    
]

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

class Find(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.lnkr = Linker()
        self.srv = Server()
        
    @commands.command(name="find", description="finds players, structures, & biomes (coming soon)")
    @commands.guild_only()

    async def Find(self, ctx, arg1: str = None) -> None:

        # === Player Locator ===
        #If there is no arguments OR arg1 is a discord memeber:
        if arg1 is None or await self._is_member(ctx, arg1):
            #If there is an arg1, set as target_player
            if not arg1 is None:
                player = await commands.MemberConverter().convert(ctx, arg1)
           
            #Use Author as target
            else:
                player = ctx.author

            await self._find_player(ctx, player)  

        # === Structure Locator ===
        #checks if input has identifier

        if ":" not in arg1:
            #prepend if not there
            arg1 = "minecraft:" + arg1

        #Check if it is in structure list
        if arg1 in struct_list or arg1 == "minecraft:village" or arg1 == "minecraft:portal":
            await self._find_structure(ctx, arg1)
            return
            
        else:
            await ctx.send(f"\"{arg1}\" is not a vaild argument.")
            return                



    async def _is_member(self, ctx, arg: str) -> bool:
        #Check if an argument is a member
        try:
            await commands.MemberConverter().convert(ctx, arg)
            return True
        except commands.MemberNotFound:
            return False
        

    async def _find_player(self, ctx, target_player):
        print("Finding Player: ", target_player)
        
        #Get the Members in game name
        player_name = self.lnkr.getMinecraftName(target_player.id)

        if not player_name == None: #If player is linked
            if self.srv.isRunning(): #if Server is running 
                if self.srv.playerOnline(player_name): #if player is online
                    #Send a request for players coords to the server
                    recv = self.srv.sendCmd(f"data get entity {player_name} Pos")
                    recv = re.findall(r"(-?\d+\.\d+)", recv)
                    coords = []
                    for value in recv:
                        coords.append(f"{float(value):.1f}")       
                    coords_formatted = ", ".join(coords)
                    embed = discord.Embed(title=f"📍 **{player_name}**", color=discord.Color.blue())
                    embed.add_field(name="Coordinates: ",value=coords_formatted, inline=True)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    await ctx.send(embed=embed)
                    return
                else:
                    await ctx.send(f"Currently {target_player.display_name} is not online.")  
                    return
            else:
                await ctx.send(f"Currently server is not online.")
                return
        else:
            await ctx.send(f"{target_player.display_name}'s account is not linked.")
            return

    async def _find_structure(self, ctx, arg):

        #Set player and get in game name
        player = ctx.author
        player_name = self.lnkr.getMinecraftName(player.id)
        
        #Check if player's account is linked
        if not player_name == None:
            if self.srv.isRunning():
                if self.srv.playerOnline(player_name):
                    print("ARG: ", arg)
                    
                    if arg == "minecraft:village" or arg == "minecraft:portal":
                        print("Is portal or village!")
                        if arg == "minecraft:village":
                            nearest_village = self._list_search(player_name, villages)

                            if not nearest_village:
                                await ctx.send(f"No villages nearby :(")
                            else:
                                await ctx.send(f"Nearest village found by {player_name} is at {nearest_village[0]}. ({nearest_village[1]} blocks away)")
                            return

                        elif arg == "minecraft:portal":
                            nearest_portal = self._list_search(player_name, portals)

                            if not nearest_portal:
                                await ctx.send(f"There are no nearby ruined portals")

                            else:
                                await ctx.send(f"Nearest portal found by {player_name} is at {nearest_portal[0]}. ({nearest_portal[1]} blocks away)")
                            return

                    else:
                        #Send a request for players coords to the server
                        recv = self.srv.sendCmd(f"execute as {player_name} at @s run locate structure {arg}")
                        if recv == "":
                            recv = "None could be found nearby..."
                        else:
                            recv = recv.replace("minecraft:","")
                            arg = arg.split(":")[-1]

                        embed = discord.Embed(title=f"📍 **{arg.capitalize()}**", color=discord.Color.purple())
                        embed.add_field(name="Search Results: ",value=recv, inline=True)
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                        await ctx.send(embed=embed)

                        return
                else:
                    await ctx.send(f"{player.display_name} is not online.")
                    return
            else:
                await ctx.send(f"Server is not online")
                return
        else:
            await ctx.send(f"{player.display_name}'s account is not linked.")
            return
        
    async def _find_biome(self, ctx, arg):
        pass


        #searches from a provided list of structures and returns the one that is closest
    def _list_search(self, playerName, list) -> list:
        #Clear list
        nearest_stuct = []
    
        #Itterate through each sturcture in the list
        for struct in list:

            #Send a command to the server using the player as starting point and one the currect structure
            recv = self.srv.sendCmd(f"execute as {playerName} at @s run locate structure {struct}")
            
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
    await bot.add_cog(Find(bot))
        
            