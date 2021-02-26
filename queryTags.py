import os, json
import requests
import datetime
from pprint import pprint
from enum import Enum


APPLICATION_SERVICES_TAGS_INFO = 'https://api.github.com/repos/mozilla/application-services/tags'

CARTFILE = 'Cartfile'
CARTFILE_RESOLVED = 'Cartfile.resolved'

client ='https://api.github.com/repos/mozilla/application-services/tags'
filepath = 'Cartfile'

print("Fetching project data from Github..." + "\n")

'''
resp = requests.get(APPLICATION_SERVICES_TAGS_INFO)
resp.raise_for_status()
resp_json = resp.json()

print(resp_json[0])

latest_tag = resp_json[0]
print(latest_tag['name'])
'''

def available_tags():
    try:
        resp = requests.get(APPLICATION_SERVICES_TAGS_INFO)
        resp_json = resp.json()
        print (resp_json[0])
        return resp_json[0]
    except HTTPError as http_error:
        print('An HTTP error has occurred: {http_error}')
    except Exception as err:
        print('An exception has occurred: {err}')

def latest_version():
    tags = available_tags()
    print (tags['name'])
    latest_tag_version = tags['name']
    return latest_tag_version

def read_cartfile_tag_version():
    myLines = []

    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            #print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            cnt += 1
            #myLines.append(line)
            #print(myLines)


            if 'mozilla/application-services' in line:
                print("here" + line)
                result = line.find("v", 32)
                print(result)
                print(len(line))
                current_tag_version = ''

                #44 to 50
                for i in range(44, 51):
                    print(line[i])
                    current_tag_version+=line[i]
                print(current_tag_version)
                return(current_tag_version)

def update_cartfile_tag_version(current_tag, as_repo_tag):
    # read the Cartfile and change it
    file = open("Cartfile", "r+")
    data = file.read()
    data = data.replace(current_tag, as_repo_tag)
    file.write(data)

    file.close()


def update_cartfile_resolved_tag_version(current_tag_version, repo_tag_version):
    # read the Cartfile.resolved and change it
    file = open("Cartfile.resolved", "r+")
    data = file.read()
    data = data.replace(current_tag, as_repo_tag)
    file.write(data)
    file.close()


def compare_versions(current_tag_version, repo_tag_version):
    if current_tag_version < repo_tag_version:
        print("Update A-S version and create PR")
        return True
    else:
        print("No new versions, skip")
        return False

if __name__ == '__main__':
    '''
    STEPS
    1. check Application-Services repo for latest version
    2. compare latest with current cartage and cartage.resolved versions in repo 
    3. if same exit, if not, continue 
    4. update both cartfile and cartfile.resolved
    '''
    as_repo_tag= latest_version()
    current_tag = read_cartfile_tag_version()
    if compare_versions(current_tag, as_repo_tag):
        update_cartfile_tag_version(current_tag, as_repo_tag)


