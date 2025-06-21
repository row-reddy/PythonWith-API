import tkinter as tk
import requests
import pyttsx3 as py
import speech_recognition as sr



from gui_api import get_joke_button, setup_label
en = py.init()

voices = en.getProperty('voices')
en.setProperty('voice', voices[1].id)  # Change index if needed
en.setProperty('rate', 160)

def speak(text):
    en.say(text)
    en.runAndWait()


def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    if response.status_code == 200:
        joke = response.json()
        setup_label.config(text = "Joke:" + joke["setup"])
        punchline_label.config(text = "Answer:" + joke["punchline"])
        window.update_idletasks()
        speak(joke["setup"]+"................"+joke["punchline"])
    else:
        setup_label.config(text = "failed to get joke")
        punchline_label.config(text = "Status:" + str(response.status_code))
def listen_and_tell_joke():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say 'joke' to hear one.")
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)

        if "joke" in command.lower():
            get_joke()
        else:
            speak("I didn't hear the word joke.")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
    except sr.RequestError:
        speak("Sorry, speech service is unavailable.")

window = tk.Tk()
window.title("🎤 Joke Teller")
window.title("Joke")
window.geometry("500x500")



get_joke_button = tk.Button(window, text="Get Joke", command=get_joke)
get_joke_button.pack(pady=50)

mic_button = tk.Button(window, text="🎙️ Speak 'joke'", command=listen_and_tell_joke, font=("Arial", 12), bg="orange")
mic_button.pack(pady=10)

setup_label = tk.Label(window,text="",font=("Arial", 12),wraplength=200)
setup_label.pack(pady=15)

punchline_label = tk.Label(window,text="",font=("Arial", 12,"bold"),wraplength=200)
punchline_label.pack(pady=15)

window.mainloop()