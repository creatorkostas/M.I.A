def MIA_assistant(bot_v, username, isadmin, logger, console, command_input, speak_engine_volume, online_ai):

    from core.modules_installer import install_missing_module
    try:
        import data.print_colors as pcolors
        from core.cprint import cprint
        import data.parameters as par
        from core.speak_engine import load_speak_engine
        from core.MIA_ai import load_MIA_bot, load_MIA_brain
        from core.weather import w
        from core.open import open_function
        from core.external_modules.count_lines_of_code import clof
        from core.music import music
        from core.get_info import ask, wiki
        from core.pc_control import change_wallpaper, shutdown
        from core.notes import new_note, del_note, edit_note, read_notes
        from core.emailer import gmail_send_message as emailer
        import core.volume_control as vc
        import speech_recognition as sr
        import pyttsx3
        import datetime
        import wikipedia
        import webbrowser
        import os
        import pyautogui
        import random
        import ctypes
        import time
        import subprocess
        from ecapture import ecapture as ec
        import wolframalpha
        import json
        import requests
        from youtube_search import YoutubeSearch
        import vlc
        import pafy
        from bs4 import BeautifulSoup as soup
        from urllib.request import urlopen
        from chatterbot import ChatBot
        from core.google_assistant.pushtotalk import main as g_assistant
        from core.google_assistant.assistant import TextAssistant
        from dotenv import load_dotenv

        
        
        #------- Volume Control Imports
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        #------------------------------

    except Exception as e:
        cprint("[CRITICAL] Critical Error while tring to load modules: "+str(e), pcolors.FAIL)
        logger.critical("[CRITICAL] Critical Error while tring to load modules: "+str(e))
        install_missing_module(e,["wikipedia"])

    #cprint("Loading your AI personal assistant MIA", pcolors.OKGREEN)
    #speak("Loading your AI personal assistant MIA")
    
    logger.info("[INFO] Starting MIA Assistant")
    cprint("Starting MIA Assistant...", pcolors.OKCYAN,["OK",pcolors.OKGREEN],0.01)

    #Loading MIA environment variables
    logger.info("[INFO] Loading MIA environment variables")
    cprint("Loading MIA environment variables...", pcolors.OKCYAN,["OK",pcolors.OKGREEN],0.01)
    load_dotenv()

    letter_letter_print_time = float(os.getenv("LETTER_LETTER_PRINT_TIME"))

    #loading settings
    logger.info("[INFO] Loading MIA settings")
    cprint("Loading MIA settings...", pcolors.OKCYAN,["OK",pcolors.OKGREEN],letter_letter_print_time)
    jsonFile = open('data/settings.json', 'r')
    settings = json.load(jsonFile)
    sleep_wait_time = settings["core"][0]["sleep_time"]
    jsonFile.close()
    
    
    
    logger.info("[INFO] Loading MIA Assistant AI")
    
    cprint("Loading MIA Brain...", pcolors.OKCYAN,["OK",pcolors.OKGREEN],letter_letter_print_time)
    MIA_brain = load_MIA_brain(ChatBot,logger, "f")
    
    cprint("Loading MIA chat bot...", pcolors.OKCYAN,["OK",pcolors.OKGREEN],letter_letter_print_time)
    if bot_v == "n":
        logger.info("[INFO] MIA_Assistant_v0.0.1 started without the AI bot")
    else:
        MIA = load_MIA_bot(ChatBot,logger, bot_v,online_ai)

    logger.info("[INFO] Loading Speak Engine")
    cprint("Loading Speak Engine...", pcolors.OKCYAN,["OK",pcolors.OKGREEN],letter_letter_print_time)
    
    #---------- Volume Control Virables --------------
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #-------------------------------------------------
    
    if int(speak_engine_volume) > 0:
        #from core.speak_engine import speak
        
        engine = load_speak_engine(pyttsx3,online_ai,os.getenv('CARTER_KEY'))
        
        if speak_engine_volume != 101:
            engine.setProperty('volume', speak_engine_volume)
            
        #cprint("Starting!", pcolors.OKCYAN)
        engine.say("Starting!")
        engine.runAndWait()
        
        def speak(text):
            engine.say(text)
            engine.runAndWait()
    else:
        def speak(text):
            cprint(text, pcolors.CBLINK)

    def wishMe():
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            speak("Hello,Good Morning "+username)
            cprint("Hello,Good Morning "+username)
        elif hour>=12 and hour<19:
            speak("Hello,Good Afternoon "+username)
            cprint("Hello,Good Afternoon "+username)
        else:
            speak("Hello,Good Evening "+username)
            cprint("Hello,Good Evening "+username)

    
    def takeCommand_v(): #takeCommand_v():
        #speak("Tell me how can I help you?")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            cprint("Listening...","")
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio=r.listen(source)
            
            
            try:
                cprint("Listening...")
                statement=r.recognize_google(audio).lower()
                cprint('user said: ' +statement + '\n')
                
            except Exception as e:
                #speak("Pardon me, please say that again")
                return 0
            return statement
            
            
    def takeCommand_k():
        statement = input("--> ")
        return statement
    
    
    if command_input == "v":
        takeCommand = takeCommand_v
    elif command_input == "k":
        takeCommand = takeCommand_k
    else:
        logger.critical("[Critical] No valid command input provided")
        exit()
    
    logger.info("[INFO] Loading Google Assistant")
    cprint("Loading Google Assistant!", pcolors.OKCYAN)
    try:
        assist = TextAssistant(os.getenv('DEVICE_MODEL_ID'),os.getenv('DEVICE_ID')) #oi metablites gia auto to object einai temp
        google_assistant_ok = True
    except Exception as e:
        google_assistant_ok = False
        logger.warning("[WARNING] Loading Google Assistant Faild with error: "+str(e))
        cprint("Google Assistant faild to load", pcolors.ERROR)
    
    wishMe()

    if bot_v == "l" or bot_v == "f" or bot_v == "n":


        while True:
            try:
                statement = str(takeCommand()).lower()
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                cprint(str(e), pcolors.FAIL)
                #pass
                
            #if statement==0:
            #    continue
            if "assistant" in statement:
                if google_assistant_ok:
                    assist.main(statement)
                else:
                    cprint("Google Assistant has not load successfully", pcolors.INFO)
                
            elif statement != "" and statement != 0 and statement != "0":# and "mia" in statement:
                statement = statement.replace("mia ","")
                brain_statement = str(MIA_brain.get_response(statement))
                cprint(brain_statement, pcolors.WARNING)

                if  brain_statement == "exit": #any(i in statement for i in par.exit):
                    logger.info("[INFO] MIA stoping...")
                    cprint('Initiating shutdown protocol', pcolors.WARNING)
                    speak('Initiating shutdown protocol')
                    from lock import lock
                    lock_pass = str(input("Lock Pass --> "))
                    lock.lock_MIA(lock_pass)
                    if speak_engine_volume != 0: 
                        engine.setProperty('rate', '2')
                    speak('Goodbay Sir')
                    exit()
                    
                elif "change speak engine" in statement:
                    engine = load_speak_engine(pyttsx3,not online_ai)
                    
                elif "change input device" in statement:
                    if command_input == "k":
                        takeCommand = takeCommand_v
                    else:
                        takeCommand = takeCommand_k
                    
                elif "volume" in statement:
                    if "volume control" in statement:
                        vc.volume_control.control()
                    if "by" in statement:
                        volume_num = statement.split("by")
                        volume_num = int(volume_num[1].replace(" ",""))
                    else:
                        volume_num = 3
                        
                    if "increase volume" in statement:
                        volume_audio = volume.GetMasterVolumeLevel()+volume_num
                        volume.SetMasterVolumeLevel(volume_audio, None)
                    elif "decrease volume" in statement:
                        volume_audio = volume.GetMasterVolumeLevel()-volume_num
                        volume.SetMasterVolumeLevel(volume_audio, None)

                elif brain_statement == "wallpaper": #any(i in statement for i in par.wallpaper):
                    change_wallpaper(logger,os,random,ctypes,username)

                elif brain_statement == "funs": #any(i in statement for i in par.funs):
                    logger.info("[INFO] Telling a joke")
                    res = requests.get('https://icanhazdadjoke.com/', headers={"Accept":"application/json"})
                    if res.status_code == requests.codes.ok:
                        speak(str(res.json()['joke']))
                    else:
                        speak('oops!I ran out of jokes')

                elif brain_statement == "info": #any(i in statement for i in par.info):
                    wiki(speak,logger,statement,wikipedia)

                elif brain_statement == "opens": #any(i in statement for i in par.opens):
                    programs_name = par.programs_name
                    programs_path = par.programs_path
                    open_function(logger, speak, statement, time, webbrowser, sleep_wait_time, os, programs_name, programs_path)
                
                elif brain_statement == "time": #any(i in statement for i in par.time):
                    logger.info("[INFO] Telling the time")
                    strTime=datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"the time is {strTime}")
                 
                elif brain_statement == "news": #any(i in statement for i in par.news):
                    try:
                        logger.info("[INFO] Reading the news")
                        Client=urlopen("https://news.google.com/news/rss")
                        xml_page=Client.read()
                        Client.close()
                        soup_page=soup(xml_page,"xml")
                        news_list=soup_page.findAll("item")
                        for news in news_list[:1]:
                            speak(news.title.text.encode('utf-8'))
                    except Exception as e:
                            logger.error("[ERROR] Error while tring to read the news")
                            cprint(e, pcolors.FAIL)
                    try:
                        del Client, xml_page, soup_page, news_list
                    except:
                        pass

                elif 'play' in statement:
                    #to play music
                    if "by name" in statement:
                        player = music(logger,pafy,vlc,YoutubeSearch,speak)
                        player.play_by_input_name()
                    else:
                        player = music(logger,pafy,vlc,YoutubeSearch,speak)
                        player.play(statement)

                elif "music" in statement:
                    #to control th music
                    player.control_player(statement)

                elif brain_statement == "cam_capture": #any(i in statement for i in par.cam_capture):
                    logger.info("[INFO] Photo capture from camera")
                    ec.capture(1,False, settings["users"][username]["paths"][0]["pictures"]+"camera_user_"+datetime.datetime.now().strftime("(%m-%d-%Y)-(%H-%M-%S)"))
                
                elif brain_statement == "scr_capture": #any(i in statement for i in par.scr_capture):
                    logger.info("[INFO] Screenshot capture")
                    myScreenshot = pyautogui.screenshot()
                    ttime=datetime.datetime.now().strftime("(%m-%d-%Y)-(%H-%M-%S)")
                    myScreenshot.save(settings["users"][username]["paths"][0]["pictures"]+"screenshot_"+username+"_"+ttime+".jpg")
                    del ttime
                    del myScreenshot

                elif brain_statement == "search": #any(i in statement for i in par.search):
                    if "search for" in statement:
                        statement = statement.replace("search for", "")
                    else:
                        statement = statement.replace("search", "")
                    logger.info("[INFO] Internet Search for: "+statement)
                    webbrowser.open_new_tab("https://www.google.com/search?client=firefox-b-d&q="+statement)
                    time.sleep(sleep_wait_time)

                elif brain_statement == "ask": #any(i in statement for i in par.ask):
                    ask(speak,logger,wolframalpha,takeCommand)

                elif brain_statement == "about_the_program": #any(i in statement for i in par.about_the_program):
                    if 'who are you' in statement or 'what can you do' in statement:
                        cprint('I am MIA version 0.0.1 your personal assistant. I am programmed to make your life easier')
                        speak('I am MIA version 0.0.1 your personal assistant. I am programmed to make your life easier')


                    elif "made you" in statement or "created you" in statement or "discovered you" in statement:
                        speak("I was built by Konstantino Moka")
                        cprint("I was built by Konstantino Moka")
                        
                    elif "lines of code do you have" in statement or "how long is your code" in statement:
                        clof(speak)

                elif brain_statement == "weather": #any(i in statement for i in par.weather):
                    w(speak,takeCommand,logger,requests)
                
                elif any(i in statement for i in par.keyboard_lock):
                    pass
                
                elif brain_statement == "turn_of": #any(i in statement for i in par.turn_of):
                    cprint("Ok , your pc will turn off in 10 sec make sure you exit from all applications", pcolors.WARNING)
                    logger.info("[INFO] Pc Shutdown")
                    speak("Ok , your pc will turn off in 10 sec make sure you exit from all applications")
                    subprocess.call(["shutdown", "/l"])
                
                elif brain_statement == "cancel_turn_of": #any(i in statement for i in par.cancel_turn_of):
                    shutdown(logger,speak,subprocess)
                    break
                    
                elif brain_statement == "email":
                    user_email = settings["users"][username]["email"]
                    emailer(logger,username,"hi",user_email)
                    del user_email

                else:
                    if bot_v != "n":
                        cprint("----- BOT -------")
                        cprint(statement)
                        logger.info("[INFO] Bot response")
                        results = MIA.get_response(statement)
                        cprint(results)
                        speak(results)
                        
                        try:
                            del results
                        except:
                            pass


