def open_subfunction(logger, speak, to_open, time, webbrowser, sleep_wait_time, os, programs_name, programs_path, item):
    browser_statments = ["youtube", "google", "gmail"]
    if any(i in item for i in programs_name):
        logger.info("[INFO] Openning "+to_open)
        program_path = programs_path[programs_name.index(to_open)]
        program_final_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"+program_path+".lnk"
        os.system('cmd /c "'+program_final_path+'"')
        speak(to_open+" have been opend")
    else:
        logger.info("[INFO] Openning "+to_open)
        webbrowser.open_new_tab("https://www."+to_open+".com")
        speak(to_open+" have been opend")
        time.sleep(sleep_wait_time)

def open_function(logger, speak, statement, time, webbrowser, sleep_wait_time, os, programs_name, programs_path):
    to_open = statement.replace("open ", "")
    if 'and' in statement:
        statement = statement.split("and")
        for item in statement:
            open_subfunction(logger, speak, to_open, time, webbrowser, sleep_wait_time, os, programs_name, programs_path, item)
    else:
        open_subfunction(logger, speak, to_open, time, webbrowser, sleep_wait_time, os, programs_name, programs_path, statement)
        
    try:
        del logger, speak, to_open, time, webbrowser, sleep_wait_time, os, programs_name, programs_path
    except:
        logger.error("[ERROR] Error while tring to delete some variables")
        