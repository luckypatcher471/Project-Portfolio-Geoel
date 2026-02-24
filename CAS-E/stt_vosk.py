#tts vosk
import vosk
import pyaudio
import json
import pygame

pygame.mixer.init()

model_path = r""

model = vosk.Model(model_path)  # Ensure you have the correct path to the Vosk model
recognizer = vosk.KaldiRecognizer(model, 16000)

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

def listen_with_vosk():
    mic=pyaudio.PyAudio()
    stream=mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Listening...")
    play_sound("resources/prompts/listening.mp3")
    while True:
        data=stream.read(8192)
        if len(data)==0:
            continue
        if recognizer.AcceptWaveform(data):
            play_sound("resources/prompts/processing.mp3")
            result=recognizer.Result()
            text=json.loads(result).get("text","")
            print("You said:"+text)
            return text
        
#--main--
while True:
    listen_with_vosk()
    

       
