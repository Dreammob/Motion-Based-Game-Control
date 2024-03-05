from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
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
    '00': 'a',
    '01': 'd'
}

file_path = "command_flag.txt"
line_index = 0  # Define line_index globally outside any function


def read_flags_from_file(file_path):
    """
    Reads lines from a given file starting from a global index and extracts the flags.
    It updates the global index after reading a line, and returns both the current
    and last flags as strings.

    Parameters:
    file_path (str): The path to the file from which to read the flags.

    Returns:
    tuple: A tuple containing two strings: (last_flags_str, current_flags_str),
           where both elements are strings of flags from the respective lines.
    """
    global line_index  # Declare 'line_index' as global to modify it
    current_flags_str = ""  # Initialize the current flags string
    last_flags_str = ""  # Initialize the last flags string

    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines

        if line_index > 0 and line_index < len(lines):
            # Get last line flags if line_index is greater than 0
            last_line = lines[line_index - 1].strip()
            last_flags = last_line.split(' - ')[-1].split() if last_line else []
            last_flags_str = ' '.join(last_flags)  # Convert list to string

        if line_index < len(lines):  # Check if the index is within the file length
            current_line = lines[line_index].strip()  # Read the line at the current index
            current_flags = current_line.split(' - ')[-1].split() if current_line else []
            current_flags_str = ' '.join(current_flags)  # Convert list to string
            line_index += 1  # Move to the next line for the next call

    return last_flags_str, current_flags_str  # Return both last and current flags as strings


def press_key(last_flags, current_flags):
    """
    Simulates pressing and releasing keyboard keys based on the input flags
    using the pynput library.
    
    Parameters:
    flags (list): A list of flags to be processed.
    """

    
    # Assign current and last keys based on flags
    last_key = flag_to_key.get(last_flags)
    current_key = flag_to_key.get(current_flags)

    if last_key is None or current_key is None:
        # print(f"One of the flags is not mapped to a key.")
        return
    
    # If the keys are different, simulate releasing the last key and pressing the new key
    if last_key != current_key:
        # print(f"Releasing '{last_key}' and pressing '{current_key}'.")
        # To simulate key press actions, use the following (commented out for safety):
        keyboard.release(last_key)
        keyboard.press(current_key)
        # keyboard.release(current_key)
    else:
        # If the keys are the same, simulate keeping the key pressed
        # print(f"Keeping '{current_key}' pressed.")
        # For a real key press, you might only press without releasing here:
        keyboard.press(current_key)
        
        # And somewhere else in your code, you would release it when needed.
        # keyboard.release(current_key)

# Main loop
while True:
    last_flags, current_flags = read_flags_from_file(file_path)
    # print(last_flags, current_flags)
    # if len(flags) == 2 and flags[0] != flags[1]:
    #     # If the last two flags are different, press the key corresponding to the last flag
    press_key(last_flags, current_flags)
    # elif len(flags) == 2:
    #     # If the last two flags are the same, it implies keeping the same key pressed
    #     # For simplicity, we simulate pressing it once here
    #     print(f"Keeping '{flag_to_key.get(flags[-1])}' pressed.")
    #     # keyboard.press(flag_to_key.get(flags[-1]))
    #     # keyboard.release(flag_to_key.get(flags[-1]))
    
    time.sleep(0.1)  # Wait for 1 second before checking the file again