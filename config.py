
import configparser
import os
import argparse
import sys

ERROR_CFG = """\
Configuration file {conf} not found

  Create configuration file `{conf}` with contents

    [Default]
    Zotfile_base_folder = ; Your zotfile base folder
    Zotfile_sub_folder = ; Your zotfile sub folder (if exists)
    rM sync folder= Zotero; Your rM folder
    rM archive folder= Zotero_Archive; The archive folder
    
    Zipfiles = true
    rmapi = /path/to/rmapi
"""

DEFAULTS = {
    'rm_sync_folder': 'Zotero',
    'rm_archive_folder': 'Zotero_Archive',
    'zipfiles': True,
    'rmapi': 'rmapi'
}
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

def parse(argv = None):
    if argv == None:
        argv=sys.argv

    configparser = argparse.ArgumentParser(description='Synchronize reMarkable and Zotero tablet export.' ,
                                           formatter_class=argparse.RawDescriptionHelpFormatter,
                                           add_help=False)
    configparser.add_argument('--config', type=str, default='Default',
                              help='config.ini section name')
    args, remaining_args = configparser.parse_known_args()

    configSection = args.config
    CONFIG = read_config()

    if not configSection in CONFIG:
        msg = f'Config section "{configSection}" does not exists.'
        raise Exception(msg)

    DEFAULTS.update(dict(CONFIG.items(configSection)))

    # Parse rest of arguments
    parser = argparse.ArgumentParser(
        parents=[configparser])
    parser.add_argument('-C', '--clean-up', action='store_true',
                        help="Delete all files on reMarkable that don't exists in the Zotero folder.")
    parser.add_argument('-F', dest='fetch_all', action='store_true',
                        help="Fetch all files in zotfile folder from reMarkable, even if they are not in the Zotero folder."
                             " (Overwrites --C)")
    parser.add_argument('--nofetch', action='store_false', dest='fetch_all',
                        help="Do not fetch all files in zotfile folder from reMarkable, even if they are not in the Zotero folder."
                        )
    parser.set_defaults(**DEFAULTS)
    args = parser.parse_args(remaining_args)
    return args
