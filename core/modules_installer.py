def install_missing_module(e,modules_names=[]):
    import os 
    cwd = os.getcwd()
    os.chdir("..")
    
    import logging
    from core.cprint import cprint
    import data.print_colors as pcolors
    
    
    logging.basicConfig(filename="logs/modules_installer.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.ERROR)
    os.chdir(cwd)
    
    if 'No module named' in str(e):
        e = str(e).split(" ")
        module_to_intall = e[-1].replace("'","")
        module_to_intall = module_to_intall.replace('"','')
        try:
            cprint("[INFO] Trying to install: "+module_to_intall, pcolors.WARNING)
            logger.info("[INFO] Trying to install: "+module_to_intall)
            import pip
            if hasattr(pip, 'main'):
                pip.main(['install', module_to_intall])
            else:
                pip._internal.main(['install', module_to_intall])
        except Exception as e:
            cprint("[ERROR] Critical Error while tring to install module: "+module_to_intall+"\n", pcolors.FAIL)
            logger.error("[ERROR] Critical Error while tring to install module: "+module_to_intall)
            logger.error("[ERROR] Error: "+str(e))
            cprint("[ERROR] Error: "+str(e)+"\n\n", pcolors.FAIL)
            try:
                cprint("[INFO] Trying to install all modules\n", pcolors.WARNING)
                logger.info("[INFO] Trying to install all modules from the list")
                
                for module_name in modules_names:
                    try:
                        if hasattr(pip, 'main'):
                            pip.main(['install', module_name])
                        else:
                            pip._internal.main(['install', module_name])
                    except Exception as e:
                        cprint("[ERROR] Critical Error while tring to install module: "+module_to_intall+"\n", pcolors.FAIL)
                        logger.error("[ERROR] Critical Error while tring to install module: "+module_to_intall)
                        logger.error("[ERROR] Error: "+str(e))
                        cprint("[ERROR] Error: "+str(e)+"\n\n", pcolors.FAIL)
            except Exception as e:
                cprint("[ERROR] Critical Error while tring to install module: "+module_to_intall+"\n", pcolors.FAIL)
                logger.error("[ERROR] Critical Error while tring to install module: "+module_to_intall)
                logger.error("[ERROR] Error: "+str(e))
                cprint("[ERROR] Error: "+str(e)+"\n\n", pcolors.FAIL)
                exit()
    else:   
        logger.error("[ERROR] Error: "+str(e))
        cprint("[ERROR] Error: "+str(e), pcolors.FAIL)
        exit()
        
    try:
        del logger
        del logging
        del cprint
        del pcolors
        del e
    except:
        pass