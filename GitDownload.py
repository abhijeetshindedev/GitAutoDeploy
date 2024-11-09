import csv
import io
import os
import sys
import base64
import shutil
import getopt
from github import Github
from github import GithubException
import openpyxl
from pandas import read_csv
import requests



def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    print("get_sha_for_tag done...")
    return matched_tags[0].commit.sha


def download_directory(token,org,repo,branch,folder,src_folder):

    # url = "https://github.com/Infosys-ValuePlusCOE/DCE_LEDS/archive/main.zip"
    url = "https://github.com/"+org+"/"+repo+"/archive/main.zip"

    payload = {}
    headers = {
    'Authorization': 'Bearer '+token,
    'Cookie':'color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; dotcom_user=poonam-ghadge01_infosys; logged_in=yes'
    }
    print ("before request")
    response = requests.request("GET", url, headers=headers, data=payload)
    print("after request")
    print("response : ",response)
    # checkout_path = "C://Users//projadmin//Downloads//Git_Deploy_POC//GitPipeline//checkout//A.zip"
    # checkout_path = src_folder +'//A.zip'
    checkout_path =  os.path.join(src_folder,"A.zip")
    with open(checkout_path,"wb") as f:
        f.write(response.content)
    print ("after response write")
    return checkout_path
    # print(response.text)

def usage():
    """
    Prints the usage command lines
    """
    print ("usage: gh-download --token=token --org=org --repo=repo --branch=branch --folder=folder")

def start_download(token,org,repo,branch,folder,src_folder):
    """
    Main function block
    """

    github = Github(token)
    organization = github.get_organization(org)
    repository = organization.get_repo(repo)
    sha = get_sha_for_tag(repository, branch)
    download_directory(repository, sha, folder,src_folder)

if __name__ == "__main__":
    """
    Entry point
    """
    start_download(sys.argv[1:])