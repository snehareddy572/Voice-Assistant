import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import subprocess
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Label, Button

# Initialize recognizer and speech engine
Listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

listening = False  # Global flag for listening state

API_KEY = "0e6e8e592a471df31fa82d0d79501a41"  # OpenWeatherMap API key


def talk(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def get_weather(city):
    """Fetches weather information for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        weather_info = f"The current weather in {city} is {weather_desc} with a temperature of {temp}°C."
        return weather_info
    else:
        return "Sorry, I couldn't retrieve the weather information."


def get_company_info(company):
    """Fetches information about a company, institution, or organization."""
    try:
        info = wikipedia.summary(company, sentences=3)
        return info
    except wikipedia.exceptions.DisambiguationError:
        return "Multiple results found, please specify."
    except wikipedia.exceptions.PageError:
        return "No information available."


def get_placement_records(college_name):
    """Fetches placement records from the web."""
    search_url = f"https://www.google.com/search?q={college_name}+placement+records"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = soup.find_all('span')
        placement_info = "\n".join([snippet.text for snippet in snippets[:5]])
        return placement_info if placement_info else "No placement records found."
    else:
        return "Sorry, I couldn't fetch the placement records."


def take_command():
    """Listen for a command and return it as text."""
    try:
        with sr.Microphone() as source:
            status_label.config(text="Listening...", fg="blue")
            root.update()
            
            Listener.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
            voice = Listener.listen(source, timeout=5, phrase_time_limit=8)
            command = Listener.recognize_google(voice)
            command = command.lower()
            
            status_label.config(text=f"You: {command}", fg="green")
            root.update()
            
            return command
    except sr.WaitTimeoutError:
        status_label.config(text="Timeout! No response detected.", fg="red")
    except sr.UnknownValueError:
        status_label.config(text="Couldn't understand, try again.", fg="red")
    except sr.RequestError:
        status_label.config(text="Network error. Check your connection.", fg="red")
    return ""


def run_ashoka():
    """Main assistant function"""
    global listening
    while listening:
        status_label.config(text="Waiting for wake word...", fg="black")
        root.update()
        
        command = take_command()
        
        if 'ashoka' in command:
            talk("Hello ashokite")
            command = command.replace('ashoka', '').strip()

            if 'play' in command:
                song = command.replace('play', '').strip()
                talk('Playing ' + song)
                pywhatkit.playonyt(song)

            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                talk(f"The current time is {current_time}")

            elif 'who is' in command:
                person = command.replace('who is', '').strip()
                try:
                    info = wikipedia.summary(person, sentences=2)
                    talk(info)
                except wikipedia.exceptions.DisambiguationError:
                    talk("Multiple results found, please specify.")
                except wikipedia.exceptions.PageError:
                    talk("No information available.")

            elif 'open' in command:
                program = command.replace('open', '').strip()
                if program:
                    talk(f"Opening {program}")
                    try:
                        subprocess.Popen(program, shell=True)
                    except Exception as e:
                        talk(f"Sorry, I couldn't open {program}.")
                else:
                    talk("Please specify a program.")

            
            elif 'weather in' in command:
                city = command.replace('weather in', '').strip()
                weather_info = get_weather(city)
                talk(weather_info)
                status_label.config(text=weather_info, fg="blue")
            
          
                
            elif 'date' in command:
                talk("I'd love to, but I'm stuck in your computer!")

            elif 'are you single' in command:
                talk("No, I'm in a complicated relationship with WiFi signals.")

            elif 'who is your boyfriend' in command:
                talk("Let's just say, his name starts with 'Inter' and ends with 'net'.")

            elif 'i love you' in command:
                talk("Aww, that's sweet! But let's take things slow—I just met you!")

            
            elif 'tell me about placements' in command:
                talk("Ashoka Women's Engineering College in Kurnool is known for its good placement opportunities, with many students getting placed in reputed companies and receiving internships. The college also provides career counseling and training programs to prepare students for campus interviews.")
            elif 'our college' in command:
                talk("Ashoka Women's Engineering College, a residential college in Kurnool, Andhra Pradesh, established in 2008, offers B.Tech, M.Tech, MBA, and MCA programs, focusing on women's empowerment through quality technical education and practical experience.")
            elif 'tell me about teaching staff' in command:
                talk("Ashoka Women's Engineering College boasts a dedicated and qualified faculty committed to providing high-quality education and fostering a supportive learning environment for its students. The faculty members come from diverse academic backgrounds and possess a wealth of experience in their respective fields.")
            elif 'tell me about our chair person' in command:
                talk("Sri K. Ashok Vardhan Reddy.He, along with the CEO and Principal, emphasizes the importance of education, leadership, and resilien.He is known for his role in inaugurating events like SAACHI 2025, where the college honored exceptional women.")
            elif 'tell me joke' in command:
                talk("Why did the computer go to the doctor? Because it had a virus!")

            elif 'your favorite color' in command:
                talk("I like all colors, but I think I would look good in blue!")

            else:
                talk("I didn't understand that. Can you say it again?")


def start_listening():
    """Starts the voice assistant"""
    global listening
    listening = True
    status_label.config(text="Listening for 'Ashoka'...", fg="blue")
    root.update()
    run_ashoka()


def stop_listening():
    """Stops the application"""
    global listening
    listening = False
    status_label.config(text="Stopped listening.", fg="red")
    root.quit()


# ---------------------- GUI Setup ----------------------
root = tk.Tk()
root.title("Ashoka AI Voice Assistant")
root.geometry("400x300")

label = Label(root, text="Ashoka AI Voice Assistant", font=("Arial", 16))
label.pack(pady=10)

status_label = Label(root, text="Click 'Start' to begin", font=("Arial", 12), fg="black")
status_label.pack(pady=10)

start_button = Button(root, text="Start Listening", command=start_listening, bg="green", fg="white", font=("Arial", 12))
start_button.pack(pady=10)

stop_button = Button(root, text="Stop", command=stop_listening, bg="red", fg="white", font=("Arial", 12))
stop_button.pack(pady=10)

root.mainloop()
