"""Read the newest log file at a location returning logs matching the levels"""

from glob import glob
from os import path

def read_logs(folder_path:str, levels:list):
    """Finds the most recent .log in the folder provided by the path param then 
    returns lines containging the level(s) keyword(s).

    :param path: str
        os.path formatted

    :param level: list str
        One or more string values indicating logging levels to be returned

        NOTSET
        DEBUG
        INFO
        WARNING
        ERROR
        CRITICAL

    :return: list - str
    """
    # Search through the log files in the folder indicated by the folder_path
    # parameter and set the newest file to the newest_log variable
    list_of_log_files = glob(path.join(folder_path, "*.log"))
    newest_file = max(list_of_log_files, key=path.getctime)

    return_list = []
    with open(newest_file, "r") as file:
        for line in file:
            if any(level.upper() in line for level in levels):
                return_list.append(line)
            else:
                pass
    
    return return_list