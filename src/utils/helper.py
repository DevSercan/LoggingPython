import json # Used for operations in JSON format.
import os # Used for operating system-related operations.

def getConfig() -> dict:
    """ Reads the configuration file in JSON format and returns it as a dictionary.
    If the file does not exist, creates it with default content. """
    
    defaultConfig = {
        "logging": {
            "minimumLevel": 5,
            "path": "logs/",
            "fileSizeLimitMegabytes": 6,
            "printLogsToConsole": 1
        }
    }
    
    configPath = "config.json"
    
    if not os.path.exists(configPath): # Check if the configuration file exists.
        with open(configPath, 'w', encoding='utf-8') as file: # Create the file if it doesn't exist.
            json.dump(defaultConfig, file, indent=4) # Write default content with 4-space indentation.
        return defaultConfig # Return the default content.
    
    # If the file exists, read its content and return it as a dictionary.
    with open(configPath, 'r', encoding='utf-8') as file:
        configDict = json.load(file)
    return configDict
