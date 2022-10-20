import sys,os
cwd = os.getcwd()
print("DIR: "+cwd)
lis=[]
print("files with .py and .json extentions")
print("-"*120)
print("#"*120)
print("-"*120)
er = 0
for path, subdirs, files in os.walk(cwd):
    try:
        for name in files:
            try:
                filee = os.path.join(path, name)
                if "__pycache__" not in filee and "ai_bot" not in filee and "google_assistant" not in filee:
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
print("-"*120)
print("#"*120)
print("-"*120)
print("lines of code in these files: "+str(len(lis)-44)+"\nAnd was "+str(er)+" errors")