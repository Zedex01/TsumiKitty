import discord
from discord.ext import commands

#Copied from the discord api:
class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    #Displays errors in commands
    async def on_command_error(self, ctx, error):
        print(f"Error in command {ctx.command}: {error}")
        await ctx.send(f"⚠️ Error: {str(error)}")
