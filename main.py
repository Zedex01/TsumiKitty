#Matthew Moran 2025-09-10

# py -c "import sys; print(sys.executable)"  
# To Install: py -m pip install -U discord.py

#Python Style guide:
#| Item                | Convention                      | Example                             |
#| ------------------- | ------------------------------- | ----------------------------------- |
#| Variable / Function | lowercase_with_underscores      | `total_score`, `send_message`       |
#| Class               | CapWords / PascalCase           | `UserProfile`, `DiscordBot`         |
#| Constant            | UPPERCASE_WITH_UNDERSCORES      | `MAX_CONNECTIONS`, `DEFAULT_PREFIX` |
#| Module / Package    | lowercase_with_underscores      | `my_module`, `utils`                |
#| Private (internal)  | _single_leading_underscore      | `_helper_method`                    |
#| Private (mangled)   | __double_leading_underscore     | `__private_var`                     |

#a method or variable prefixed with '_' is a hint to indicate it is 'protected'
#and should not be accesed from outside the class

import discord, os, asyncio, platform, sys, logging
from src.bot.Bot import Bot
from src.commands import *
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler

#Util Imports
from src.util.Config import Config
from src.util.Server import Server

#Grab current Env Variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#Create config object
cfg = Config()

#Set command Prefix
PREFIX = cfg.get_str("Bot", "prefix")
if not PREFIX:
    print("[-] Prefix not set!")
    sys.exit(1)

bot = Bot(command_prefix=PREFIX, intents=intents)

#Get Discord Bot Token
TOKEN = cfg.get_str("Bot", "token")
if not TOKEN:
    print("[-] Token Not Set!")
    sys.exit(1)


#logging Setup
def setup_logging():
    # Ensure logs/ directory exists

    #get log location from config file
    log_dir = cfg.get_str("Logger", "Logs_path")

    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        print("[-] Logger init error: ", e)
        sys.exit(2)
    
    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # capture everything, handlers will filter

    # Formatter (shared)
    formatter = logging.Formatter(
        "[%(levelname)s] [%(asctime)s] %(message)s [%(name)s]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    #Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # only show INFO+ in console
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (daily rotation, keep 50 days)
    log_file = os.path.join(log_dir, "discord_bot.log")
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1,
        backupCount=50, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # keep all details in file
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


#TODO: Add helper method to simplify adding more commands using server, logger and config etc

#Loading modular commands (cogs)
async def load_extensions():
    await bot.load_extension("src.commands.GetServerStatus")
    #await bot.load_extension("src.commands.Exit")
    await bot.load_extension("src.commands.Reload")
    #await bot.load_extension("src.commands.StartServer")
    #await bot.load_extension("src.commands.StopServer")
    await bot.load_extension("src.commands.ListPlayers")
    await bot.load_extension("src.commands.LinkAccount")
    #await bot.load_extension("src.commands.Locate")
    #await bot.load_extension("src.commands.LocateStructure")
    await bot.load_extension("src.commands.LogWatcherCog")
    await bot.load_extension("src.commands.Find")

   

# Main Function
async def main():
    logger = setup_logging()
    logger.info("Tsumikitty is starting")
    async with bot:
        await load_extensions() #Load all command classes
        await bot.start(TOKEN)

# Launch
if __name__ == "__main__":
    asyncio.run(main()) #Start the main Function