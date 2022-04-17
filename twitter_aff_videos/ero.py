import re
import requests
from bs4 import BeautifulSoup

# APIのレスポンスで返されたサンプルビデオのURL
r = requests.get('https://www.dmm.co.jp/litevideo/-/part/=/cid=atkd298/size=720_480/')
soup = BeautifulSoup(r.text, 'html.parser')
find_src = soup.find("iframe", allow="autoplay").get("src")
tcid = re.findall("cid=(.*)/mtype", find_src)[0]
video_url = "http://cc3001.dmm.co.jp/litevideo/freepv/{}/{}/{}/{}_sm_w.mp4".format(tcid[:1], tcid[:3], tcid, tcid)
response = requests.get(video_url)
with open(r'E:\Dropbox\Download\test.mp4', 'wb') as saveFile:
    saveFile.write(response.content)
