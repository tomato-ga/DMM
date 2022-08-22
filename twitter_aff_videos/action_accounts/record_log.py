import logging

def getMyLogger(name):
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(f'/home/don/py/DMM/twitter_aff_videos/action_accounts/log/{name}.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger