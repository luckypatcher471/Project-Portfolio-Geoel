#tts
import pyttsx3

def text_to_speech(text, voice_index=1, rate=200, volume=1.0):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #set properties
    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    #speak the text
    engine.say(text)
    engine.runAndWait()

#-----Main-----
text="Hello, how are you?"
text_to_speech(text)