import sys,os

def clof(speak):
    cwd = os.getcwd()
    lis=[]
    print("files with .py and .json extentions")
    er = 0
    for path, subdirs, files in os.walk(cwd):
        try:
            for name in files:
                try:
                    filee = os.path.join(path, name)
                    fi = filee
                    filee = filee.replace("\\", "/")
                    filepath = filee.split(".")
                    if len(filepath) == 1:
                        ext = ""
                        filepath = filepath[-1]
                    else:
                        ext = filepath[-1]
                        filepath = filepath[:-1]
                    try:
                        if ext == "py" or ext == "json":
                            print(fi)
                            f = open(fi, "r")
                            for x in f:
                                #print(x)
                                if x == "" or x == " " or x == "    ":
                                    pass
                                else:
                                    lis.append(x)
                            f.close()
                    except Exception:
                        er = er + 1
                except Exception:
                    er = er + 1
        except Exception:
            er = er + 1
    print("lines of code in these files: "+str(len(lis)-40)+"\nAnd was "+str(er)+" errors")
    speak("I consist approximately of "+str(len(lis)-40)+" lines of code")