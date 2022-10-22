#ENDC = '\033[0m'
#def cprint(ctext,color):
#    print(f"{color}{ctext}\033[0m")

from time import sleep

def textp(text,color):
    print(color,'\r',text,' ', "\033[0m" , sep='', end='', flush=True)
 
def cprint(ctext, color="", mode=0, letter_time=0.07):
    #from instabot import Bot
    #bot = Bot()
    #bot.login()
    if mode == 0:
        if color == "":
            print(ctext)
        else:
            print(f"{color}{ctext}\033[0m")

    elif type(mode) == type([]) or mode == 4:
        tx = ""
        for i in range(len(ctext)):
            if type(mode) == type([]):
                end = mode[0]
                if len(mode) == 2:
                    end = f"{mode[1]}{end}\033[0m"
            else:
                end = ''
                
            tx += ctext[i]
            textp(tx,color)
            sleep(letter_time)
        
        print(end,'')
        
    elif mode == 1:
        print(f"{ctext}")
        #bot.send_messages(text=ctext,user_ids=["user"])
    elif mode == 2:
        pass
        #bot.send_messages(ctext,"user")
    elif mode == 3:
        pass
    
if __name__ == "__main__":
    color = '\033[94m'
    cprint("Test text",color,mode=['ok'],letter_time = 0.01)
    cprint("Test text",color,mode=['ok',color],letter_time = 0.01)
    cprint("Test text2",color,mode=4,letter_time = 0.01)