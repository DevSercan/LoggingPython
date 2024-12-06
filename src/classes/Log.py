import time # Used to timestamp log file names.
import traceback # Displays current error details for debugging.
import os # Used for file operations.
from src.utils.helper import getConfig

# Load configuration settings.
CONFIG = getConfig()
PATH = str(CONFIG["logging"]["path"]) # Path to store log files.
LEVEL = int(CONFIG["logging"]["minimumLevel"]) # Minimum logging level to process.
SIZE = int(CONFIG["logging"]["fileSizeLimitMegabytes"]) # Max log file size in MB.
PRINTCONSOLE = bool(CONFIG["logging"]["printLogsToConsole"]) # Whether to print logs to console.

class Log:
    """ A class used for logging operations. """
    def __init__(self, printConsole:bool=PRINTCONSOLE, logFolder:str=PATH, logLevel:int=LEVEL, maxFileSizeMB:int=SIZE):
        """ Initializes the log class with configuration settings. """
        if not 1 <= logLevel <= 5:
            raise ValueError("'logLevel' value must be between 1 and 5.")
        self.printConsole = printConsole # Option to print logs to console.
        self.logFolder = logFolder # Folder to store log files.
        self.logLevel = logLevel # Minimum log level to process.
        self.maxFileSizeMB = maxFileSizeMB # Max log file size before creating a new one.
        self.levelTags = {1: "[CRITICAL]", 2: "[ERROR]", 3: "[WARNING]", 4: "[INFO]", 5: "[DEBUG]"} # Tags for log levels.

        # Create log folder if it doesn't exist.
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder)

    def _log(self, message:str, level:int):
        """ Handles the logging process, including file rotation and console output. """
        try:
            if level <= self.logLevel:
                filePath = self._getLastLogFile() # Get the latest log file.

                # Check if the current log file exceeds the max size.
                if os.path.exists(filePath):
                    currentSize = os.path.getsize(filePath) / (1024*1024) # Convert file size to MB.
                    if currentSize > self.maxFileSizeMB: # If the file size exceeds the target size, creates a new log file.
                        self.createLogFile() # Create a new log file if size limit is exceeded.
                    del currentSize

                # Format log message with timestamp and level.
                logTime = time.strftime("[%d.%m.%Y %H:%M:%S]") # Current time in 'day.month.year hour:minute:second' format.
                logText = f"{logTime} {self.levelTags[level]} {message}"
                
                if self.printConsole and level != 5: # Condition is met if the option to print log entries to the console is True AND the log message level to be printed is not Debug.
                    print(logText) # Prints the log entry to the console.
                
                # Append the log message to the file.
                with open(filePath, "a", encoding="utf-8") as file: # Appends to the file if it exists. If not, creates it.
                    file.write(f"{logText}\n")
                
                del logTime, logText
        except Exception as e:
            # Handle any exceptions during logging and log the error details.
            errorName = type(e).__name__ # Retrieves the name of the caught error as a string.
            errorMessage = f"[{errorName}]\n{traceback.format_exc()}"
            with open(filePath, "a", encoding="utf-8") as file:
                file.write(f"LogError: {errorMessage}\n")
    
    def createLogFile(self) -> str:
        """ Creates a new log file and returns its path. """
        fileName = time.strftime("log_%d%m%Y-%H%M%S.log") # File name format: 'log_dayMonthYear-HourMinute.log'.
        filePath = os.path.join(self.logFolder, fileName)

        # Create a new empty log file.
        with open(filePath, "w", encoding="utf-8") as file:
            file.write("")

        del fileName
        return filePath

    def _getLastLogFile(self) -> str:
        """ Retrieves the most recently created log file or creates a new one if none exist. """
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder) # Ensure the log folder exists.
        
        if len(os.listdir(self.logFolder)) < 1:
            self.createLogFile() # Create the first log file if the folder is empty.
        
        # Find the most recently created log file.
        fullLogPaths = [os.path.join(self.logFolder, file) for file in os.listdir(self.logFolder)]
        lastLogFile = max(fullLogPaths, key=os.path.getctime)
        del fullLogPaths
        return lastLogFile

    def critical(self, message:str):
        """ Logs a message at the CRITICAL level. """
        self._log(message, 1)

    def error(self, message:str):
        """ Logs a message at the ERROR level. """
        self._log(message, 2)

    def warning(self, message:str):
        """ Logs a message at the WARNING level. """
        self._log(message, 3)

    def info(self, message:str):
        """ Logs a message at the INFO level. """
        self._log(message, 4)

    def debug(self, message:str):
        """ Logs a message at the DEBUG level, primarily for code details. """
        self._log(message, 5)