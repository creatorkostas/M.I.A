import requests
from io import StringIO
import json
import os
import time
from datetime import datetime
import sqlite3
from os import listdir
from os.path import isfile, join
import shutil
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('GITHUB_TOKEN')
owner = 'creatorkostas'
repo = 'M.I.A'

def execution_time_function(timer_start, timer_end, message):
    execution_time = (timer_end - timer_start)
    execution_time = "{:.2f}".format(round(execution_time, 2))
    print(f"{message} took {execution_time}s")
    
def db_upload_download(backup_database_path,upload_download):
    import paramiko

    try:
        host = os.getenv('UPDATE_DATABASE_HOST')
        username = os.getenv('UPDATE_DATABASE_USERNAME')
        password = os.getenv('UPDATE_DATABASE_PASS')
      
        port = 22
        transport = paramiko.Transport((host, port))
        transport.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception as e:
        print(str(e))
        
    if upload_download == "upload":
        try:
            path = "MIA_db/backup_database.db"
            localpath = backup_database_path
            sftp.put(localpath, path)
            sftp.close()
            transport.close()
        except Exception as e:
            print(str(e))
    elif upload_download == "download":
        try:
            remotepath = "MIA_db/backup_database.db"
            localpath = backup_database_path
            sftp.get(remotepath, localpath)
            sftp.close()
            transport.close()
        except Exception as e:
            print(str(e))

def check_for_update():
    


    # define parameters for a request
    path = 'data/info.json'
    #path = 'assistant.py'

    # send a request
    r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{path}', headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
    r = r.text
    r = r.split(",")
    r = r[0].replace("[{","")
    r = r.replace("\n","")
    r = r.replace('"Version": "Alpha v',"")
    r = r.replace('"',"")
    r = r.replace(' ',"")
    
    f0 = open("data/info.json","r")
    f = f0.read()
    f0.close
    f = f.split(",")
    f = f[0].replace("[{","")
    f = f.replace("\n","")
    f = f.replace('"Version": "Alpha v',"")
    f = f.replace('"',"")
    f = f.replace(' ',"")
    
    if str(r) != str(f):
        return True
    else:
        return False
    
    
def download_update_files(files):
    for file in files:
        file = file.split(" ")
        if file[2] == "d":
            dfile = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{file[1]}', headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
            
            file_handle = open(file[0], "wb")
            file_handle.write(dfile)
            file_handle.close  

