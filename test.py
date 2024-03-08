from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import threading
import datetime

keyboard = KeyboardController()

def dodge_to_direction(key):
    """Presses a key for a given duration then releases it."""
    def press_and_release():
        
        keyboard.press(key)
        time.sleep(0.1)  # This blocks the thread, not the main program
        keyboard.press(Key.shift)
          # This blocks the thread, not the main program
        time.sleep(0.1)
        keyboard.release(Key.shift)
        time.sleep(0.1)
        keyboard.release(key)
        print(f"dodged to {key} direction")

    thread = threading.Thread(target=press_and_release)
    thread.start()

time.sleep(3)    
while True:
    print("dodge")
    dodge_to_direction('a', 0.3)
    time.sleep(2)
