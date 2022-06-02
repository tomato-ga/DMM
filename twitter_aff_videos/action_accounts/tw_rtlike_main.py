import tw_package
import api_tomorrow_genkio
import api_1j_mc
import api_togsi7
import api_HjQhq
import api_OtxSf # RT設定しない


"""
1.API読み込み
2.APIモジュールにいいねRTするidを記載して読み込み
3. max_rt_countで最大いいね数とRT数を入れる
"""

max_rt_count = 2

tw_package.My_rt(API=api_HjQhq, ids=api_HjQhq.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_1j_mc, ids=api_1j_mc.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_togsi7, ids=api_togsi7.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_OtxSf, ids=api_OtxSf.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_tomorrow_genkio, ids=api_tomorrow_genkio.ids, max_rt_count=max_rt_count)

"""履歴
2022/05/10 21:02
他人のツイートのRTやめる

2022/05/26 19:49
OtxでRT実施
エロアカであやのRTといいね実施

2022/06/02 19:00
エロアカであや・ゆかり（いいね・RT）・グラビア太郎（いいね）の実施

"""