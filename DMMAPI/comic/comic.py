import requests

end_point = 'https://api.dmm.com/affiliate/v3/ItemList'
api = 'b7fkZaG3pW6ZZHpGBbLz'
params ={
	"api_id":       "b7fkZaG3pW6ZZHpGBbLz",
	"affiliate_id": "kamipanmen-990",
	"output":       "json",
    "hits": 80,
    "site": "DMM.com",
    "service": "ebook",
    "floor": "comic",
    }


r = requests.get(end_point, params=params)
print(r.json())


rr = r.json()
print(rr)