def make_an_update(start_dir,end_dir,backup_database_path,path_to_replace,debug_print=False):
    
    
    def connect():
        conn = sqlite3.connect(backup_database_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS database (id INTEGER PRIMARY KEY, filename text, last_modification_time text, filesize text)")
        conn.commit()
        conn.close()

    def view():
        conn = sqlite3.connect(backup_database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM database")
        rows = cur.fetchall()
        return rows
        conn.close()

    def delete(id):
        conn = sqlite3.connect(backup_database_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM database WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    #----------------------------------      
    connect()
    #----------------------------------

    def read_database_files(db_files):
        timer_start = time.time()
        database = view()
        print("Database lenght: "+str(len(database)))
        print("\nReading data from Database...")
        for i in tqdm(range(0, len(database))):
            db_files.append(database[i][1])
        timer_end = time.time()
        execution_time_function(timer_start, timer_end, "time took: ")
        return db_files

    def update_database_for_not_existing_files_in_it(t,err,db_files,start_dir,path_to_replace):
        print("\nComparing files from Database and Directory...")
        timer_start = time.time()
        database = view()
        # r=root, d=directories, f = files
        for r, d, f in os.walk(start_dir):
            for file in f:
                #print(os.stat(os.path.join(r, file)))
                file_path_updated = os.path.join(r, file)
                if ".git" not in file_path_updated:
                    file_path_updated = file_path_updated.replace(path_to_replace,"")
                    t[0].append(file_path_updated)  #file
                    t[1].append(str(os.stat(os.path.join(r, file))[8])) #last modification time
                    t[2].append(os.stat(os.path.join(r, file))[6]) #filesize

        print("Files to check: "+str(len(t[0])))

        #insert into database
        conn = sqlite3.connect(backup_database_path)
        cur = conn.cursor()
        
        for i in tqdm(range(0, len(t[0]))):
            #print(t[0][i])
            if t[0][i] not in db_files:
                print("New file found: "+t[0][i])
                try:
                    cur.execute("INSERT INTO database VALUES (NULL,?,?,?)", (t[0][i], t[1][i], t[2][i]))
                except Exception:
                    err[0].append(t[0][i])
                    err[1].append(t[1][i])
                    err[2].append(t[2][i])
                    
            elif str(database[i][2]) != str(t[1][t[0].index(database[i][1])]) or str(database[i][3]) != str(t[2][t[0].index(database[i][1])]):
                try:
                    print("\n\n"+"-"*60+"\n"+str(database[i][0])+": "+str(database[i][1])+"\n")
                    print("update last modification time and filesize")
                    print("-"*60)
                    cur.execute("UPDATE database SET last_modification_time="+t[1][t[0].index(database[i][1])]+", filesize="+str(t[2][t[0].index(database[i][1])])+" WHERE id="+str(database[i][0]))
                except Exception as e:
                    print(str(e))
                    err[0].append(t[0][i])
                    err[1].append(t[1][i])
                    err[2].append(t[2][i])
                #print(view())
        try:
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(str(e))
            conn.close()
            print("\nFaild")

        timer_end = time.time()
        execution_time_function(timer_start, timer_end, "time took: ")
        
        if len(err[0]) == 0:
            print("\nDone")
        else:
            print("\nError list: ")
            print(err)
            
    def update_del_files(database):
        print("Checking Files for Delete...")
        for i in tqdm(range(0, len(database))):
            if database[i][1] not in t[0]:
                print(database[i][1]+" does not exist")
                #os.remove(end_dir+database[i][1].replace(start_dir, ""))
                delete(database[i][0])

    

    t = [[],[],[]]
    err = [[],[],[]]
    db_files = []
    
    def update_database():
    
        update_database_for_not_existing_files_in_it(t,err,db_files,start_dir,path_to_replace)
        database = view()
        update_del_files(database)
        database = view()
        return database
    update_database()   

def update_prosses(end_dir,backup_database_path,path_to_replace):
    import os
    import time
    from datetime import datetime
    import sqlite3
    from os import listdir
    from os.path import isfile, join
    import shutil
    from tqdm import tqdm
    import requests
    from io import StringIO
    import json

    def view():
        conn = sqlite3.connect(backup_database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM database")
        rows = cur.fetchall()
        return rows
        conn.close()

    database = view()

    t2 = [[],[],[]]
    err2 = [[],[],[]]
    db_files2 = []
    
    timer_start = time.time()
    # r=root, d=directories, f = files
    for r, d, f in os.walk(end_dir):
        for file in f:
            file_path_updated = os.path.join(r, file)
            if ".git" not in file_path_updated:
                file_path_updated = file_path_updated.replace(path_to_replace,"")
                t2[0].append(file_path_updated)  #file
                #print(os.stat(os.path.join(r, file)))
                t2[1].append(str(os.stat(os.path.join(r, file))[8])) #last modification time
                t2[2].append(os.stat(os.path.join(r, file))[6]) #filesize

    timer_end = time.time()
    execution_time_function(timer_start, timer_end, "time took: ")
    print(len(t2[0]))

    print("\nUpdate prosses...")
    for i in tqdm(range(0, len(database))):
        if database[i][1] not in t2[0]:
        
            try:
                dfile = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{database[i][1]}', headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
                file_handle = open("new_files\\"+database[i][1], "wb")
                file_handle.write(dfile)
                file_handle.close
                
                #to download the files and the to copy them
                #print("coping...\n"+database[i][1])
                shutil.copy2("new_files\\"+database[i][1], database[i][1])
                
            except FileNotFoundError:
                folder = database[i][1]
                folder = folder.replace(database[i][1].split("\\")[len(database[i][1].split("\\"))-1], "")
                #print(folder)
                os.makedirs(folder)
                
                dfile = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{database[i][1]}', headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
                file_handle = open("new_files\\"+database[i][1], "wb")
                file_handle.write(dfile)
                file_handle.close
                
                shutil.copy2("new_files\\"+database[i][1], database[i][1])
        
        elif str(database[i][2]) != str(t2[1][t2[0].index(database[i][1])]) or str(database[i][3]) != str(t2[2][t2[0].index(database[i][1])]):
            print(database[i][1]+" has been changed")
            os.remove(database[i][1])
            
            dfile = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{database[i][1]}', headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
            file_handle = open("new_files\\"+database[i][1], "wb")
            file_handle.write(dfile)
            file_handle.close
                

            #os.remove(end_dir+database[i][1].replace(start_dir, ""))
            #shutil.copy2(database[i][1], end_dir+database[i][1].replace(start_dir, ""))
            shutil.copy2("new_files\\"+database[i][1], database[i][1])
            
            
        if debug_print:
            print(database[i][2])
            print(t2[1][t2[0].index(database[i][1].replace(start_dir, ""))])
            print("-"*60)
            print(database[i][3])
            print(t2[2][t2[0].index(database[i][1].replace(start_dir, ""))])
            print("-"*60)
            print("-"*60)
        

if __name__ == "__main__":
    import time
    import os
    print("Sleeping for 10 seconds!")
    #time.sleep(10)
    
    backup_database_path = "updater/update_database.db"
    os.chdir('..')
    start_dir = os.getcwd()
    path_to_replace = start_dir
    
    if check_for_update():
        db_upload_download(backup_database_path,"download")
        update_prosses(start_dir,backup_database_path,path_to_replace)
        print("Update DONE!")
    else:
        print("No update")