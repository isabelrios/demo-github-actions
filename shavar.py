import os, json
import requests
import shutil


FILE = 'test.json'

class Shavar:

    def __init__(self):
        # if set in init, it starts by doing this, no need to call in main, use one or the other
        self.query_download_file()
        pass
    
    def query_download_file(self):
        url = "https://tools.learningcontainer.com/sample-json.json"

        res = requests.get(url)
        print(res.text)

        open("tmp.json", "wb").write(res.content)


    def compare_file(self, file1, file2):

        json1 = json.load(open("./test.json", "r"))
        json2 = json.load(open("./tmp.json", "r"))

        file_1 = json.dumps(json1, sort_keys=True)
        file_2 = json.dumps(json2, sort_keys=True)
        
        if (file_1 != file_2): 
            shutil.move('tmp.json', 'test.json')
            print("test.json file changed")
        else:
            os.remove('tmp.json')
            print("No changes, remove temporary file created")


s = Shavar()
#s.query_download_file()
s.compare_file("tmp.json", FILE)



'''
def main():
    s=Shavar()
    s.query_download_file()


if __name__ == '__main__':
    main()
'''
