from master_twit_upload_module_0510 import Tweet

if __name__ == '__main__':

    try:
        i = Tweet()
        i.Uploads(account='tomorrow_genkio', text='この動画を特定したぞ→')
        i.Quit()
    except:
        logger.exception(sys.exc_info())
