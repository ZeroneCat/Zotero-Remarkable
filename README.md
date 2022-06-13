# Zotero to reMarkable Cloud

This script can be used with the `Send to Tablet` function from [ZotFile](http://zotfile.com/).
It synchronizes the ZotFile basis folder with a folder in the reMarkable cloud.

The following changes are synchronized:
- A new file in the ZotFile folder is send to the reMarkable cloud.
- Any updated to a file on the reMarkable cloud is fetched into the ZotFile folder.
- With the command line option `--clean-up`, any file that was removed from the ZotFile folder is moved to an archive folder.

## Configuration

- After installation of ZotFile, the only necessary option in Zotero is to define an base folder in the ZotFile preferences.
- The script uses [rmapi](https://github.com/juruen/rmapi), which requires setting up the connection to the cloud.
- Configuration file:

  Create a configuration file at ~/.config/zotero2rm.ini with contents:

    [Default]
    Zotfile_base_folder=;
    Zotfile_sub_folder =;
    rM_sync_folder=; #e.g. 'Zotero'
    rM_archive_folder= ;# create this Archive folder in reMarkable.
    #rmapi=/path/to/rmapi
    #zip_files=true

## Help


check usage: sync.py [-h]


