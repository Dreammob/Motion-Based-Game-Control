from pynput.keyboard import Key, Controller, Listener
import time

keyboard = Controller()

def read_flag_from_file():
    try:
        with open("command_flag.txt", "r") as file:
            flag = file.read().strip()
        # Clear the file after reading the flag
        with open("command_flag.txt", "w") as file:
            file.write("")
        return flag
    except FileNotFoundError:
        return None

def press_key_based_on_flag(flag):
    # Maps flags to keys
    mapping = {
        "00": 'a',
        "01": 'd',
        "10": 'w',
        "11": 's'  
    }
    
    key = mapping.get(flag)
    if key:
        keyboard.press(key)
        time.sleep(1)  # Hold the key for a bit
        keyboard.release(key)

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Start listening for the ESC key
listener = Listener(on_release=on_release)
listener.start()

while True:
    flag = read_flag_from_file()
    if flag:
        time.sleep(1)
        press_key_based_on_flag(flag)
    time.sleep(1)  # Check the file every 0.5 seconds
