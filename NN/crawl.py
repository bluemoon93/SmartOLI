import urllib.request
from urllib.request import Request, urlopen
import requests
import shutil

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
cookies = {'dismiss_warning': '1'}

for page in range(1, 100):
    print("Loading http://sharemyshit.com/?order=new&page_num="+str(page))

    mybytes = requests.get("http://sharemyshit.com/?order=new&page_num="+str(page), headers=headers, cookies=cookies)
    mystr = mybytes.text

    #print(mystr)
    for line in mystr.split("\""):
        if "jpeg" in line:
            print(line)

            response = requests.get(line, headers=headers, cookies=cookies, stream=True)
            with open("dataset/"+line.split("/")[-1], 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response  