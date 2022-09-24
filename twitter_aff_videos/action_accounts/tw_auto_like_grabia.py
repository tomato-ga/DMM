import API_duga_vvdashvv
import API_config_ggg
import API_config_gidolso

import tw_package
from record_log import getMyLogger
import datetime


today = datetime.datetime.now()
logger = getMyLogger(str(today)+"autolike")
logger.info(f"Goスタート")

max_like_count = 2 #最大RT / Like数
try:

    tw_package.My_rt_like_matchcase(API=API_config_ggg, ids=API_config_ggg.ids, max_rt_like_count=max_like_count)
    tw_package.My_rt_like_matchcase(API=API_config_gidolso, ids=API_config_gidolso.ids, max_rt_like_count=max_like_count)
    tw_package.My_rt_like_matchcase(API=API_duga_vvdashvv, ids=API_duga_vvdashvv.ids, max_rt_like_count=max_like_count)

except Exception as e:
    logger.exception(e)
    pass

