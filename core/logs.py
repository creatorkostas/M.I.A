def logs(logs_path = "logs/log.log", log_level = "INFO"):
    import logging
    #---------------------------------     LOGGING INFO    ------------------------------
    logging.basicConfig(filename="logs/login.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
    #logging.basicConfig()
    logger=logging.getLogger()
    console = logging.StreamHandler()
    #logger.addHandler(console)
    if log_level == "INFO":
        logging_level = logging.INFO
    elif log_level == "DEBUG":
        logging_level = logging.DEBUG
        
    logger.setLevel(logging_level)
    logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
    logging.getLogger('comtypes').setLevel(logging.INFO)
    logging.getLogger('comtypes.client').setLevel(logging.INFO)
    logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
    logging.getLogger('chatterbot.chatterbot').setLevel(logging.WARNING)
    #---------------------------------     LOGGING INFO END   ------------------------------
    
    return logging,logger