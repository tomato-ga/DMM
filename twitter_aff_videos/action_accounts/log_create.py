import logging

def getMyLogger(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('/home/don/py/DMM/twitter_aff_videos/action_accounts/testlog.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger