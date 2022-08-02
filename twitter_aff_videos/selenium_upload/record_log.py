import logging

def getMyLogger(name):
    logging.basicConfig(level=logging.WARNING)

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(f'/home/don/py/DMM/twitter_aff_videos/selenium_upload/log/{name}.log')
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger