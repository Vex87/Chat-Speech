TEMP_PATH = "__temp__"
TTS_PATH = "__temp__/tts.mp3"

import speech_recognition as sr
import os
from gtts import gTTS 
import playsound
import threading
import queue

r = sr.Recognizer()

def create_queue(callback):
    new_queue = queue.Queue()
    threading.Thread(
        target = callback,
        args = (new_queue,),
        daemon = True
    ).start()

    return new_queue

def delete_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def say_message(message: str):
    audio = gTTS(text = message, lang = "en", tld = "com", slow = False) 
    if not os.path.isdir(TEMP_PATH):
        os.mkdir(TEMP_PATH)
    delete_contents(TEMP_PATH)
    audio.save(TTS_PATH) 
    playsound.playsound(TTS_PATH)

def copy_to_clip_board(text):
    command = "echo " + text.strip() + "| clip"
    os.system(command)

def watch_voice(voice_queue):
    while True:
        with sr.Microphone() as source:
            print("listening...")
            text = r.listen(source)

            try:
                text = r.recognize_google(text)
            except sr.UnknownValueError:
                print("Cannot understand")
                continue
            except sr.RequestError as error_message:
                print(f"Could not get results from Google Speech Recognition service: {error_message}")

            if text and text != "":
                voice_queue.put(text)

def __main__():
    global voice_queue
    voice_queue = create_queue(watch_voice)

    while True:
        text = (voice_queue.qsize() > 0) and voice_queue.get()
        if text:
            copy_to_clip_board(text)
            print(f"> {text}")
            say_message(text)

if __name__ == "__main__":
    __main__()

