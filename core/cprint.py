#ENDC = '\033[0m'
#def cprint(ctext,color):
#    print(f"{color}{ctext}\033[0m")
 
def cprint(ctext,color="",mode=0):
    #from instabot import Bot
    #bot = Bot()
    #bot.login()
    if mode == 0:
        if color == "":
            print(ctext)
        else:
            print(f"{color}{ctext}\033[0m")
       
    elif mode == 1:
        print(f"{ctext}")
        #bot.send_messages(text=ctext,user_ids=["user"])
    elif mode == 2:
        pass
        #bot.send_messages(ctext,"user")
    elif mode == 3:
        pass