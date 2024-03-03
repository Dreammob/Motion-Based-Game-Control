from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
last_flag = None  # Track the last flag

# Maps flags to keys
mapping = {
    "00": 'a',
    "01": 'd',
    "10": 'w',
    "11": 's'  
}

def read_flag_from_file():
    try:
        with open("command_flag.txt", "r") as file:
            flag = file.read().strip()
        # Optionally clear the file after reading the flag
        with open("command_flag.txt", "w") as file:
            file.write("")
        return flag
    except FileNotFoundError:
        return None

def press_key_based_on_flag(flag, last_flag):
    key = mapping.get(flag)
    # This will prevent the InvalidKeyException for a None last_key
    last_key = mapping.get(last_flag) if last_flag else None
    
    if key:
        # If the new stage is different from the last, release the last key and press the new key
        if last_key and key != last_key:
            keyboard.release(last_key)  # Release the last key if it's different
        if not last_flag or key != last_key:  # Press the new key if it's the first time or if it has changed
            keyboard.press(key)
        # If the stage is the same as the last, we keep the key pressed and do nothing here
    else:
        # If there's no valid current key but there was a last key, release it
        if last_key:
            keyboard.release(last_key)
    return flag  # Return the current flag as the new 'last_flag' for the next cycle

while True:
    flag = read_flag_from_file()
    if flag:
        last_flag = press_key_based_on_flag(flag, last_flag)
    elif last_flag:
        # Ensure to release the last key if no new flag is provided
        last_key = mapping.get(last_flag) if last_flag else None
        if last_key:
            keyboard.release(last_key)
        last_flag = None  # Reset last_flag since no action is needed
    time.sleep(0.1)
