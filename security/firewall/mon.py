import ctypes, sys
from subprocess import Popen, PIPE, CalledProcessError
import logging

    
    
if __name__ == '__main__':
    
    logging.basicConfig(filename="logs.log",format='%(name)s -- %(asctime)s -- %(message)s',filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
    logging.getLogger('comtypes').setLevel(logging.INFO)
    logging.getLogger('comtypes.client').setLevel(logging.INFO)
    logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
    logging.getLogger('chatterbot.chatterbot').setLevel(logging.WARNING)
    
    console = logging.StreamHandler()
    
    def is_admin( ):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


    known_pros = []
    logs = []
    f = open("known_pros.txt", "r")
    for line in f:
      known_pros.append(line)

    f.close()
    print(known_pros)
    
    try:
        if is_admin():
            from win10toast import ToastNotifier
            toast = ToastNotifier()
            toast.show_toast("Notification","Notification body",duration=1)
            # Code of your program here
            #with Popen('netstat -a -b -f -o -q 1', stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            #startupinfo = subprocess.STARTUPINFO()
            #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            with Popen('netstat -b 1', stdout=PIPE, bufsize=1, universal_newlines=True, startupinfo=startupinfo) as p:
            #with Popen('netstat -b 1', stdout=PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    logs.append(line)
                    if "[" in line:
                        #print(line)
                        pros = line.split("[")
                        pros = pros[1].replace("]","")
                        print(pros, end="")
                        if pros not in known_pros:
                            inp = input(f"{pros} not in known prosseses. Do you want to put it? ")
                            if inp == "y":
                                known_pros.append(pros)
                            
                    
        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except KeyboardInterrupt:
    
        err = []
        for i in logs:
            try:
                logger.info(i)
            except Exception:
                err.append(i)
    
        print(known_pros)
        
        err = []
        f = open("known_pros.txt", "w")
        for i in known_pros:
            try:
                f.writelines(i)
            except Exception:
                err.append(i)
                
        f.close()
        print(err)
        sys.exit()
        
    except Exception:
        err = []
        for i in logs:
            try:
                logger.info(i)
            except Exception:
                err.append(i)
    
        print(known_pros)
        
        err = []
        f = open("known_pros.txt", "w")
        for i in known_pros:
            try:
                f.writelines(i)
            except Exception:
                err.append(i)
                
        f.close()
        print(err)
        
        sys.exit()
        