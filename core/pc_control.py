def change_wallpaper(logger,os,random,ctypes,username):
    import json
    #path_parent = os.path.dirname(os.getcwd())
    #os.chdir(path_parent)
    
    logger.info("[INFO] Loading wallpaper path")
    jsonFile = open('data/settings.json', 'r')
    settings = json.load(jsonFile)
    wallpapers_path = settings["users"][username]["paths"][0]["wallpapers"]
    jsonFile.close()
    del jsonFile, settings, json

    logger.info("[INFO] Changing wallpaper")
    entries = os.listdir(wallpapers_path)
    wall = entries[random.randint(0,len(entries))]
    full_wallpaper_path = wallpapers_path + wall
    logger.info("[INFO] New wallpaper: "+ full_wallpaper_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, full_wallpaper_path , 0)

def shutdown(logger,speak,subprocess):
    print("Ok , your pc will not turn off")
    logger.info("[INFO] Cancel Pc Shutdown")
    speak("Ok , your pc will not turn off")
    subprocess.call(["shutdown", "/l"])