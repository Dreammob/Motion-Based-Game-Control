from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import threading
import datetime

keyboard = KeyboardController()

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
            time.sleep(0.05)
            pass

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

            # current_time = lines[line_index].strip().split(' || ')[0]
            # next_time_str = lines[line_index + 1].strip().split(' || ')[0]
            # next_time = datetime.datetime.strptime(next_time_str, '%Y-%m-%d %H:%M:%S.%f')

            # time_difference = next_time - curr_time
            # print(time_difference.total_seconds())

            line_index += 1  # Move to the next line for the next call

        # print(f"reading index {line_index}") # For debugging
        # print(f"last line index {len((lines))}")

    return last_flags_set, current_flags_set

def handling_action_to_keyboard(last_flags_set, current_flags_set):

    global keypressed
    for flag in current_flags_set:
        if flag not in last_flags_set:
            press_key(flag)
    
    for flag in last_flags_set:
        if flag not in current_flags_set and line_index != 0:
            release_key(flag)

def press_key(action_flag):
    global attack_prep
    
    # if action_flag == 'left turn':
    #     keyboard.press('a')
    #     keypressed.add('a')
    #     print("press a")

    # elif action_flag == 'right turn':
    #     keyboard.press('d')
    #     keypressed.add('d')
    #     print("press d")

    if action_flag == 'left_attack_norm':
        if attack_prep:
            keyboard.press('1')
            keypressed.add('1')
            print("press 1")

    if action_flag == 'walk':
        if attack_prep:
            keyboard.press('w')
            keypressed.add('w')
            print("press w")

    if action_flag == 'right_attack_norm':
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

    if action_flag == 'run':
        keyboard.press(Key.shift)
        keypressed.add(Key.shift)
        print("press shift")

# def press_key(action_flag):
#     """
#     Simulates pressing and releasing keyboard keys based on the input flags
#     using the pynput library.
    
#     Parameters:
#     flags (list): A list of flags to be processed.
#     """
#     global attack_prep

#     match action_flag:
#         # Now change to left and right move since we are using locked viewpoint
#         case 'left turn':
#             keyboard.press('a')
#             keypressed.add('a')
#             print("press a")
#             # game_controller.right_joystick_float(x_value_float=-0.5, y_value_float=0.0)
#             # game_controller.update()

#         # Now change to left and right move since we are using locked viewpoint
#         case 'right turn':
#             keyboard.press('d')
#             keypressed.add('d')
#             print("press d")
#             # game_controller.right_joystick_float(x_value_float=0.5, y_value_float=0.0)
#             # game_controller.update()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

#         case 'left_attack_norm':
#             # keyboard.press('w')
#             # keypressed.add('w')
#             # print("press w")
#             # mouse.click(Button.left, 1)
#             # print("clicked")
#             if attack_prep:
#                 keyboard.press('1')
#                 keypressed.add('1')
#                 print("press 1")
#                 # game_controller.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
#                 # game_controller.update()

#         case 'right_attack_norm':
#             # keyboard.press('w')
#             # keypressed.add('w')
#             # print("press w")
#             # mouse.click(Button.left, 1)
#             # print("clicked")
#             if attack_prep:
#                 keyboard.press('2')
#                 keypressed.add('2')
#                 print("press 2")
#                 # game_controller.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
#                 # game_controller.update()
#         case 'prepare':
#             attack_prep = True
#             # keyboard.press('s')
#             # keypressed.add('s')
#             # print("press s")

#         case 'jump':
#             keyboard.press(Key.space)
#             keypressed.add(Key.space)
#             print("press space")
#             # game_controller.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
#             # game_controller.update()

#         case 'dodge':
#             # game_controller.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
#             # game_controller.update()
#             press_key_with_delay(Key.shift, 0.3)     
         
#         case 'run':
#             # game_controller.left_joystick_float(x_value_float=0.0, y_value_float=1.0)
#             # game_controller.update()
#             keyboard.press(Key.shift)
#             keypressed.add(Key.shift)
#             print("press shift")

def release_key(action_flag):
    if action_flag == 'left turn':
        keyboard.release('a')
        if 'a' in keypressed:
            keypressed.remove('a')
        print("release a")

    if action_flag == 'right turn':
        keyboard.release('d')
        if 'd' in keypressed:
            keypressed.remove('d')
        print("release d")

    if action_flag == 'walk':
        keyboard.release('w')
        if 'w' in keypressed:
            keypressed.remove('w')
        print("release w")

    if action_flag == 'left_attack_norm':
        keyboard.release('1')
        if '1' in keypressed:
            keypressed.remove('1')
        print("release 1")

    if action_flag == 'right_attack_norm':
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

    if action_flag == 'run':
        keyboard.release(Key.shift)
        if Key.shift in keypressed:
            keypressed.remove(Key.shift)
        print("release shift")


# def release_key(action_flag):
#     match action_flag:

#         case 'left turn':
#             keyboard.release('a')
#             if 'a' in keypressed:
#                 keypressed.remove('a')
#             print("release a")
#             # game_controller.right_joystick_float(x_value_float=0.0, y_value_float=0.0)

#         case 'right turn':
#             keyboard.release('d')
#             if 'a' in keypressed:
#                 keypressed.remove('d')
#             print("release d")

#         case 'left_attack_norm':
#             keyboard.release('1')
#             if 'w' in keypressed:
#                 keypressed.remove('1')
#             print("release 1")
#             # game_controller.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
#             # game_controller.update()

#         case 'right_attack_norm':
#             keyboard.release('2')
#             if 'w' in keypressed:
#                 keypressed.remove('2')
#             print("release 2")

#         case 'prepare':
#             attack_prep = False
#         #     keyboard.release('s')
#         #     if 's' in keypressed:
#         #         keypressed.remove('s')
#         #     print("release s")

#         case 'jump':
#             # game_controller.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
#             # game_controller.update()

#             keyboard.release(Key.space)
#             if Key.space in keypressed:
#                 keypressed.remove(Key.space)
#             print("release space")

#         # case 'dodge':
#         #     game_controller.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
#         #     game_controller.update()
            
#         case 'run':
#             # game_controller.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
#             keyboard.release(Key.shift)
#             if Key.shift in keypressed:
#                 keypressed.remove(Key.shift)
#             print("release shift")

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


def clear_file_contents(filename):
    with open(filename, 'w') as file:
        pass  # Opening in 'w' mode and closing it clears the file

# Main loop
time.sleep(3)

with open(file_path, 'w') as file:
    pass  # No need to write anything, opening in 'w' mode truncates the file

while line_index >= 0:
    last_flags_set, current_flags_set = read_flags_from_file(file_path)
    handling_action_to_keyboard(last_flags_set, current_flags_set)
    print(line_index)

    # print(last_flags_set)
    # print("\n")
    # print(current_flags_set)



print("Sync stop, cleaning up")

for key in keypressed:

    print(f"Released {key}")
    # press_key(key)
    keyboard.release(key)
    # time.sleep(0.1)  # Wait for 1 second before checking the file again

