import pyautogui
import time
import webbrowser
import cv2
import requests
from tkinter import *
import threading
from pynput.keyboard import Controller
import pywhatkit
import os
import win32api, win32con
import keyboard
import pyttsx3
from googletrans import Translator
from PIL import Image
import speech_recognition as sr
import numpy as np




class ap:
    class steve:
        class steve:
            class steve:
                class steve:
                    class steve:
                        class steve:
                            class steve:
                                class steve:
                                    class steve:
                                        class steve:
                                            class steve:
                                                class steve:
                                                    class steve:
                                                        class steve:
                                                            class steve:
                                                                class steve:
                                                                    class steve:
                                                                        class steve:
                                                                            class steve:
                                                                                class steve:
                                                                                    class steve:
                                                                                        class steve:
                                                                                            class steve:
                                                                                                class steve:
                                                                                                    class steve:
                                                                                                        class steve:
                                                                                                            class steve:
                                                                                                                class steve:
                                                                                                                    class steve:
                                                                                                                        class steve:
                                                                                                                            class steve:
                                                                                                                                class steve:
                                                                                                                                    class steve:
                                                                                                                                        class steve:
                                                                                                                                            class steve:
                                                                                                                                                class steve:
                                                                                                                                                    class steve:
                                                                                                                                                        class steve:
                                                                                                                                                            class steve:
                                                                                                                                                                class steve:
                                                                                                                                                                    class steve:
                                                                                                                                                                        class steve:
                                                                                                                                                                            class steve:
                                                                                                                                                                                class steve:
                                                                                                                                                                                    class steve:
                                                                                                                                                                                        class steve:
                                                                                                                                                                                            class steve:
                                                                                                                                                                                                class steve:
                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                                                                                                    class steve:
                                                                                                                                                                                                                                                                                                                        class steve:
                                                                                                                                                                                                                                                                                                                            class steve:
                                                                                                                                                                                                                                                                                                                                class steve:
                                                                                                                                                                                                                                                                                                                                    def steve1():
                                                                                                                                                                                                                                                                                                                                        def robotic_speech(text, gender=0):
                                                                                                                                                                                                                                                                                                                                            engine = pyttsx3.init()
                                                                                                                                                                                                                                                                                                                                            voices = engine.getProperty('voices')
                                                                                                                                                                                                                                                                                                                                            engine.setProperty('voice', voices[gender].id)
                                                                                                                                                                                                                                                                                                                                            engine.say(text)
                                                                                                                                                                                                                                                                                                                                            engine.runAndWait()

                                                                                                                                                                                                                                                                                                                                        robotic_speech('We are the many steves')
                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                        def steve2():
                                                                                                                                                                                                                                                                                                                                            while True:
                                                                                                                                                                                                                                                                                                                                                robotic_speech('Steve')
                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                        t = threading.Thread(target=steve2)
                                                                                                                                                                                                                                                                                                                                        t.start()
                                                                                                                                                                                                                                                                                                                                        

                                    

    def list_screen_size():
        return pyautogui.size()

    def calculator(problem):
        return eval(problem)

    def translate(text, target):
        translator = Translator()
        new_text, origin = translator.translate(text=text, dest=target).text, translator.translate(text=text, dest=target).origin, translator.translate(text=text, dest=target)
        return new_text, origin

    class images:
        def show_image(window_name, picture):
            pic = cv2.imread(picture)
            cv2.imshow(window_name, pic)
            cv2.waitKey(1)

        def load_image(image):
            return cv2.imread(image)

        x, y = pyautogui.size()

        def screenshot(region=(0,0, x, y)):
            return pyautogui.screenshot(region=region)

        def save_image(image, image_name, file_type):
            image.save(f'{image_name}.{file_type}')

        #def compare_images_probability(img1, img2):
        #    img1, img2 = cv2.imread(img1), cv2.imread(img2)
        #    height = 288
        #    width = 512
        #    img1 = cv2.resize(img1, (width, height))
        #    img2 = cv2.resize(img2, (width, height))
        #    A = np.zeros(img1, np.uint8)
        #    B = np.zeros(img2, np.uint8)
        #    errorL2 = cv2.norm( A, B, cv2.NORM_L2 )
        #    similarity = 1 - errorL2 / ( height * width )
        #    print('Similarity = ',similarity)
