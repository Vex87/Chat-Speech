import speech_recognition as sr
import os

r = sr.Recognizer()

def copy_to_clip_board(text):
    command = "echo " + text.strip() + "| clip"
    os.system(command)

while True:
    with sr.Microphone() as source:
        print("listening...")

        text = None
        while not text and text != "":
            text = r.listen(source)

        try:
            text = r.recognize_google(text)
            copy_to_clip_board(text)
            print(f"> {text}")
        except Exception as error_message:
            print(error_message)

