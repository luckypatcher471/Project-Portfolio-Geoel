#Stt.py - Speech-to-Text using Google Speech Recognition API

import speech_recognition as sr
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Function to play prompt audio
def play_sound(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to convert speech to text
def listen_with_google():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        play_sound('resources/prompts/listening.mp3')

        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        print("Processing...")
        play_sound('resources/prompts/processing.mp3')

        # Convert speech to text using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text


# Main execution block
if __name__ == "__main__":
    try:
        result = listen_with_google()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google service: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")