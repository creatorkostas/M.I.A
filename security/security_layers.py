import datetime
import hashlib
from dotenv import load_dotenv
import os
load_dotenv()


class securitylayers:
    def __init__(self):
        self.adminlist = [os.getenv('ADMIN_PASS_LIST_SHA512')]
        self.users = [os.getenv('USER1'),os.getenv('USER2')]
        self.userpass = [os.getenv('USERPASS1_SHA512'),os.getenv('USERPASS2_SHA512')]

    def gather_data(self):
        import subprocess
        import urllib.request
        import json
        url = 'http://ipinfo.io/json'
        response = urllib.request.urlopen(url)
        data = json.load(response)

        IP=data['ip']
        org=data['org']
        city = data['city']
        country=data['country']
        region=data['region']
        loc=data['loc']

        current_temp = ""
        data = org+city+country+region+loc

        out = subprocess.check_output('netsh wlan show interfaces').decode("utf-8")
        current = out.split("\n")
        pop_list = [16, 16, 16] 
        for i in pop_list:
            current.pop(i)

        for i in current:
            if i != "" or i != "\n" or i != "\r":
                temp = i.replace("\r","")
                temp = temp.split(":")
                if len(temp) == 2:
                    current_temp += temp[1]

        data += current_temp
        data = hashlib.sha512(data.encode('utf-8')).hexdigest()
        data = hashlib.sha512(data.encode('utf-8')).hexdigest()
        #print(f"Data: \n{data}\n\n")
        return data

    def check_if_in_admin_list(self,username,password):
        if username in self.users and password == self.userpass[self.users.index(username)]:
            if hashlib.sha512(username.encode('utf-8')).hexdigest() in self.adminlist:
                return True
        return False
 
    def send_g_pin(self,username,logger):
        try:
            from core.emailer import gmail_send_message
           
            pin_gen_time = int(datetime.datetime.now().strftime("%M"))
            g_pin = int(datetime.datetime.now().strftime("%m%d%Y%H%M"))
            g_pin = str(g_pin + int(g_pin/int(datetime.datetime.now().strftime("%Y")))) + username
            g_pin = int(hashlib.sha256(g_pin.encode('utf-8')).hexdigest(), 16) % 10**4
            print("Pin is active for 5 minutes")
            logger.info("[INFO] Pin created successfully for user: "+username)
            
            import getpass
            import platform
            os_user_name = getpass.getuser()
            os_name = platform.system()

            message = f"\nPIN: {g_pin}\n\nOS: {os_name}\nOS USER NAME: {os_user_name}\n\nLOGIN USERNAME: {username}"
            gmail_send_message(logger,username,message,os.getenv('ADMIN_MAIL'))
            #server.sendmail(sender_email, receiver_email, message)
            print("Email with pin send successfully")
            logger.info("[INFO] Email with pin send successfully for user: "+username)
            
            try:
                del os_user_name
                del os_name
                del getpass
                del platform
            except:
                pass
            #print("PIN (while emailer is under fix): "+str(g_pin))
            return pin_gen_time, g_pin
            
        except Exception as e:
            print(str(e))
            return "" , ""
    
    def admin_security_layer(self,username,logger):
        # Try to log in to server and send email
        try:
            pin_gen_time, g_pin = self.send_g_pin(username,logger)
            
        except Exception as e:
            print("Error sending email")
            logger.error("[ERROR] Error while trying to send email for user: "+username)
            #logger.addHandler(console)
            logger.debug("[DEBUG] Error: "+str(e))
            pin = "ERROR"
            #logger.removeHandler(console)
        
        def del_admin_verification_variables(pin_gen_time,pin_in_time,pin,g_pin):
            pin_gen_time = ""
            pin_in_time = ""
            pin = ""
            g_pin = ""
            try:
                del pin_gen_time
                del pin_in_time
                del pin
                del g_pin
            except:
                pass
        
        if g_pin != "" and pin_gen_time != "":
            pin = input("Please provide the pin --> ") #disabled for development only

            pin_in_time = int(datetime.datetime.now().strftime("%M"))
            if pin_in_time-pin_gen_time <= 5:
                if pin == str(g_pin): #disabled for development only
                    del_admin_verification_variables(pin_gen_time,pin_in_time,pin,g_pin)
                    return True
                else:
                    del_admin_verification_variables(pin_gen_time,pin_in_time,pin,g_pin)
                    return False
            else:
                del_admin_verification_variables(pin_gen_time,pin_in_time,pin,g_pin)
                print("Pin expired")
                logger.info("[INFO] Pin expired for user: "+username)
                return False
        else:
            print("There was a problem with pin.\nVerification was unsuccessful")
            logger.warning("[SECURITY] There was a problem with pin. Verification was unsuccessful for user: "+username)
            return False

    def check_internet_connection(self,logger):
        import socket
        IPaddress=socket.gethostbyname(socket.gethostname())
        if IPaddress=="127.0.0.1":
            logger.addHandler(console)
            logger.warning("[WARNING] Internet connection is down")
            logger.removeHandler(console)
            del IPaddress
            return False
        else:
            logger.info("[INFO] Internet connection is up with IP: "+IPaddress)
            print("Connected to the internet")
            del IPaddress
            return True
    
    def first_security_layer(self,username, password, connected_to_the_internet,logger):
        isadmin = False
        fspass = False
        if username == "" or password == "":
            print("You must provide a username and a password!")
            logger.info("[INFO] None credentials provided")
            exit()
        elif username in self.users and password == self.userpass[self.users.index(username)]:
            fspass = True
            
            if hashlib.sha512(username.encode('utf-8')).hexdigest() in self.adminlist:
                
                if self.admin_security_layer(username,logger) and connected_to_the_internet:
                    logger.info("[INFO] user: "+username+" logged in as admin")
                    print("(Admin) Welcome "+username+" !")
                    isadmin = True
                else:
                    if connected_to_the_internet == False:
                        logger.warning("[SECURITY] user: "+username+" tried to log in as admin but was anable to identified his/her identity because there is no conecction to the internet")
                    else:
                        logger.warning("[SECURITY] user: "+username+" tried to log in as admin but was anable to identified his/her identity")
                    print("You tried to login as admin without permision or without internet connection.\nPlease do not try it again!")
                    isadmin = False
                    exit()
            else:
                logger.info("[INFO] "+username+" logged in")
                print("Welcome "+username+" !")
        else:
            print("Wrong username or password!")
            logger.warning("[SECURITY] Wrong credentials (user: "+username+ " with pass: "+password+")")
            exit()

        try:
            del username
            del password
        except:
            pass

        return fspass, isadmin