#
        #def find_differences():
        #    pass


    #def detect_language(text):
    #    translator = Translator()
    #    print(translator.detect(text))
    #    return translator.detect(text)

    def robotic_speech(text, gender=0):

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[gender].id)
        engine.say(text)
        engine.runAndWait()

    def listen_for_speech():
        while True:
            try:
                with sr.Microphone() as source:
                    r = sr.Recognizer()
                    text = r.listen(source)
                    text = r.recognize_google(text)
                    if text:
                        return text
            except:
                pass

    def list_dir(directory):
        for (name, dirs, files) in os.walk(directory):
            return name, dirs, files

    def thread(funtion, args=None):
        t = threading.Thread(target=funtion, args=args)
        t.daemon = True
        t.start()

    def wait(delay):
        time.sleep(delay)

    def search_youtube(name):
        pywhatkit.playonyt(name)

    def get_site_content(site):
        return requests.get(site).content

    def get_site(site):
        return requests.get(site)
        
    class bot:


        def macro(delay,x='',y='', image='', amount=0, stop_key='q'):
            def click():
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            if x and y:
                pyautogui.moveTo(x,y)
                if amount != 0:
                    for i in range(amount):
                        click()
                        time.sleep(delay)
                        if keyboard.is_pressed(stop_key):
                            break
                else:
                    while keyboard.is_pressed(stop_key) == False:
                        click()
                        time.sleep(delay)
            elif image:
                location = pyautogui.locateOnScreen(image)
                pyautogui.moveTo(location[0],location[1])
                if amount != 0:
                    for i in range(amount):
                        click()
                        time.sleep(delay)
                        if keyboard.is_pressed(stop_key):
                            break
                else:
                    while keyboard.is_pressed(stop_key) == False:
                        click()
                        time.sleep(delay)
            else:
                if amount != 0:
                    for i in range(amount):
                        click()
                        time.sleep(delay)
                        if keyboard.is_pressed(stop_key):
                            break
                else:
                    while keyboard.is_pressed(stop_key) == False:
                        click()
                        time.sleep(delay)
                    

        def current_position():
            pyautogui.displayMousePosition()

        def position():
            return pyautogui.position()

        def open_website(website):
            webbrowser.open(website)
        global keyboard1
        keyboard1 = Controller()
        def left_click(x, y):
            pyautogui.leftClick(x,y)

        def type(text, delay):
            for char in str(text):
                keyboard1.press(char)
                time.sleep(delay)

        def press(key):
            keyboard1.press(key)

        def move(x, y):
            pyautogui.move(x, y)

        def moveTo(x, y):
            pyautogui.moveTo(x, y)

        def scroll(amount):
            pyautogui.scroll(amount)

    class window:

        def __init__(self, title, icon, frame):
            
            frame.iconbitmap(icon)
            frame.title(title)
            frame.geometry('500x500')

        def create():

            root = Tk()
            return root
            

        def geometry(x, y, frame):
            frame.geometry(f'{x}x{y}')

        def unknown():
            pass
        def button(frame, text='', command=unknown, x=0, y=0, font=('Helvetica', 20)):
            btn = Button(master=frame, text=text, command=command, font=font)
            btn.place(x, y)
            frame.update()
        def label(frame, text='', x=0, y=0, font=('Helvetica', 20)):
            lbl = Label(frame, text=text, font=font)
            lbl.place(x=x, y=y)
            frame.update()
        def entry(frame, width=5, font=('Helvetica', 20),  x=0, y=0):
            
            btn = Button(frame, width=width, font=font)
            btn.place(x=x, y=y)
            frame.update()

        def frame(frame, location=[0,0], size=[100,100]):
            thing = Frame(frame, width=size[0], height=size[1])
            thing.place(x=location[0], y=location[1])

        def clear(frame):
            for widget in frame.winfo_children():
                widget.destroy()

        def loop(frame):
            frame.mainloop()



#ap.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve.steve1()