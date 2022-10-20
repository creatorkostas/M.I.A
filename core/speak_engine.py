from pydub import AudioSegment
from pydub.playback import play
import io
import requests

class online_speak_engine:
    def __init__(self):
        print("Online speak engine have been loaded!")
        self.temp_filename = 'temp.mp3'
        

    def say(text,not_asynchronous=False):
        s = "https://api.carterapi.com/v0/speak/CEpSVEJYeFrE7IdJ74jCNsMyhbulyHKA/"+text
        #AudioSegment.ffmpeg  = "./core/modules_files/ffmpeg"
        r = requests.get(s, stream=True)
        song = AudioSegment.from_file(io.BytesIO(r.content), format="mp3")
        play(song)
    def runAndWait():
        print("This property is not available in the online version")
        pass
        
    def setProperty(a='',b=''):
        print("This property is not available in the online version")
        pass
    
    
def load_speak_engine(pyttsx3,online_engine,carter_key):
    if online_engine:
        return online_speak_engine(carter_key)
    else:
        engine = pyttsx3.init(debug=False)
        #voices = engine.getProperty('voices')
        #for voice in voices:
        #    print("Voice:")
        #    print(" - ID: %s" % voice.id)
        #    print(" - Name: %s" % voice.name)
        #    print(" - Languages: %s" % voice.languages)
        #    print(" - Gender: %s" % voice.gender)
        #    print(" - Age: %s" % voice.age)
        #engine.setProperty('voice', 'voice[10].id')
        #engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
        #engine.getProperty('voices')
        #engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', '173')
        #engine.setProperty('volume', 0)
        
        return engine

    
def speak(text,engine):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    from playsound import playsound
    import requests
    import os
    sp = load_speak_engine("",True)
    t = "I am MIA version 0.0.1"
    sp.say(t,False)
    sp.runAndWait()
    sp.setProperty()
    import time
    time.sleep(500)