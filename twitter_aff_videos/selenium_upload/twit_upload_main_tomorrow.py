from master_twit_upload_module_0510 import Tweet
import create_log
import sys

logger = create_log.get_logger(__name__, 'log.txt')
logger.debug('ロギングスタート')


if __name__ == '__main__':

    try:
        i = Tweet()
        i.Uploads(account='tomorrow_genkio', text='この動画を特定したぞ→')
        i.Quit()
    except:
        logger.exception(sys.exc_info())
