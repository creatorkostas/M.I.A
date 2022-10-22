def login(logger):
    try:
        import os
        os.chdir(".")
        from core.modules_installer import install_missing_module
        from security.security_layers import securitylayers
        
        #from security.firewall.monitor import start_monitoring
        import hashlib
        
        #from core.logs import logs
        #logging,logger = logs("logs/login.log", "INFO")
        

        #---------------------------------     LOGGING INFO    ------------------------------
        #logging.basicConfig(filename="logs/login.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')

        #---------------------------------     LOGGING INFO END   ------------------------------
        
        import platform
        import getpass
        
    except Exception as e:
        #print(str(e))
        install_missing_module(e,[])

    #Test messages
    #logger.debug("[DEBUG] Harmless debug Message")
    #logger.info("[INFO] Just an information")
    #logger.warning("[WARNING] Its a Warning")
    #logger.warning("[SECURITY] Its a Security Warning")
    #logger.error("[ERROR] Its an Error (π.χ. Did you try to divide by zero)")
    #logger.critical("[CRITICAL] Internet is down")

    try:
        securityLayers = securitylayers()
        os_user_name = getpass.getuser()
        os_name = platform.system()
        logger.info("[INFO] MIA starting in: "+os_name+" with os user name: "+os_user_name)
        del platform
        del getpass
        
        connected_to_the_internet = securityLayers.check_internet_connection(logger)
        username = input("Username: ")
        password = hashlib.sha512(input("Password: ").encode('utf-8')).hexdigest()
        logger.info("[INFO] user: "+username+ " tring to log in with pass: "+password)
        
        #-------------------------------------------------------------------------------------------------------------
        lines = [[],[]]
        users=['']
        k=0
        with open("security\\trusted.txt","r") as file:
            users = file.read()
            
            users = users.split("---")
            #print(users)
            for i in users:
                if i != '':
                    #print(i.split("\n"))
                    lines[k] = i.split("\n")
                    k+=1
        #print("\n\n---------------------------------\n"+str(lines)+"\n---------------------------------\n\n")
        #TODO review this part
        done = False
        for user in users:
            if user != "":
                line = user.split("\n")
                line4 = line[4].split(",")
                if connected_to_the_internet and securityLayers.gather_data() in line4: 
                    #Check if is a trusted user
                    if username == line[0] and password == line[1] and os_user_name == line[2] and os_name == line[3]:
                        fspass = True
                        isadmin = securityLayers.check_if_in_admin_list(username,password)
                        done = True
                else:
                    fspass, isadmin = securityLayers.first_security_layer(username, password, connected_to_the_internet,logger)
                    done = True
            else:
                fspass, isadmin = securityLayers.first_security_layer(username, password, connected_to_the_internet,logger)
                done = True
                
                if done:
                    break
        #-------------------------------------------------------------------------------------------------------------
        
        try:
            del password
        except:
            pass
            
        return fspass, isadmin, username, connected_to_the_internet
        
        
    except KeyboardInterrupt as e:
        print("Exitting...")
        logger.info("[INFO] Keyboard Interrupt by the user")