
import configparser
import os
import argparse
import sys

ERROR_CFG = """\
Configuration file {conf} not found

  Create configuration file `{conf}` with contents

    [Default]
    Zotfile_base_folder=;
    Zotfile_sub_folder =;
    rM_sync_folder=paper
    #rM_archive_folder=Archive;
    #rmapi=~/path/to/rmapi
    #zip_files=true
"""

DEFAULTS = {
    'rm_sync_folder': 'Zotero',
    'rm_archive_folder': 'Zotero_Archive',
    'rmapi': 'rmapi',
    'zip_files': True,
    'clean_up': False,
    'fetch_all': True,
}

def read_config() -> configparser.ConfigParser:
    """
    Read and return Remt project configuration.
    """
    conf_file = os.path.expanduser(os.path.join('~','.config','zotero2rm.ini'))
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

    for option in CONFIG.options(configSection):
        if option in ['zip_files','clean_up','fetch_all', 'upload_only']:
            DEFAULTS.update({option: CONFIG.getboolean(configSection, option)})
        else:
            DEFAULTS.update({option: CONFIG.get(configSection, option)})
    # Parse rest of arguments
    parser = argparse.ArgumentParser(
        parents=[configparser])
    parser.add_argument('-c', '--clean-up', action='store_true',
                        help="Archive all files on reMarkable that don't exists in the Zotero folder.")
    parser.add_argument('--fa', dest='fetch_all', action='store_true',
                        help="Fetch all files in zotfile folder from reMarkable, even if they are not in the Zotero folder."
                             " (Overwrites --clean-up)")
    parser.add_argument('--nfa', action='store_false', dest='fetch_all',
                        help="Do not fetch files not in the Zotero folder."
                        )
    parser.set_defaults(**DEFAULTS)
    args = parser.parse_args(remaining_args)
    return args
