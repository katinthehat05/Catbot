import pygame
from player import Player
import threading
import speech_recognition as sr
import pyttsx3
import openai
import APIKEY

# Initialize Pygame
pygame.init()
DISPLAY_W, DISPLAY_H = 250, 250
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
clock = pygame.time.Clock()
house = pygame.image.load('imagee.png').convert()

# Initialize the player
cat = Player()


API_KEY = APIKEY.APIKEY
openai.api_key = API_KEY
chat_log = []


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except Exception as e:
        print("Error:", e)
        return ""

def Catbot():
    global chat_log
    while True:
        user_message = listen()
        if user_message.lower() == "quit":
            break
        else:
            chat_log.append({"role": "user", "content": user_message})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_log
            )
            assistant_response = response['choices'][0]['message']['content']
            clean_assistant_response = assistant_response.strip("\n").strip()
            print("Catbot:", clean_assistant_response)
            chat_log.append({"role": "assistant", "content": clean_assistant_response})
            speak(clean_assistant_response)

def speak(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()


def start_Catbot():
    catbot_thread = threading.Thread(target=Catbot)
    catbot_thread.daemon = True
    catbot_thread.start()


start_Catbot()


running = True
while running:
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY, cat.FACING_LEFT = True, True
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY, cat.FACING_LEFT = True, False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY = False
    
    # Update player
    cat.update()
   
    # Drawing
    canvas.blit(house, (0,0))
    cat.draw(canvas)
    window.blit(canvas, (0,0))
    pygame.display.update()