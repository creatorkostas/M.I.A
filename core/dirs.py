import os
from os import listdir
from os.path import isfile, join


#start_dir="C:/"

dirs_not_to_search=['C:/Program Files\\', 'C:/Program Files (x86)\\', 'C:/Windows\\', 'C:/Intel\\', 'C:/PerfLogs\\']

def index_dirs(start_dir):
    ds=[]
    for root, dirs, files in os.walk(start_dir, topdown=False):
        for name in dirs:
            if not any(i in root for i in dirs_not_to_search):
                to_append=os.path.join(root, name)
                to_append=to_append.replace("\\","/")
                ds.append(to_append)

    print(len(ds))

    f = open("dirs.txt", "w", encoding="utf-8")
    err = []

    for i in ds:
        try:
            f.writelines(i+"\n")
        except Exception:
            err.append(i)

    f.close()
    print(err)
    del ds, err

def read_indexed_dirs():
    ds=[]
    f = open("dirs.txt", "r", encoding="utf-8")
    ds = f.readlines()

    for i in range(0,len(ds)):
        ds[i] = ds[i].replace("\n","")

    f.close()
    del f
    return ds