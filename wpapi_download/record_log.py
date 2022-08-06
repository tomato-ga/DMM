import logging
import datetime

today = datetime.datetime.now()

def getMyLogger(today):
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(today)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(f'/home/don/py/DMM/wpapi_download/log/{today}_mizugazo.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger