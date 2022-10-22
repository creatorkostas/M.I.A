if __name__ == "__main__":
    try:
        import logging
        #---------------------------------     LOGGING INFO    ------------------------------
        logging.basicConfig(filename="logs/start.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
        logger=logging.getLogger()
        console = logging.StreamHandler()
        logging_level = logging.DEBUG
        logger.setLevel(logging_level)
        logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
        logging.getLogger('comtypes').setLevel(logging.INFO)
        logging.getLogger('comtypes.client').setLevel(logging.INFO)
        logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
        logging.getLogger('chatterbot.chatterbot').setLevel(logging.WARNING)

        if logging_level == 10:
            logger.addHandler(console)
        #---------------------------------     LOGGING INFO END   ------------------------------

        from security.login import login
    
        import assistant
        import ctypes
        import os
        #Loading Settings
        import json
        jsonFile = open('data/settings.json', 'r')
        settings = json.load(jsonFile)
        jsonFile.close()
        
        #Cheking Os UpTime
        
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])
        mins, sec = divmod(t, 60)
        
        if settings["core"][0]["start_in_startup"] == 0 and mins < 1 and sec < 30:
            exit()
        
        try:
            check_update = settings["core"][0]["check_for_updates_in_start"]
            if check_update == 1:
                from updater.updater import check_for_update
                if check_for_update():
                    os.start("updater\\updater.py")
                    exit()
        except Exception as e:
            print("[ERROR] Error while tring to check for update")
            logger.error("[ERROR] Error while tring to check for update: "+str(e))
        
        
            
        #Unlock Security Folder
        
        if os.path.exists("lock.7z"):
            from lock import lock
            lock_pass = str(input("Unlock Pass --> "))
            lock.unlock_MIA(lock_pass)
        
        fspass, isadmin, username, connected_to_the_internet = login(logger)
        online_ai = connected_to_the_internet

        if fspass == False:
            logger.warning("[SECURITY] Someone tried to baypass the security layer")
            print("You did not pass the first security layer! \nStopping...")
            sys.exit()
        elif fspass == True and (isadmin == True or isadmin == False):
            print("You have logged in!")
            ai_v_l = input("what ai version to load? [l(lite)/f(full)/n(none)]")
            if ai_v_l == "l":
                logger.info("[INFO] Loading MIA ai bot lite version (not realy just does not save the conversation)")
                ai_v_l = "l"
            elif ai_v_l == "f":
                logger.info("[INFO] Loading MIA ai bot full version")
                ai_v_l = "f"
            else:
                logger.info("[INFO] Skiping loading MIA ai bot")
                ai_v_l = "n"

            logging.basicConfig(filename="logs/MIA.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
            logger=logging.getLogger()
            console = logging.StreamHandler()
            
            
                
            assistant.MIA_assistant(ai_v_l, username, isadmin, logger, console, "v", 101, online_ai) #the second from the end is the command_input [command_input = input("command input [v(voise)/k(keyboard)]")]
            #the last is speak_engine_volume if it is 101 is the default volume else set to the given value
            try:
                del fspass, isadmin, username
            except: 
                pass
                
    except KeyboardInterrupt as e:
        print("Exitting...")
        logger.info("[INFO] Keyboard Interrupt by the user")
        
    '''except Exception as e:
        logger.critical("[CRITICAL] Critical ERROR! error: "+str(e))
        print("Critical ERROR!\nExitting...")
        print(str(e))
    '''