if __name__ == '__main__':
    
    import logging
    import os
    logging.basicConfig(filename="logs/MIA.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)
    logging_level = logging.INFO
    logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
    logging.getLogger('comtypes').setLevel(logging.INFO)
    logging.getLogger('comtypes.client').setLevel(logging.INFO)
    logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
    logging.getLogger('chatterbot.chatterbot').setLevel(logging.WARNING)
    logging.getLogger('chatterbot.response_selection').setLevel(logging.WARNING)
    
    #from core.logs import logs
    #logging,logger = logs("logs/login.log", "DEBUG")
    if os.path.exists("\\security") != False:
        import lock
        lock_pass = str(input("Unlock Pass --> "))
        lock.unlock_MIA(lock_pass)
    
    console = logging.StreamHandler()
    if logging_level == 10:
        logger.addHandler(console)
        
    manual_give_choises = input("manual give choises [m(manual)/a(auto)]")
    if manual_give_choises == "m":
        ai_v_l = input("what ai version to load? [l(lite)/f(full)/n(none)] ")
        command_input = input("command input [v(voise)/k(keyboard)/i(instagram (not yet)))] ")
        speak_engine_volume = input("speak engine volume [101(Default)/'number'(The number giver)] ")
        if speak_engine_volume == '':
            speak_engine_volume=101
        online_ai = False
    else:
        #ai_v_l = "n"
        ai_v_l = "l"
        command_input = "v"
        speak_engine_volume = 101
        print("AI version [none]\ncommand input [voice]\nspeak engine volume [default]")
        online_ai = True

    MIA_assistant(ai_v_l, "user", True, logger, console, command_input, speak_engine_volume,online_ai)
