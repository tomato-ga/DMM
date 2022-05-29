import tw_package
import api_tomorrow_genkio
import api_1j_mc
import api_togsi7
import api_HjQhq
import api_OtxSf # RT設定しない

#メインアカはRTしない
# tw_package.Thirdparty_rt(api_tomorrow_genkio)
# tw_package.My_rt(api_tomorrow_genkio, api_tomorrow_genkio.ids)

#tw_package.Thirdparty_rt(api_1j_mc)
max_rt_count = 1

tw_package.My_rt(API=api_HjQhq, ids=api_HjQhq.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_1j_mc, ids=api_1j_mc.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_togsi7, ids=api_togsi7.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_OtxSf, ids=api_OtxSf.ids, max_rt_count=max_rt_count)

tw_package.My_rt(API=api_tomorrow_genkio, ids=api_tomorrow_genkio.ids, max_rt_count=max_rt_count)

"""_summary_
2022/05/10 21:02
他人のツイートのRTやめる

2022/05/26 19:49
OtxでRT実施
エロアカであやのRTといいね実施

"""