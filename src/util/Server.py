"""
For Communicating with the server via TCP connection

**NOTE: for this feature to work properly, 
you must configure your server.properties file correctly.

"""

from mcrcon import MCRcon
import os, logging, asyncio

logger = logging.getLogger(__name__)


class Server:
    def __init__(self) -> None:
        self.PORT = os.getenv('SERVER_PORT')
        self.PASS = os.getenv('SERVER_PASSWORD')
        
    def sendCmd(self, content: str) -> str:
        if self.isRunning():
            with MCRcon("127.0.0.1", self.PASS, port=int(self.PORT)) as mcr:
                output = mcr.command(content)
            return output
        return "-1"
        
#TODO
    def isRunning(self) -> bool:
        
        try:
            #Try to probe the server and see if there is a response
            with MCRcon("127.0.0.1", self.PASS, port=int(self.PORT)) as mcr:
                mcr.command('list')
                logger.info("Server is online")
            return True
            
        #except(ConnectionRefusedError, socket.timeout, OSError):
        except Exception as e:
            logger.info("Server is Offline")
            return False
    
    #waits the duration 
    async def waitUntilRunning(self, interval = 5, timeout = 300) -> bool:
        
        elapsed = 0
        while elapsed < timeout:
            #If the server is running, return true
            if self.isRunning():
                return True
            
            #Wait one interval and increment elapsed by interval
            await asyncio.sleep(interval)
            elapsed += interval
            
        #If timeout is reached, return False
        return False
        
    #Checks to see if a specific player is online
    def playerOnline(self, playerName) -> bool:
        logger.info(f"Checking if {playerName} is online")
        
        #Sends commands to server, has built-in check to see if server is online
        output = self.sendCmd("list")
            
        players = output.split(":",1)[1].strip()
        players = players.split(", ") if players else []
        
        if playerName in players:
            logger.info("Player online")
            return True
        else:
            logger.info("Player not online")
            return False
        
 
        
        
    