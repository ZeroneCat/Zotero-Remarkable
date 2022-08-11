
import configparser
import os
import argparse
import sys

ERROR_CFG = """\
Configuration file {conf} not found

  Create configuration file `{conf}` with contents

  [DEFAULT]
    Zotfile_base_folder=/path/to/Zotfile/base/folder
    rM_archive_folder=/path/to/rM/archive/folder
    rmapi=/path/to/rmapi
    default_config=example
  [example]
    Zotfile_sub_folder =zotero_sub_folder
    rM_sync_folder=rM_folder

"""

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
    configparser.add_argument('--config', type=str,
                              help='config.ini section name')

    args, remaining_args = configparser.parse_known_args()

    configSection = args.config

    config = read_config()


    if not configSection in config:
        msg = f'Config section "{configSection}" does not exists. '
        configSection = config[config.default_section].get("default_config")
        msg += 'Default section does not exists.'
        if not configSection in config:
            raise Exception(msg)
    DEFAULTS = dict()
    for option in config.options(configSection):
        if option in ['zip_files', 'clean_up', 'fetch_all']:
            DEFAULTS.update({option: config.getboolean(configSection, option)})
        else:
            DEFAULTS.update({option: config.get(configSection, option)})
    # Parse rest of arguments
    parser = argparse.ArgumentParser(
        parents=[configparser])
    parser.add_argument('-c', '--clean-up', action='store_true',dest='archive',
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
