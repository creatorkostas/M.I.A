import sqlite3

def connect(logger):
    logger.info("[INFO] Connencting to notes_database.db")
    try:
        conn = sqlite3.connect("notes_database.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note text, creation_time text )")
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error("[ERROR] Error while trying to connect to notes_database.db")
        logger.error("[ERROR] Error: "+str(e))

def view(logger):
    logger.info("[INFO] Retrieving notes")
    try:
        conn = sqlite3.connect("notes_database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM notes")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        logger.error("[ERROR] Error while trying to retrieve notes")
        logger.error("[ERROR] Error: "+str(e))
    
    

def new_note(speak,logger,takeCommand,datetime):
    speak("I am listening")
    note = takeCommand()
    # using now() to get current time 
    current_time = datetime.datetime.now() 
    logger.info("[INFO] Making new note. Time: "+str(current_time))
    connect(logger)
    conn = sqlite3.connect("notes_database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO notes VALUES (NULL,?,?)", (note,current_time))

    try:
        conn.commit()
        conn.close()
        logger.info("[INFO] New note saved successfully")
        
    except Exception as e:
        logger.error("[ERROR] Error while trying to save the note in database")
        logger.error("[ERROR] Error: "+str(e))
        conn.close()
        print("\nFaild")
        speak("There was an error while trying to save the note")
    
    
def del_note(speak,logger,takeCommand):
    
    connect(logger)
    
    
def edit_note(speak,logger,takeCommand):
    connect(logger)
    
def read_notes(speak,logger):
    logger.info("[INFO] Telling the notes to user")
    connect()
    notes = view(logger)
    for note in notes:
        speak(note)
        print(note)
        
if __name__ == '__main__':
    import logging
    import datetime
    import speech_recognition as sr
    #logging.basicConfig(filename="logs/logs.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
    logging.getLogger('comtypes').setLevel(logging.INFO)
    logging.getLogger('comtypes.client').setLevel(logging.INFO)
    logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
    console = logging.StreamHandler()
    
    def speak(text):
        print(text)
    
    def takeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.8
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio=r.listen(source)

            try:
                statement=r.recognize_google(audio).lower()
                print('user said: ' +statement + '\n')
                
            except Exception as e:
                #speak("Pardon me, please say that again")
                return 0
            return statement
    
    choise = input("1)new\n2) del\n3)Edit\n4)view\n")
    
    if choise == 1:
        new_note(speak,logger,takeCommand,datetime)
    elif choise ==2:
        pass
    elif choise ==3:
        pass
    elif choise ==4:
        read_notes()
    else:
        pass
    
    read_notes()