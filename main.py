import os
from pathlib import Path
import sys
import zipfile
from GitDownload import download_directory, start_download
from transfer_and_restart import copy_folder, stop_flask, stop_flask_app

#python main.py --token=__ --org=__

def main():

    print("Starting Git Pipeline")
    token = input("Enter Github Private Access Token : ")
    org = input("Enter Github Organization Name : ")
    repo = input("Enter Repository Name : ")
    branch = input("Enter Branch Name : ")
    folder = input("Enter Github Folder Name : ")
    dest_folder = input("Enter path of Destination Directory : ")

    proj_dir = os.getcwd()
    src_folder = os.path.join(proj_dir,"checkout")
    if not os.path.exists(src_folder):
        os.makedirs(src_folder)
    print ("data downloaded temp : ",src_folder)

    app_script = dest_folder +"//"+ repo+"-main//"+ folder


    #download data from Git to localDir
    print("Starting Git Pipeline")

    print("Git Download start.........")

    checkout_folder = download_directory(token,org,repo,branch,folder,src_folder)
    

    print("Git Download successful.......")

    #start transferring data
    #close application
    print("stopping running python process")
    stop_flask_app()
    # stop_flask("python.exe")
    print("Process stopped...!!!")

    #delete-copy-restart data from target Directory

    copy_folder(src_folder,dest_folder,app_script,checkout_folder)
    print("application started successfully!!!")

if __name__ == "__main__":
    main()
