from pynput.keyboard import Key, Controller as KeyboardController
import time
import threading
import datetime

keyboard = KeyboardController()

file_path = "command_flag.txt"
line_index = 0  # Define line_index globally outside any function
attack_prep = False
keypressed = set()


def read_flags_from_file(file_path):
    global line_index 
    current_flags_set = set()
    last_flags_set = set()

    with open(file_path, 'r') as file:

        lines = file.readlines()

        # If excess the end of file, wait 0.05 for write into file.
        if len(lines) < 2 or line_index >= len(lines)-1:
            time.sleep(0.05)
            pass
        
        # Else read this line and move to next line.
        else:
            last_line = lines[line_index - 1].strip().split(' || ')[1] 
            
            if last_line:
                last_flags = last_line.split(' - ')
                for flag in last_flags:
                    last_flags_set.add(flag)

            current_line = lines[line_index].strip().split(' || ')[1]

            # curr_time_str = lines[line_index].strip().split(' || ')[0]
            # curr_time = datetime.datetime.strptime(curr_time_str, '%Y-%m-%d %H:%M:%S.%f')

            if current_line:
                current_flags = current_line.split(' - ')
                for flag in current_flags:
                    current_flags_set.add(flag)

            line_index += 1
            # current_time = lines[line_index].strip().split(' || ')[0]
            # next_time_str = lines[line_index + 1].strip().split(' || ')[0]
            # next_time = datetime.datetime.strptime(next_time_str, '%Y-%m-%d %H:%M:%S.%f')

            # time_difference = next_time - curr_time
            # print(time_difference.total_seconds())
           

        # print(f"reading index {line_index}") # For debugging
        # print(f"last line index {len((lines))}")

    return last_flags_set, current_flags_set

'''
Handle what action need to be done with flags of last frame and current frame as input
compare two lines flags, if one action was in last frame but not this, release the 
corresponding key, then if one action is in current frame but not this, press the key.
'''
def handling_action_to_keyboard(last_flags_set, current_flags_set):

    global keypressed
    for flag in current_flags_set:
        if flag not in last_flags_set:
            press_key(flag)
    
    for flag in last_flags_set:
        if flag not in current_flags_set and line_index != 0:
            release_key(flag)

''' 
press the key for input flag, if flag is dodge, call the function to handle it.
'''
def press_key(action_flag):
    global attack_prep
    
    if action_flag == 'turn_left':
        keyboard.press('3')
        keypressed.add('3')
        print("press 3")

    if action_flag == 'turn_right':
        keyboard.press('4')
        keypressed.add('4')
        print("press 4")

    if action_flag == 'attack_norm_left':
        if attack_prep:
            keyboard.press('1')
            keypressed.add('1')
            print("press 1")

    if action_flag == 'walk':
        if attack_prep:
            keyboard.press('w')
            keypressed.add('w')
            print("press w")

    if action_flag == 'attack_norm_right':
        if attack_prep:
            keyboard.press('2')
            keypressed.add('2')
            print("press 2")

    if action_flag == 'prepare':
        attack_prep = True

    if action_flag == 'jump':
        keyboard.press(Key.space)
        keypressed.add(Key.space)
        print("press space")

    if action_flag == 'dodge_right':
        dodge_to_direction('d')

    if action_flag == 'dodge_left':
        dodge_to_direction('a')

    # if action_flag == 'run':
    #     keyboard.press(Key.shift)
    #     keypressed.add(Key.shift)
    #     print("press shift")

'''
Release the key for the input flag.
'''
def release_key(action_flag):
    if action_flag == 'turn_left':
        keyboard.release('3')
        if '3' in keypressed:
            keypressed.remove('3')
        print("release 3")

    if action_flag == 'turn_right':
        keyboard.release('4')
        if '4' in keypressed:
            keypressed.remove('4')
        print("release 4")

    if action_flag == 'walk':
        keyboard.release('w')
        if 'w' in keypressed:
            keypressed.remove('w')
        print("release w")

    if action_flag == 'attack_norm_left':
        keyboard.release('1')
        if '1' in keypressed:
            keypressed.remove('1')
        print("release 1")

    if action_flag == 'attack_norm_right':
        keyboard.release('2')
        if '2' in keypressed:
            keypressed.remove('2')
        print("release 2")

    if action_flag == 'prepare':
        attack_prep = False

    if action_flag == 'jump':
        keyboard.release(Key.space)
        if Key.space in keypressed:
            keypressed.remove(Key.space)
        print("release space")

    # if action_flag == 'run':
    #     keyboard.release(Key.shift)
    #     if Key.shift in keypressed:
    #         keypressed.remove(Key.shift)
    #     print("release shift")

'''
Helper function for handling dodge to certain input direction.
'''
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

'''
Helper function for cleaning up written flag file for sync with camera input
'''
def clear_file_contents(filename):
    with open(filename, 'w') as file:
        pass  # Opening in 'w' mode and closing it clears the file


'''
Integrator start, wait 3 secs for switch screen focus to Elden Ring.
'''
time.sleep(3)

clear_file_contents(file_path)

'''
Main loop
'''
while line_index >= 0:
    last_flags_set, current_flags_set = read_flags_from_file(file_path)
    handling_action_to_keyboard(last_flags_set, current_flags_set)
    # print(line_index)
    # print(last_flags_set)
    # print("\n")
    # print(current_flags_set)



print("Sync stop, cleaning up")

for key in keypressed:

    print(f"Released {key}")
    # press_key(key)
    keyboard.release(key)
    # time.sleep(0.1)  # Wait for 1 second before checking the file again

