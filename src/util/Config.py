""" Class for grabbing from config file"""
import configparser, os, sys
from pathlib import Path

class Config:
    def __init__(self, config_path:str=None) -> None:
        if not config_path:
            if getattr(sys, "frozen", False):
                #print("DEBUG: Running as executeable")
                CONFIG_FILE = Path(sys.executable).parent / "config.ini"
            else:
                #print("DEBUG: Running as script(.py)")
                CONFIG_FILE = Path(__file__).parent.parent / "config.ini"
        else:
            CONFIG_FILE = Path(config_path)
        
        #Set config file path
        self.config_path = CONFIG_FILE 
        
        #Set config file object
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE)

    #Getters from config file
    def get_bool(self, section: str, key: str, fallback=False) -> bool:
        return self.config.getboolean(section, key, fallback=fallback)
    
    def get_str(self, section:str , key:str , fallback=None) -> str:
        return self.config.get(section, key, fallback=fallback)
        
    def get_int(self, section:str, key:str, fallback=-1) -> int:
        return self.config.getint(section, key, fallback=fallback)

    #Generate config from template
    def gen(self, template=None):
        #Check if config file exists:

        if not (self.config_path.exists() and self.config_path.is_file()):

            #if is dir, delete it first:
            if self.config_path.is_dir():
                self.config_path.rmdir()

            #Create new config file
            self.config_path.touch() #Create file

            if self.config_path.exists() and self.config_path.is_file():

                #If a template is provided, write into config file
                if template:
                    for section, values in template.items():
                        #Add Section to config:
                        if not self.config.has_section(section):
                            self.config.add_section(section)

                        #Add every key and value pair:
                        for key, value in values.items():
                            self.config.set(str(section), str(key), str(value))

                    #Write data to the config file:
                    with open(self.config_path, "w") as file:
                        self.config.write(file)

                return 0, "GEN_OK"

            else:
                #print("[-] ERROR: Unable to create config file")
                return 1, "GEN_FAIL"
        
        else:
            return 0, "ALREADY_EXISTS"


