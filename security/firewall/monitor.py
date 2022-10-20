import ctypes, sys
from subprocess import Popen, PIPE, CalledProcessError
import logging

def is_admin():
    import ctypes, sys
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def start_monitoring():
    from subprocess import Popen, PIPE, CalledProcessError
    import logging

    logging.basicConfig(filename="../../logs/firewall_logs.log",format='%(name)s -- %(asctime)s -- %(message)s',filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
    logging.getLogger('comtypes').setLevel(logging.INFO)
    logging.getLogger('comtypes.client').setLevel(logging.INFO)
    logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
    logging.getLogger('chatterbot.chatterbot').setLevel(logging.WARNING)

    known_pros = []
    logs = []
    f = open("known_pros.txt", "r")
    for line in f:
      known_pros.append(line)

    f.close()
    #print(known_pros)
    
    try:
        if is_admin():
            # Code of your program here
            #with Popen('netstat -a -b -f -o -q 1', stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            with Popen('netstat -b 1', stdout=PIPE, bufsize=1, universal_newlines=True, startupinfo=startupinfo) as p:
                for line in p.stdout:
                    logs.append(line)
                    if "[" in line:
                        #print(line)
                        pros = line.split("[")
                        pros = pros[1].replace("]","")
                        #print(pros, end="")
                        if pros not in known_pros:
                            logger.warning(f"[SECURITY] {i} used the internet")

                    
        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        logger.error("[ERROR] Error: "+str(e))

    
if __name__ == '__main__':
    start_monitoring()
    