"""
voice_assistant.py
Simple customizable voice assistant in Python (Tanglish friendly).
Features: listen, speak, time/date, wikipedia search, open websites, play youtube search,
create/read notes, simple timer, graceful exit.

Dependencies:
  pip install SpeechRecognition pyttsx3 wikipedia pyaudio
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import time
from datetime import datetime
import os
import threading

# ========== Configuration ==========
ASSISTANT_NAME = "assistant"   # wake word (or change to your name)
NOTES_DIR = "assistant_notes"  # directory to save notes
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# ========== Initialize TTS ==========
engine = pyttsx3.init()
engine.setProperty("rate", 165)   # speech speed
voices = engine.getProperty("voices")
# choose a voice index if you want (0 or 1 usually)
# engine.setProperty('voice', voices[0].id)

def speak(text):
    """Speak the given text aloud and print to console."""
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ========== Speech recognition ==========
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen(timeout=5, phrase_time_limit=7):
    """
    Listen from microphone and return recognized text (lowercase).
    Returns None on failure.
    """
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return None
    try:
        query = recognizer.recognize_google(audio, language="en-IN")
        print("You:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("Speech service error:", e)
        return None

# ========== Helper actions ==========
def tell_time():
    now = datetime.now()
    speak(now.strftime("Time is %I:%M %p"))

def tell_date():
    now = datetime.now()
    speak(now.strftime("Today is %A, %B %d, %Y"))

def open_website(site_name):
    # site_name like 'youtube' or 'google' or 'github'
    mapping = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
    }
    url = mapping.get(site_name, None)
    if url:
        speak(f"Opening {site_name}")
        webbrowser.open(url)
    else:
        # treat site_name as url or search
        if "." in site_name:
            url = site_name if site_name.startswith("http") else "https://" + site_name
            speak(f"Opening {url}")
            webbrowser.open(url)
        else:
            speak(f"Opening search for {site_name}")
            webbrowser.open("https://www.google.com/search?q=" + site_name.replace(" ", "+"))

def wikipedia_search(query):
    try:
        speak("Searching Wikipedia...")
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
        speak(summary)
    except Exception as e:
        print("Wiki error:", e)
        speak("Sorry, I could not find that on Wikipedia.")

def play_youtube(query):
    # opens a YouTube search page for the query (easier than automating playback)
    speak(f"Searching YouTube for {query}")
    url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
    webbrowser.open(url)

def write_note(text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(NOTES_DIR, f"note_{timestamp}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    speak(f"Saved note as {os.path.basename(filename)}")

def read_notes():
    files = sorted(os.listdir(NOTES_DIR))
    if not files:
        speak("No notes found.")
        return
    speak(f"I found {len(files)} notes. Reading the latest one.")
    latest = files[-1]
    with open(os.path.join(NOTES_DIR, latest), "r", encoding="utf-8") as f:
        content = f.read(800)  # read first 800 chars
    speak(f"Note {latest}: {content}")

def set_timer(seconds):
    def timer_thread(sec):
        speak(f"Timer set for {sec} seconds. I will tell you when time is up.")
        time.sleep(sec)
        speak(f"Timer finished after {sec} seconds!")
    t = threading.Thread(target=timer_thread, args=(seconds,), daemon=True)
    t.start()

# ========== Main command processor ==========
def process_command(cmd):
    if cmd is None:
        return True  # continue loop

    # wake-word handling: allow direct commands if wake present OR user typed directly
    if ASSISTANT_NAME in cmd:
        # remove wake word for simpler parsing
        cmd = cmd.replace(ASSISTANT_NAME, "").strip()

    # simple commands
    if any(x in cmd for x in ["time", "what's the time", "tell time", "current time"]):
        tell_time()
    elif any(x in cmd for x in ["date", "what's the date", "today date", "tell date"]):
        tell_date()
    elif cmd.startswith("open "):
        target = cmd.replace("open ", "", 1).strip()
        open_website(target)
    elif cmd.startswith("search wikipedia for ") or cmd.startswith("wikipedia "):
        # e.g. "search wikipedia for alan turing" or "wikipedia alan turing"
        q = cmd.replace("search wikipedia for ", "").replace("wikipedia ", "").strip()
        wikipedia_search(q)
    elif cmd.startswith("search ") or cmd.startswith("google "):
        q = cmd.replace("search ", "").replace("google ", "").strip()
        speak(f"Searching web for {q}")
        webbrowser.open("https://www.google.com/search?q=" + q.replace(" ", "+"))
    elif cmd.startswith("play ") or "youtube" in cmd:
        # "play despacito" or "play youtube despacito"
        q = cmd.replace("play ", "").replace("on youtube", "").strip()
        play_youtube(q)
    elif any(x in cmd for x in ["make a note", "take a note", "note this"]):
        # ask follow-up for note content
        speak("What would you like me to write?")
        note = listen(timeout=6, phrase_time_limit=20)
        if note:
            write_note(note)
        else:
            speak("No content heard. Note cancelled.")
    elif any(x in cmd for x in ["read note", "read notes"]):
        read_notes()
    elif "set timer" in cmd or "timer for" in cmd:
        # expected format: "set timer for 10 seconds" or "timer for 1 minute"
        import re
        m = re.search(r"(\d+)\s*(second|seconds|minute|minutes|sec|min)", cmd)
        if m:
            val = int(m.group(1))
            unit = m.group(2)
            seconds = val * 60 if "minute" in unit else val
            set_timer(seconds)
        else:
            speak("For how many seconds or minutes?")
            ans = listen(timeout=6, phrase_time_limit=6)
            if ans:
                try:
                    val = int(''.join([c for c in ans if c.isdigit()]))
                    set_timer(val)
                except:
                    speak("I couldn't parse the time.")
    elif any(x in cmd for x in ["exit", "quit", "goodbye", "stop"]):
        speak("Goodbye. Have a nice day!")
        return False  # stop loop
    else:
        # fallback: try quick web search
        speak("I didn't fully get that. Should I search the web for that?")
        ans = listen(timeout=5, phrase_time_limit=5)
        if ans and any(y in ans for y in ["yes", "y", "ok", "sure"]):
            webbrowser.open("https://www.google.com/search?q=" + cmd.replace(" ", "+"))
        else:
            speak("Okay.")

    return True  # continue loop

# ========== Main loop ==========
def main():
    speak("Hello! I am your assistant. Say 'assistant' followed by a command, or say a command directly.")
    running = True
    while running:
        cmd = listen(timeout=6, phrase_time_limit=7)
        running = process_command(cmd)
    speak("Shutting down.")

if __name__ == "__main__":
    main()
