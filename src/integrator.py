from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import threading
import datetime

keyboard = KeyboardController()
mouse = MouseController()

# last_command = None  # To track the last command processed

# def read_last_commands(n=10):
#     """Reads the last n lines from the command_flag.txt file."""
#     try:
#         with open("command_flag.txt", "r") as file:
#             lines = file.readlines()
#             # Return the last n lines
#             return lines[-n:]
#     except FileNotFoundError:
#         return []

# def extract_command(line):
#     """Extracts the command from a line."""
#     # Assumes the line format is "YYYY-MM-DD HH:MM:SS - CMD"
#     return line.strip().split(" - ")[-1]

# def process_commands(commands):
#     global last_command
#     # Extract commands from the last few lines
#     extracted_commands = [extract_command(cmd) for cmd in commands if cmd.strip()]

#     # Determine the current command: assume the most frequent command in the last few lines
#     if extracted_commands:
#         current_command = max(set(extracted_commands), key=extracted_commands.count)
#     else:
#         current_command = None

#     # Maps commands to keys
#     command_mapping = {
#         "00": 'a',
#         "01": 'd',
#         # Add other mappings as necessary
#     }
    
#     if current_command != last_command:
#         # Release the previous key if there was one
#         if last_command is not None and last_command in command_mapping:
#             keyboard.release(command_mapping[last_command])
#         # Press the new key if the command has changed
#         if current_command in command_mapping:
#             keyboard.press(command_mapping[current_command])
#             time.sleep(0.1)  # Optional: hold the key for a bit before releasing, if needed for your application
#             keyboard.release(command_mapping[current_command])
#         # Update the last command processed
#         last_command = current_command

# while True:
#     commands = read_last_commands(10)  # Read the last 10 lines; adjust as needed
#     process_commands(commands)
#     time.sleep(0.04)  # Adjust the sleep time as necessary

flag_to_key = {
    'left turn': 'a',
    'attack': 'w',
    'prepare': 's',
    'jump': 'space',
    'dodge': 'shift',
    'idle': None

}

file_path = "command_flag.txt"
line_index = 0  # Define line_index globally outside any function
attack_prep = False
keypressed = set()

def read_flags_from_file(file_path):
    global line_index  # Declare 'line_index' as global to modify it
    current_flags_set = set()  # Initialize the current flags string
    last_flags_set = set()  # Initialize the last flags string

   
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines
        if len(lines) < 2 or line_index >= len(lines)-1:
            time.sleep(0.3)
            pass

        else:
            # Get last line flags if line_index is greater than 0
            last_line = lines[line_index - 1].strip().split(' || ')[1] 
            
            if last_line:
                last_flags = last_line.split(' - ')
                for flag in last_flags:
                    last_flags_set.add(flag)
            # last_flags = last_line.split(' - ')[-1].split() if last_line else []
            # last_flags_str = ' '.join(last_flags)  # Convert list to string

            current_line = lines[line_index].strip().split(' || ')[1]  # Read the line at the current index
            curr_time_str = lines[line_index].strip().split(' || ')[0]
            curr_time = datetime.datetime.strptime(curr_time_str, '%Y-%m-%d %H:%M:%S.%f')

            if current_line:
                current_flags = current_line.split(' - ')
                for flag in current_flags:
                    current_flags_set.add(flag)

            # current_time = lines[line_index].strip().split(' || ')[0]
            next_time_str = lines[line_index + 1].strip().split(' || ')[0]
            next_time = datetime.datetime.strptime(next_time_str, '%Y-%m-%d %H:%M:%S.%f')

            time_difference = next_time - curr_time
            # print(time_difference.total_seconds())

            time.sleep(0.1)
        print(line_index ) # For debugging
        print(len((lines)))
    return last_flags_set, current_flags_set  # Return both last and current flags as strings

def handling_action_to_keyboard(last_flags_set, current_flags_set):

    global keypressed
    for flag in current_flags_set:
        if flag not in last_flags_set:
            press_key(flag)
    
    for flag in last_flags_set:
        if flag not in current_flags_set and line_index != 0:
            release_key(flag)

    # time.sleep(0.05)




def press_key(action_flag):
    """
    Simulates pressing and releasing keyboard keys based on the input flags
    using the pynput library.
    
    Parameters:
    flags (list): A list of flags to be processed.
    """
    global attack_prep
    match action_flag:
        case 'left turn':
            keyboard.press('a')
            keypressed.add('a')
            print("press a")
        case 'attack':
            # keyboard.press('w')
            # keypressed.add('w')
            # print("press w")
            if attack_prep:
                # mouse.click(Button.left, 1)
                # print("clicked")
                move_mouse_right_by_100_pixels()

        case 'prepare':
            # keyboard.press('s')
            # keypressed.add('s')
            # print("press s")
            attack_prep = True

        case 'jump':
            keyboard.press(Key.space)
            keypressed.add(Key.space)
            print("press space")
        case 'dodge':
            press_key_with_delay(Key.shift, 0.3)        
        case 'run':
            keyboard.press(Key.shift)
            keypressed.add(Key.shift)
            print("press shift")


def release_key(action_flag):
    match action_flag:
        case 'left turn':
            keyboard.release('a')
            if 'a' in keypressed:
                keypressed.remove('a')
            print("release a")

        # case 'attack':
        #     keyboard.release('w')
        #     if 'w' in keypressed:
        #         keypressed.remove('w')
        #     print("release w")

        # case 'prepare':
        #     keyboard.release('s')
        #     if 's' in keypressed:
        #         keypressed.remove('s')
        #     print("release s")

        case 'jump':
            keyboard.release(Key.space)
            if Key.space in keypressed:
                keypressed.remove(Key.space)
            print("release space")

        case 'run':
            keyboard.release(Key.shift)
            if Key.shift in keypressed:
                keypressed.remove(Key.shift)
            print("release shift")

def press_key_with_delay(key, duration):
    """Presses a key for a given duration then releases it."""
    def press_and_release():
        keyboard.press(key)
        time.sleep(duration)  # This blocks the thread, not the main program
        keyboard.release(key)
        print(f"Key {key} released after {duration} seconds.")
    
    thread = threading.Thread(target=press_and_release)
    thread.start()

def clear_file_contents(filename):
    with open(filename, 'w') as file:
        pass  # Opening in 'w' mode and closing it clears the file

def move_mouse_right_by_100_pixels():
    # Get the current position of the mouse
    current_x, current_y = mouse.position
    # Move the mouse to right by 100 pixels (add 100 to the current x-coordinate)
    new_x = current_x + 100
    mouse.position = (new_x, current_y)

# Now call the function to move the mouse
move_mouse_right_by_100_pixels()

# Main loop
time.sleep(3)

with open(file_path, 'w') as file:
    pass  # No need to write anything, opening in 'w' mode truncates the file

while line_index >= 0:
    last_flags_set, current_flags_set = read_flags_from_file(file_path)
    handling_action_to_keyboard(last_flags_set, current_flags_set)

    print(last_flags_set)
    print("\n")
    print(current_flags_set)

    line_index += 1  # Move to the next line for the next call


print("Sync stop, cleaning up")

for key in keypressed:

    print(f"Released {key}")
    # press_key(key)
    keyboard.release(key)
    # time.sleep(0.1)  # Wait for 1 second before checking the file again

