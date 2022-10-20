from dotenv import load_dotenv
import os
load_dotenv
def w(speak,takeCommand,logger,requests):
    api_key= os.getenv('OPENWEATHER_API')
    base_url="https://api.openweathermap.org/data/2.5/weather?"
    speak("what is the city name")
    city_name=takeCommand()
    logger.info("[INFO] Wheather in "+str(city_name))
    complete_url=base_url+"appid="+api_key+"&q="+city_name
    response = requests.get(complete_url)
    x=response.json()
    if x["cod"]!="404":
        y=x["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        speak(" Temperature in kelvin unit is " + str(current_temperature) + "\n humidity in percentage is " + str(current_humidiy) + "\n description  " + str(weather_description))
        print(" Temperature in kelvin unit = " + str(current_temperature) + "\n humidity (in percentage) = " + str(current_humidiy) + "\n description = " +str(weather_description))
    else:
        speak("Sorry i was anable to find info")
        print("Sorry i was anable to find info")