#!/user/bin/env python3

import os
import subprocess
from config import parse

args = parse()

ZOTERO_FOLDER = os.path.join(
    args.zotfile_base_folder,
    args.zotfile_sub_folder
)
if "~" in ZOTERO_FOLDER:
    ZOTERO_FOLDER = os.path.expanduser(ZOTERO_FOLDER)

RM_FOLDER =  args.rm_sync_folder
RM_FOLDER_ARCHIVE = args.rm_archive_folder

RMAPI_BIN = args.rmapi

def rmapi(cmd):
    return subprocess.check_output(
        f"{RMAPI_BIN} {cmd}", shell=True, stderr=subprocess.STDOUT
    ).decode("utf-8").split('\n')[0:-1]

def upload_file(file):
    path = os.path.join(ZOTERO_FOLDER, f"{file}.pdf")
    rmapi(f'put "{path}" "{RM_FOLDER}"')

def download_file(file):
    path = '/'.join([RM_FOLDER,file])
    zip_file = f"{file}.zip"
    try:
        rmapi(f'geta -a "{path}"')
        f_annotations = f"{file}-annotations.pdf"
        os.replace(f_annotations,os.path.join(ZOTERO_FOLDER,f"{file}.pdf"))
    except Exception as inst:
        if not ("document has no pages" in inst.output.decode("utf-8")):
            print(inst.output.decode("utf-8"))
    finally:
        if (os.path.isfile(zip_file)):
            os.remove(zip_file)

def delete_file(file):
    path = '/'.join([RM_FOLDER,file])
    rmapi(f'rm "{path}"')

def get_files():
    files_on_remarkable = set([f.split('\t')[-1] for f in rmapi(f"ls {RM_FOLDER}")])

    files_on_local = set([os.path.splitext(os.path.basename(f))[0] for f in os.listdir(ZOTERO_FOLDER) if f.endswith(".pdf")])
    return files_on_remarkable, files_on_local

def process_files(delete=False, download=False):
    files_on_remarkable, files_on_local = get_files()
    files_to_download = files_on_remarkable.copy()

    if not download:
        files_to_download &= files_on_local

    files_to_upload = files_on_local - files_on_remarkable
    files_to_delete = files_on_remarkable - files_on_local

    for file in files_to_upload:
        print(f"[Uploading  ] '{file}'")
        upload_file(file)

    for file in files_to_download:
        print(f"[Downloading] '{file}'")
        download_file(file)

    if delete and not download:
        for file in files_to_delete:
            print(f"[Deleting   ] '{file}'")
            delete_file(file)

if __name__ == '__main__':
    pass
    #process_files(delete=args.delete, download=args.download)
