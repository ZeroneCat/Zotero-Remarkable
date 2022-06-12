
import configparser
import os
ERROR_CFG = """\
Configuration file {conf} not found

  Create configuration file `{conf}` with contents

    [Default]
    Zotfile base folder=~/Reading
    Zotfile sub folder = rM
    rM sync folder=Zotero
    rM archive folder=Zotero_Archive
    
    Zipfiles = true
    rmapi = rmapi
    
"""

def read_config() -> configparser.ConfigParser:
    """
    Read and return Remt project configuration.
    """
    conf_file = os.path.expanduser('~/.config/zotero2rm.ini')
    if not os.path.exists(conf_file):
        msg = ERROR_CFG.format(conf=conf_file)
        raise Exception(msg)

    cp = configparser.ConfigParser()
    cp.read(conf_file)
    return cp
