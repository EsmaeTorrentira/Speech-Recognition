import speech_recognition as sr
import keyboard
import pyttsx3
import pywhatkit
import pyjokes
import webbrowser
import os
import time
import sys

# Setup TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speech speed

def speak(text):
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="en-US")
        print("✅ You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

def execute_command(command):
    if not command:
        return

    if "play" in command:
        song = command.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Please tell me what to play.")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "time" in command:
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "open" in command and "chrome" in command:
        site = command.replace("open", "").replace("in chrome", "").strip()
        if site:
            if not site.startswith("http"):
                site = "https://www." + site.replace(" ", "") + ".com"
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chrome_path).open(site)
            speak(f"Opening {site} in Chrome")
        else:
            speak("Please tell me which site to open in Chrome.")

    elif "open folder" in command or "open file" in command:
        path = command.replace("open folder", "").replace("open file", "").strip()
        if os.path.exists(path):
            os.startfile(path)
            speak(f"Opening {path}")
        else:
            speak(f"Sorry, I couldn't find {path}")

    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")

    elif "sleep" in command:
        speak("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        sys.exit()

    else:
        speak("Sorry, I don't know that command yet.")

def main():
    speak("Voice Assistant ready. Press F4 to talk to me.")
    while True:
        # Wait for F4 to activate listening
        keyboard.wait('F4')
        time.sleep(0.5)  # Small delay to allow you to start speaking
        command = listen()
        execute_command(command)

if __name__ == "__main__":
    main()
