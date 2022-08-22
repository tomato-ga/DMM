import API_config_yukarin
import api_tomorrow_genkio
import api_togsi7
import api_1j_mc
import api_OtxSf
import api_popo5ppo
import api_tsuma
import api_jd
import api_after2000
import api_ranko
import API_config_seihuku
import API_config_gal
import API_config_pp_psan

import tw_package
from record_log import getMyLogger
import datetime


today = datetime.datetime.now()
logger = getMyLogger(str(today)+"autolike")
logger.info(f"Goスタート")

max_like_count = 1 #最大RT数
try:
    tw_package.My_like(API=API_config_yukarin, ids=API_config_yukarin.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_tomorrow_genkio, ids=api_tomorrow_genkio.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_togsi7, ids=api_togsi7.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_1j_mc, ids=api_1j_mc.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_OtxSf, ids=api_OtxSf.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_popo5ppo, ids=api_popo5ppo.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_tsuma, ids=api_tsuma.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_jd, ids=api_jd.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_after2000, ids=API_config_yukarin.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=api_ranko, ids=API_config_yukarin.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=API_config_seihuku, ids=API_config_yukarin.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=API_config_gal, ids=API_config_yukarin.ids, max_rt_like_count=max_like_count)
    tw_package.My_like(API=API_config_pp_psan, ids=API_config_yukarin.ids, max_rt_like_count=max_like_count)
except Exception as e:
    logger.exception(e)
    pass
