#!/user/bin/env python3

import os
import subprocess
import rmrl
from config import parse

args = parse()

ZOTERO_FOLDER = os.path.expanduser(os.path.join(
    args.zotfile_base_folder,
    args.zotfile_sub_folder
))

RM_FOLDER =  args.rm_sync_folder
RM_FOLDER_ARCHIVE = args.rm_archive_folder

RMAPI_BIN = os.path.expanduser(args.rmapi)

ZIPFILES=args.zip_files
zipdir = os.path.join(ZOTERO_FOLDER, os.path.basename(RM_FOLDER))
if not os.path.isdir(zipdir):
    os.mkdir(zipdir)

def rmapi(cmd, cmddir="."):
    return subprocess.check_output(
        f"cd {cmddir} && {RMAPI_BIN} {cmd}", shell=True, stderr=subprocess.STDOUT
    ).decode("utf-8").split('\n')[0:-1]

def upload_file(file):
    rmapi(f'put "{file}.pdf" "{RM_FOLDER}"', ZOTERO_FOLDER)

def fetch_files(files_to_download, fetch_all=True):
    print("\n".join(rmapi(f'mget -i "{RM_FOLDER}"', ZOTERO_FOLDER)).replace("downloading ",
                                                                     "[Downloading]\t"))  # download *.zip using rmapi
    for f in files_to_download:
        try:
            zip_file = os.path.join(zipdir, f+".zip")
            pdf_file = os.path.join(ZOTERO_FOLDER, f+".pdf")
            if (os.path.isdir(pdf_file) and os.path.getmtime(zip_file)>os.path.getmtime(os.path.join(ZOTERO_FOLDER, f+".pdf"))) or\
                (not os.path.isdir(pdf_file) and fetch_all):

                output = rmrl.render(zip_file)
                with open(os.path.join(ZOTERO_FOLDER, f"{f}.pdf"), 'wb') as outputpdf:
                    outputpdf.write(output.read())
        except:
            print("[Fail!] to convert {f}, unknown error.")



def download_single_file(file):
    remotepath = '/'.join([RM_FOLDER,file])
    zip_file = os.path.join(zipdir, f"{file}.zip")

    try:
        print("".join(rmapi(f'get "{remotepath}"', zipdir)[-2:]).replace("downloading: ", "[Downloading]\t")) #download *.zip using rmapi
        output = rmrl.render(zip_file)
        with open( os.path.join(ZOTERO_FOLDER, f"{file}.pdf"), 'wb') as outputpdf:
            outputpdf.write(output.read())
    except Exception as inst:
        if not ("document has no pages" in inst.output.decode("utf-8")):
            print(inst.output.decode("utf-8"))
    finally:
        if (not ZIPFILES and (os.path.isfile(zip_file))):
            os.remove(zip_file)

def delete_file(file):
    path = '/'.join([RM_FOLDER,file])
    rmapi(f'rm "{path}"')
    print(f"[Delete]\t {path}")

def archive_file(file):
    archive_path = '/'.join([RM_FOLDER_ARCHIVE, file])
    original_path = '/'.join([RM_FOLDER, file])
    try:
        rmapi(f'mv "{original_path}" "{archive_path}"')
    except:
        print(f"[Fail] to archive {original_path}!!!")

def get_files():
    Warning_RMAPI = {"Refreshing tree...",
                    "WARNING!!!",
                    "  Using the new 1.5 sync, this has not been fully tested yet!!!",
                    "  Make sure you have a backup, in case there is a bug that could cause data loss!",
                     "ReMarkable Cloud API Shell"}
    files_on_remarkable = set([f.split('\t')[-1] for f in rmapi(f"ls {RM_FOLDER}")])
    files_on_remarkable -= Warning_RMAPI
    files_on_local = set([os.path.splitext(os.path.basename(f))[0] for f in os.listdir(ZOTERO_FOLDER) if f.endswith(".pdf")])
    return files_on_remarkable, files_on_local

def process_files(clean_up=False, fetch_all=False):
    files_on_remarkable, files_on_local = get_files()

    files_to_download = files_on_remarkable.copy()
    if not fetch_all:
        files_to_download &= files_on_local

    files_to_upload = files_on_local - files_on_remarkable
    files_to_archive = files_on_remarkable - files_on_local

    for file in files_to_upload:
        print(f"[Uploading] \t '{file}'")
        upload_file(file)

    if len(files_to_download):
        fetch_files(files_to_download, fetch_all)

    if not fetch_all:
        for file in files_to_archive:
            print(f"[Archiving]\t '{file}'")
            archive_file(file)

if __name__ == '__main__':
    pass
    process_files(clean_up=args.clean_up, fetch_all=args.fetch_all)
