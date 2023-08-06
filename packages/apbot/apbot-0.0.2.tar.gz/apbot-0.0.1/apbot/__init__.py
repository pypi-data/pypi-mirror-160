import pyautogui
import time
import webbrowser
import cv2
import requests
from tkinter import *
import threading
from pynput.keyboard import Controller
import pywhatkit




class ap:

    def thread(funtion, args=None):
        t = threading.Thread(target=function, args=args)
        t.daemon = True
        t.start()

    def screenshot(region):
        if region:
            return pyautogui.screenshot(region=region)

    def show(window_name, picture):
        pic = cv2.imread(picture)
        cv2.imshow(window_name, pic)
        cv2.waitKey(1)

    def wait(delay):
        time.sleep(delay)

    def search_youtube(name):
        pywhatkit.playonyt(name)

    def get_site_content(site):
        return requests.get(site).content
        
    class bot:
        def current_position():
            pyautogui.displayMousePosition()

        def position():
            return pyautogui.position()

        def open_website(website):
            webbrowser.open(website)
        global keyboard
        keyboard = Controller()
        def left_click(x, y):
            pyautogui.leftClick(x,y)

        def type(text, delay):
            for char in str(text):
                keyboard.press(char)
                time.sleep(delay)

        def press(key):
            keyboard.press(key)

        def move(x, y):
            pyautogui.move(x, y)
        def moveTo(x, y):
            pyautogui.moveTo(x, y)

        


    

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

        def button(frame, text, command, x, y, font):
            btn = Button(master=frame, text=text, command=command, font=font)
            btn.place(x, y)
            frame.update()
        def label( frame, text, x, y, font):
            lbl = Label(frame, text=text, font=font)
            lbl.place(x=x, y=y)
            frame.update()
        def entry(frame, width, font,  x, y):
            
            btn = Button(frame, width=width, font=font)
            btn.place(x=x, y=y)
            frame.update()

        def frame(frame, location, size):
            thing = Frame(frame, width=size[0], height=size[1])
            thing.place(x=location[0], y=location[1])

        def clear(frame):
            for widget in frame.winfo_children():
                widget.destroy()

        def loop(frame):
            frame.mainloop()




