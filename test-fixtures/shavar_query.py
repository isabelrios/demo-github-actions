import os
import json
import requests
import shutil
import tempfile


PATH_TO_FILES = './content-blocker'
ORIGINAL_SHAVAR_FILE = PATH_TO_FILES + '/base-fingerprinting-track.json'
TMP_SHAVAR_FILE = './content-blocker/tmp.json'
tmp = tempfile.NamedTemporaryFile()


'''
STEPS
1. POST to shavar url
2. Process the response to get the u value
3. Append .json to u value to compose the new url: name_of_the_list.json
4. GET to the new url to retrieve the list
5. Compare the json list with the local json list
'''


class Shavar:

    def __init__(self):
        pass

    def query_shavar_file_with_u_value(self):
        url = "https://shavar.stage.mozaws.net/downloads?appver=86.0&pver=2.2"
        payload = "base-fingerprinting-track-digest256;"

        res = requests.post(url, payload)
        print(res.text)
        data = res.text
        return data

    def process_data_to_get_new_url(self, u_value):
        with open(tmp.name, 'w') as f:
            try:
                f.write(u_value)
            except:
                print("Error writing u value to file")

        with open(tmp.name) as file:
            try:
                rows = (line.split(':') for line in file)
                dict = {row[0]: row[1] for row in rows}
            except:
                print("Error formatting u value")

        append_str = '.json'
        new_string = dict["u"].strip("\n")
        new_url = "http://" + new_string + append_str
        print(new_url)
        return new_url

    def get_list_json_format(self, new_url):
        res = requests.get(new_url)
        new_list = res.json()
        new_list_str = str(new_list["domains"])
        new_list_quotes = new_list_str.replace("'", '"').replace(",", ",\n").replace("[", "[\n ").replace("]", "\n]")
        print(new_list_quotes)

        with open("./content-blocker/tmp.json", 'w') as f:
            try:
                f.write(new_list_quotes)
            except:
                ("Error creating json file")

    def compare_file(self, file1, file2):

        json1 = json.load(open(ORIGINAL_SHAVAR_FILE, "r"))
        json2 = json.load(open(TMP_SHAVAR_FILE, "r"))

        file_1 = json.dumps(json1, sort_keys=True)
        file_2 = json.dumps(json2, sort_keys=True)

        if (file_1 != file_2):
            shutil.move('PATH_TO_FILES/tmp.json', 'PATH_TO_FILES/base-fingerprinting-track.json')
            print("content blocker file changed")
        else:
            os.remove('./content-blocker/tmp.json')
            print("No changes in shavar list")


def main():
    s = Shavar()
    u_value = s.query_shavar_file_with_u_value()
    new_url = s.process_data_to_get_new_url(u_value)
    s.get_list_json_format(new_url)
    s.compare_file(ORIGINAL_SHAVAR_FILE, TMP_SHAVAR_FILE)


if __name__ == '__main__':
    main()
