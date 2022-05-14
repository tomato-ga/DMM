from dataclasses import dataclass
from re import search
import requests
import json


@dataclass
class Duga:

    def __init__(self):
        self.api_domain = ''
        self.api_id = ''
        self.agent_id = ''
        self.version = "1.2"
        self.hits = 0
        self.rating = 0
        self.category = 0
        self.offset = 0

    def searchKeyword(self, keyword):
        url = f"{self.api_domain}?version={self.version}&appid={self.api_id}&agentid={self.agent_id}&keyword={keyword}&hits={self.hits}&bannerid=01&format=json&adult={self.rating}&sort=favorite"
        response: json = requests.get(url)
        return response


    # TODO forでoffset増やしながら取得 DMM横展開
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

    def getSort(self, sort):
        api_domain = self.api_domain
        api_id = self.api_id
        agentid = self.agentid
        version = self.version
        hits = self.hits
        url = "{0}?version={1}&appid={2}&agentid={3}&hits={4}&sort={5}&bannerid=01&format=json&adult=1&sort=favorite".format(api_domain,version,api_id,agentid,hits,sort)
        response = requests.get(url)
        return response


duga = Duga()
duga.api_domain = "http://affapi.duga.jp/search"
duga.api_id = "8HQYQ9RvZRJ2CyztK0Hw"
duga.agent_id = "35841"
duga.hits = 100
duga.rating = 1  # アダルト1 一般0
duga.category = 12  # アダルト > アイドル


res = duga.category_search()
searchkey = json.loads(res.text)
print(searchkey)
