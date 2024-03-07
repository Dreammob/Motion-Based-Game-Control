from pynput.keyboard import Controller, Key
import time

# Initialize the keyboard controller
keyboard = Controller()

# Function to press a key
def press_key(key):
    keyboard.press(key)
    # Do not call release; the key remains pressed

# Function to release a key
def release_key(key):
    keyboard.release(key)

# Example usage:
# To keep the 'a' key pressed
press_key('a')
# Remember, 'a' will remain pressed until you call release_key('a')

while True:
        # time.sleep(1)  # Wait for 1 second before checking the file again
        print()