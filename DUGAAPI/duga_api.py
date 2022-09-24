from dataclasses import dataclass
from re import search
import requests
import json
from datetime import datetime, date, timedelta
import pymongo


@dataclass
class Duga:

    api_domain = ''
    api_id = ''
    agent_id = ''
    version = "1.2"
    hits = 0
    adult = 0
    category = 0
    offset = 0
    sort = ""
    bannerid = ""
    openstt = ""
    openend = ""
    index_today = ""


    def searchKeyword(self, keyword):
        url = f"{self.api_domain}?version={self.version}&appid={self.api_id}&agentid={self.agent_id}&keyword={keyword}&hits={self.hits}&bannerid=01&format=json&adult={self.rating}&sort=favorite"
        response: json = requests.get(url)
        return response


    def category_search(self):
        url = f"{self.api_domain}?version={self.version}&appid={self.api_id}&agentid={self.agent_id}&category={self.category}&hits={self.hits}&bannerid=01&format=json&adult={self.rating}&sort=favorite&offset={self.offset}"
        response: json = requests.get(url)
        return response


    def searchCategory(self, category):
        api_domain = self.api_domain
        api_id = self.api_id
        agentid = self.agentid
        version = self.version
        hits = self.hits

        url = "{0}?version={1}&appid={2}&agentid={3}&category={4}&hits={5}&bannerid=01&format=json&adult=1&sort=favorite".format(api_domain,version,api_id,agentid,category,hits)
        response = requests.get(url)
        return response

    def getRanking(self):

        params = {
        "api_domain": self.api_domain,
        "appid" : self.api_id,
        "agentid":  self.agent_id,
        "version": self.version,
        "hits": self.hits,
        "sort": self.sort,
        "format": "json",
        "bannerid": self.bannerid,
        "adult": self.adult,
        "category": self.category,
        "openstt": self.openstt,
        "openend": self.openend,
        }

        response = requests.get(url=self.api_domain, params=params)
        r = response.json()


        for i, x in enumerate(r['items']):

            try:
                yield dict(
                    title = x["item"]['title'],
                    actor = x["item"]["performer"][0]["data"]["name"],
                    video_embed_url = x["item"]['samplemovie'][0]['midium']['movie'],
                    aff_url =  x["item"]['affiliateurl'],
                    dates = x["item"]['opendate'],
                    price = x["item"]['price'],
                    index=self.index_today + "_" + str(i))
            except:
                pass

    def DugaDownload(self, r_json):
        r_json = r_json

        video_response = requests.get(r_json["video_embed_url"])
        with open(fr"/mnt/hdd/don/files/duga/{r_json['index']}.mp4", "wb") as save_video:
            save_video.write(video_response.content)


duga = Duga()
duga.api_domain = "http://affapi.duga.jp/search"
duga.api_id = "sRMJzpZCoB8bFa94ZZko"
duga.agent_id = "42370"
duga.hits = 100
duga.adult = 1  # アダルト1 一般0
duga.category = 12  # アダルト > アイドル
duga.sort =  "favorite"
duga.bannerid = "01"

today = datetime.now()
today_str = today.strftime("%Y%m%d")
oneweek =  today - timedelta(days=7)
oneweek = oneweek.strftime("%Y%m%d")

duga.openstt = oneweek
duga.openend = today_str

index_today = datetime.now().replace(microsecond=0).strftime("%Y%m%d")
duga.index_today = index_today


db_url = 'mongodb://pyton:radioipad1215@192.168.0.25:27017'
client = pymongo.MongoClient(db_url)
db = client.twitter
collection = db.duga


for video_info in duga.getRanking():
    duga.DugaDownload(video_info)
    collection.insert_one(video_info)
