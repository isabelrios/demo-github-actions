import os, json
import requests
import datetime
from github import Github


SHAVARD_REPO = 'mozilla-services/shavar-prod-lists'
github_access_token = os.getenv("GITHUB_TOKEN")

def  get_latest_branch_and_commit():

    g = Github(github_access_token)
    repo = g.get_repo(SHAVARD_REPO)

    response_json = list(repo.get_branches())
    # This shows the available branches:
    #[Branch(name="69.0"), Branch(name="70.0")......
    # (str(response_json[0]))
    # This returns first branch information
    # Branch(name="69.0")

    max_branch_name = ''

    # Iterate all the branches to get the one with higher value
    for i in range(len(response_json)):
        string = str(response_json[i])
        current_version = ''
        version_found = '"'
        initial_occurrence = 1
        final_ocurrence = initial_occurrence + 1
        # version format: XX.Y
        val = -1
        for i in range(0, initial_occurrence): 
            val = string.find(version_found, val + 1) 
        
        for i in range(0, final_ocurrence): 
            final_val = string.find(version_found, val + 1) 

        for i in range(val+1, final_val):
            current_version+=string[i]

        if current_version[0].isdigit():
            if (current_version) > max_branch_name:
                max_branch_name = current_version

    branch = repo.get_branch(max_branch_name)
    commit = branch.commit.sha

    print(f"Branch  {branch.name}")
    print(f"Commit  {commit}")
    return branch.name, commit

def find_version(line):
    current_version = ''
    version_found = '"'
    initial_occurrence = 3
    final_ocurrence = initial_occurrence + 1
    # version format: vXX.Y.Z
    val = -1
    for i in range(0, initial_occurrence): 
        val = line.find(version_found, val + 1) 
    
    for i in range(0, final_ocurrence): 
        final_val = line.find(version_found, val + 1) 

    for i in range(val+1, final_val):
        current_version+=line[i]
    print(f"Current version in repo {current_version}")
    return(current_version)


def read_cartfile_version(file):
    # Read Cartfile and Carfile.resolved to find the current a-s version
    with open(file) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            line = fp.readline()
            cnt += 1

            # Find the line that defines the a-s version
            if 'mozilla-services/shavar-prod-lists' in line:
                return find_version(line)


def update_cartfile(repo_branch, shavard_branch, file_name):
    # Read the Cartfile and Cartife.resolved, update
    file = open(file_name, "r+")
    data = file.read()
    data = data.replace(repo_branch, shavard_branch)
    file.close()
    
    file = open(file_name, "wt")
    file.write(data)
    file.close()


def main():
    shavard_latest_branch, shavard_latest_hash_commit = get_latest_branch_and_commit()
    repo_branch = read_cartfile_version('Cartfile')
    repo_commit = read_cartfile_version('Cartfile.resolved')

    # Add a contition to run only when those are different
    update_cartfile(repo_branch, shavard_latest_branch, 'Cartfile')
    update_cartfile(repo_commit, shavard_latest_hash_commit, 'Cartfile.resolved')
    

if __name__ == '__main__':
    main()

