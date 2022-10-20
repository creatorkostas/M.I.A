class music:
    def __init__(self,logger,pafy,vlc,YoutubeSearch,speak):
        self.logger = logger
        self.pafy = pafy
        self.vlc = vlc
        self.YoutubeSearch = YoutubeSearch
        self.speak = speak
        
    def play(self,statement):
        #speak("These function is not implemented yet!")
        self.logger.info("[INFO] Playing music")
        #music_path = json.load(open("data/settings.json", "r"))
        statement = statement.replace("play", "")
        
        #get videos urls
        if 'max results' in statement:
            m_results = 1
        else:
            m_results = 1
        results = self.YoutubeSearch(statement, max_results=m_results).to_json()
        results= results.replace(",", ":")
        results = results.split(":")
        ti=[]
        di=[]
        ui=[]
        for i in range(0, len(results)):
            if results[i] == ' "title"':
                ti.append(results[i+1].replace('"',""))
            if results[i] == ' "duration"':
                di.append((results[i+1]+":"+results[i+2]).replace('"',""))
            if results[i] == ' "url_suffix"':
                ui.append(results[i+1].replace('"','').replace("}","").replace("]",""))
        
        url = "https://www.youtube.com"+ui[0]
        url = url.replace(" ","")
        video = self.pafy.new(url)
        #audiostreams = video.audiostreams
        bestaudio = video.getbestaudio()
        playurl = bestaudio.url  
        Instance = self.vlc.Instance()
        self.player = Instance.media_player_new()
        Media = Instance.media_new(playurl)

        self.player.set_media(Media)     
        self.player.play()
        return
        
    def control_player(self, statement):
        try:
            if "pause" in statement:
                self.player.pause()
            elif "stop" in statement:
                self.player.stop()
            elif "play" in statement:
                self.player.play()
        except Exception:
            print("No music is playing")
            self.speak("No music is playing")
        
    def play_by_input_name(self):
        #speak("These function is not implemented yet!")
        self.logger.info("[INFO] Playing music")
        #music_path = json.load(open("data/settings.json", "r"))
        statement = input("Song name --> ")
        
        #get videos urls
        if 'max results' in statement:
            m_results = 1
        else:
            m_results = 1
        results = self.YoutubeSearch(statement, max_results=m_results).to_json()
        results= results.replace(",", ":")
        results = results.split(":")
        ti=[]
        di=[]
        ui=[]
        for i in range(0, len(results)):
            if results[i] == ' "title"':
                ti.append(results[i+1].replace('"',""))
            if results[i] == ' "duration"':
                di.append((results[i+1]+":"+results[i+2]).replace('"',""))
            if results[i] == ' "url_suffix"':
                ui.append(results[i+1].replace('"','').replace("}","").replace("]",""))
        
        url = "https://www.youtube.com"+ui[0]
        url = url.replace(" ","")
        video = self.pafy.new(url)
        #audiostreams = video.audiostreams
        bestaudio = video.getbestaudio()
        playurl = bestaudio.url  
        Instance = self.vlc.Instance()
        self.player = Instance.media_player_new()
        Media = Instance.media_new(playurl)

        self.player.set_media(Media)     
        self.player.play()
        return


def p(logger,statement,YoutubeSearch,pafy,vlc):
    #speak("These function is not implemented yet!")
    logger.info("[INFO] Playing music")
    #music_path = json.load(open("data/settings.json", "r"))
    statement = statement.replace("play", "")
    
    #get videos urls
    if 'max results' in statement:
        m_results = 1
    else:
        m_results = 1
    results = YoutubeSearch(statement, max_results=m_results).to_json()
    results= results.replace(",", ":")
    results = results.split(":")
    ti=[]
    di=[]
    ui=[]
    for i in range(0, len(results)):
        if results[i] == ' "title"':
            ti.append(results[i+1].replace('"',""))
        if results[i] == ' "duration"':
            di.append((results[i+1]+":"+results[i+2]).replace('"',""))
        if results[i] == ' "url_suffix"':
            ui.append(results[i+1].replace('"','').replace("}","").replace("]",""))
    
    url = "https://www.youtube.com"+ui[0]
    url = url.replace(" ","")
    video = pafy.new(url)
    #audiostreams = video.audiostreams
    bestaudio = video.getbestaudio()
    playurl = bestaudio.url  
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    #Media.get_mrl()
    #https://r6---sn-ixaa5n-5uid.googlevideo.com/videoplayback?expire=1622064420&ei=xGiuYOakF8bQ7gPa87rIDg&ip=141.237.108.242&id=o-AP43Kud1WQrhzteUWT3bIqaDK9B6zNhxDZuZ9Kv-qEDv&itag=140&source=youtube&requiressl=yes&mh=xu&mm=31%2C29&mn=sn-ixaa5n-5uid%2Csn-nv47lnl6&ms=au%2Crdu&mv=m&mvi=6&pl=20&initcwndbps=647500&vprv=1&mime=audio%2Fmp4&ns=68BxDRL5UszjlsO6ZCSt3CAF&gir=yes&clen=168213986&dur=10393.878&lmt=1572316907885052&mt=1622042699&fvip=6&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=1301222&n=q5d02z_ZMqmi34c6hS&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgSbgIuZFp4EKbZfRBAUohM_yN9imLhB5JzTxWaQBGl1MCIQCV7tCs7FSyQ82o6l93jq4U9Zjs_jtHbGlAi-reKfn3tw%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRAIgd0jkkIRnt2S0yHZ6TSo_xp_dnObzWGMetIMlbHlIfxQCICoCU6A1vbiSDI_U3oorfywFD-0ydOpxDLQKXQ5ZkJuw'
    player.set_media(Media)     
    player.play()
    return player
    '''
    player.play()
    player.pause()
    player.stop()
    '''

def c(player,statement, speak):
    if "pause" in statement:
        try:
            player.pause()
        except Exception:
            print("No music is playing")
            speak("No music is playing")
            
    elif "stop" in statement:
        try:
            player.stop()
        except Exception:
            print("No music is playing")
            speak("No music is playing")
    
    elif "play" in statement:
        try:
            player.play()
        except Exception:
            print("No music is paused")
            speak("No music is paused")
            
            
if __name__ == "__main__":
    #import YoutubeSearch,pafy,vlc
    from youtube_search import YoutubeSearch
    import pafy
    import vlc
    
    import logging
    logging.basicConfig(filename="logs.log",format='%(process)d -- %(name)s -- %(asctime)s -- %(levelname)s --  %(message)s',filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('comtypes._comobject').setLevel(logging.INFO)
    logging.getLogger('comtypes').setLevel(logging.INFO)
    logging.getLogger('comtypes.client').setLevel(logging.INFO)
    logging.getLogger('comtypes.client._code_cache').setLevel(logging.WARNING)
    logging.getLogger('chatterbot.chatterbot').setLevel(logging.WARNING)
    
    console = logging.StreamHandler()
    
    def speak(a):
        print(a)

    statement = "play christmas mix"
    player = p(logger,statement,YoutubeSearch,pafy,vlc)
