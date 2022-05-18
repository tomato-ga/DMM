from ast import keyword
import dmm

api_id = 'b7fkZaG3pW6ZZHpGBbLz'
affiliate_id = 'kamipanmen-990'

# インスタンスを作成
dmm = dmm.API(api_id=api_id, affiliate_id=affiliate_id)

# 商品検索
#items = item_search = api.item_search(site="FANZA", hits=3, keyword="巨乳")

# gte_bust = 80 #バスト何cm以上の情報を収集するか
# lte_bust = 84 #バスト何cm以下の情報を収集するか
# res = api.actress_search(gte_bust=gte_bust,
# lte_bust=lte_bust,
# hits = 100, # 1回のリクエストで入手できる情報最大で100件
# offset = 1, #データベースの何番から情報を取るか。hits=100なら次は101に設定しよう
# sort = "bust",
# output="json")

items = dmm.search('ItemList', keyword='六本木', hits=9)

for i in items['result']:
    cid = i.get('content_id')
    dmm.video_download(cid)

# フロア一覧
floor_list = api.floor_list()

# 女優検索
actress_search = api.actress_search()

# ジャンル検索
genre_search = api.genre_search(floor_id=91)

# メーカー検索
maker_search = api.maker_search(floor_id=91)

# シリーズ検索
series_search = api.series_search(floor_id=91)

# 作者検索
author = api.author_search(floor_id=72)
