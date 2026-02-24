import pyaudio
import vosk
import pygame
import google.generativeai as genai
import pyttsx3
import json
import io

#initialize pygame mixer for audio playback

pygame.mixer.init()
model_path = r"C:\Users\Geoel\OneDrive\Desktop\ema\Resources\vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)  # Ensure you have the correct path to the Vosk model
recognizer=vosk.KaldiRecognizer(model,16000)

#configure the Gemini API client
genai.configure(api_key="AIzaSyA_vGq9N5vFjpn4suG6Btcyy_yC2LsM-Ys")
# Function to play prompt audio
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# Function to convert speech to text
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
        
def emotion_analysis(text):
    text = text.lower()
    words = set(text.split())

    emotion_lexicon = {
        "angry": {
            "words": [
                "angry", "mad", "furious", "annoyed", "irritated",
                "rage", "hate", "frustrated", "outraged", "resentful"
            ],
            "weight": 3
        },
        "fear": {
            "words": [
                "scared", "afraid", "worried", "nervous", "anxious",
                "terrified", "panic", "fearful", "uneasy"
            ],
            "weight": 3
        },
        "sad": {
            "words": [
                "sad", "depressed", "unhappy", "down", "miserable",
                "cry", "lonely", "heartbroken", "disappointed"
            ],
            "weight": 2
        },
        "happy": {
            "words": [
                "happy", "great", "awesome", "good", "fantastic",
                "love", "excited", "joyful", "delighted", "pleased"
            ],
            "weight": 1
        },
        "surprise": {
            "words": [
                "wow", "really", "amazing", "unexpected",
                "shocked", "surprised"
            ],
            "weight": 1
        }
    }

    scores = {}

    for emotion, data in emotion_lexicon.items():
        score = 0
        for word in data["words"]:
            if word in words:
                score += data["weight"]
        scores[emotion] = score

    # choose highest weighted emotion
    max_emotion = max(scores, key=scores.get)

    if scores[max_emotion] == 0:
        return "neutral"

    return max_emotion
    
def gemini_api(text,emotion):
    #initialize the Gemini API client   
    model=genai.GenerativeModel("models/gemini-2.5-flash")
    prompt = f"""text: {text} emotion: {emotion}"""
    convo=model.start_chat()
    #generate a response based on input text
    response=model.generate_content(prompt)
    print(response.text,"emotion:",emotion)
    return response.text

def text_to_speech(text, voice_index=1, rate=200, volume=1.0,emotion="neutral"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #set properties
    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume) 
    #emotion-based adjustments (placeholder)
    if emotion == "happy":
        engine.setProperty('rate', 220)
    elif emotion == "sad":
        engine.setProperty('rate', 160)
    elif emotion == "angry":
        engine.setProperty('rate', 230)
    else:
        engine.setProperty('rate', 200)
    #speak the text
    engine.say(text)
    engine.runAndWait()

#-----Main----

text=listen_with_vosk()
emotion=emotion_analysis(text)
ai_response=gemini_api(text,emotion=emotion)
audio_response=text_to_speech(ai_response,emotion=emotion)


   
