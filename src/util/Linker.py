""" Linker Class """
""" Used for attaching discord accounts to players on the server """
import os, json, logging
from src.util.Config import Config

logger = logging.getLogger(__name__)

class Linker:
    def __init__(self) -> None:
        self.cfg = Config()
        
        #Gets the file stored at the location of the env_var path
        linker_file = os.getenv(self.cfg.get_str("Linker", "link_path_env_var_name"))  
        
        if not linker_file:
            raise ValueError(f"Environment variable {env_var_name} is not set!")
    
        self.linker_file = linker_file
        
    def setMinecraftName(self, UUID: str, name: str) -> None:
        UUID = str(UUID)
        
        try:
            #get the current contents of .json file
            with open (self.linker_file, "r") as f:
                data = json.load(f)            
            
            data[UUID] = name
        
            #Write to json file
            with open(self.linker_file, "w") as f:
                json.dump(data, f, indent=4)
            
        except Exception as e:
            print(f"ERR: {e}")
        
        
    def getMinecraftName(self, UUID: str) -> str:
        UUID = str(UUID)
        
        if self.isLinked(UUID):
            #get the current contents of .json file
            with open (self.linker_file, "r") as f:
                data = json.load(f)            
            
            return data[UUID]
        else:
            return None
                      
    
    def isLinked(self, UUID: str) -> bool:
        UUID = str(UUID)
        try:
            #get the current contents of .json file
            with open (self.linker_file, "r") as f:
                data = json.load(f)            
            
            #Check if the UUID is in the json file
            if UUID in data:
                return True
            else:
                return False
                   
        except Exception as e:
            print(f"ERR: {e}")
            return False
        
    
        