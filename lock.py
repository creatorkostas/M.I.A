class lock:
    def lock_MIA(lock_pass):
        import py7zr
        import os
        with py7zr.SevenZipFile('lock.7z', 'w', password=lock_pass) as archive:
            archive.writeall(os.getcwd()+'\\security','security')
        import shutil
        shutil.rmtree(os.getcwd()+'\\security')
        
    def unlock_MIA(lock_pass):
        import py7zr
        import os
        with py7zr.SevenZipFile('lock.7z', mode='r', password=lock_pass) as archive:
            archive.extractall()
        os.remove('lock.7z')

if __name__ == "__main__":
    choice = int(input("1 or 2 --> "))
    passw = input("pass --> ")
    if choice == 1:
        lock.lock_MIA(passw)
    elif choice == 2:
        lock.unlock_MIA(passw)