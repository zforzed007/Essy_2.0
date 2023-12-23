import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pywhatkit
from config import apikey
import datetime
import wikipedia
import os

openai.api_key = apikey

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 180)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

convo = ""
user_name = "Friend"
assistant_name = "essy 2.0"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning!")
    elif hour>=12 and hour<17:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("My name is Essy two point o! How may I help you")

def takecommand():
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source,duration=0.2)
        r.energy_threshold = 800
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        user_input = r.recognize_google(audio, language='en-in')
        print(f"User said : {user_input}")
        
    except Exception as e:
        print(e)
        speak("Didn't get you")
        print("Didn't get you")
        return "None"
    return user_input

def ai(input):
    prompt = user_name + ":" + input + "\n" + assistant_name + ":"
    global convo 
    convo += prompt
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=convo,
        temperature=1,
        max_tokens=32,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    response_str = response["choices"][0]["text"].replace("\n","")
    response_str = response_str.split(user_name + ":" ,1)[0].split(assistant_name + ":" ,1)[0]
            
    convo += response_str +"\n"
    
    print(f"Essy 2.0 : {response_str}\n")
    engine.say(response_str)
    engine.runAndWait()
    return(f"Essy 2.0 : {response_str}\n")

def openApp(input):
    
    if 'discord' in input:
        speak("Opening discord")
        codePath = "C:\\Users\\Z\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord"
        os.startfile(codePath)
        
    elif 'code' in input:
        speak("Opening vs code")
        codePath = "C:\\Users\\Z\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code"
        os.startfile(codePath)
        
    elif 'steam' in input:
        speak("Opening steam")
        codePath = "D:\\programs\\Steam\\steam"
        os.startfile(codePath)
        
    elif 'vmware' in input:
        speak("Opening VM ware")
        codePath = "D:\\programs\\vmplayer"
        os.startfile(codePath)
        
    elif 'spotify' in input:
        speak("Opening spoti fy")
        codePath = "C:\\Users\\Z\\OneDrive\\Desktop\\Spotify"
        os.startfile(codePath)
        
    elif 'hotstar' in input:
        speak("Opening hotstar")
        codePath = "C:\\Users\\Z\\OneDrive\\Desktop\\Hotstar"
        os.startfile(codePath)
        
    else:
        speak("Requested apps are unavailable or cannot be opened")
      
def closeApp(input):
    
    if 'spotify' in input:
        speak("closing spotify")
        os.system("TASKKILL /f /im spotify.exe")
        
    elif 'discord' in input:
        speak("closing discord")
        os.system("TASKKILL /f /im discord.exe")
        
    elif 'steam' in input:
        speak("closing ")
        os.system("TASKKILL /f /im steam.exe")    
    
    elif 'code' in input:
        speak("closing vs code")
        os.system("TASKKILL /f /im code.exe")
        
    elif 'vmware' in input:
        speak("closing VM ware")
        os.system("TASKKILL /f /im vmplayer.exe")
    
    else:
        speak("Requested app is either not open or cannot be closed")


if __name__ == "__main__":
    
    wishme()
    
    while True:
        
        user_input = takecommand().lower()
        
        if 'stop' in user_input: 
            speak("It was nice to have a conversation with you!")
            exit(0)
        
        if 'open website' in user_input:
            user_input = user_input.replace("open website","")
            user_input = user_input.replace(" ","")
            speak(f"opening {user_input} .com ")
            web = 'https://www.' + user_input + '.com'
            webbrowser.open(web)
            continue
        
        elif 'wikipedia' in user_input:
            speak("Searching wikipedia...")
            user_input = user_input.replace("wikipedia","")
            results = wikipedia.summary(user_input,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            continue
        
        elif 'open maps' in user_input:
            speak("Opening maps")
            webbrowser.open("googlemaps.com") 
        
        elif 'search on youtube' in user_input:
            user_input = user_input.replace("search on youtube","")
            speak(f"searching {user_input} on youtube")
            web = 'https://www.youtube.com/results?search_query=' + user_input
            webbrowser.open(web)
            continue
            
        elif 'search on google' in user_input:
            user_input = user_input.replace("search on google","")
            speak(f"searching {user_input} on google")
            pywhatkit.search(user_input)
            continue
                
        elif 'the time' in user_input:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(strTime)
            continue
        
        elif 'open app' in user_input:
            speak("Which app would you like to open")
            Appinput = takecommand().lower()
            openApp(Appinput)
            continue
        
        elif 'close app' in user_input:
            speak("Which app would you like to close")
            Appinput = takecommand().lower()
            closeApp(Appinput)
            continue
        
        else :
            ai(user_input)
            continue