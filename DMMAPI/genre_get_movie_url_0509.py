import os
import json
from re import search
from socket import if_nameindex
from unicodedata import name
import requests
import pprint
from box import Box
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class Genre_dmm:

    APIID: str = ''
    AFFILIATEID: str = ''
    keyword: str = ''

    # floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

    #pprint.pprint(Box.from_json(floor.text))
    # json_box = Box.from_json(floor.text)
    # print(json_box)


    @property
    def search_keyword(self):

        search_keyword_response = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={self.APIID}&affiliate_id={self.AFFILIATEID}&site=FANZA&service=digital&floor=videoa&hits=20&sort=rank&keyword={self.keyword}&output=json')
        search_json_box =Box.from_json(search_keyword_response.text)
        
        
        items = [i.items for i in search_json_box.result['items']]
    
        pprint.pprint(items)

if __name__ == '__main__':

    g = Genre_dmm()
    g.APIID = 'b7fkZaG3pW6ZZHpGBbLz'
    g.AFFILIATEID = 'kamipanmen-990'
    g.keyword= 'メンズエステ' # 不要→ keyword.encode('utf-8')

    g.search_keyword