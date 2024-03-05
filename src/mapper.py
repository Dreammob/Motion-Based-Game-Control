# Maps recognized gestures to specific keyboard or mouse actions.
# This script should define a mapping from gestures identified by `classifier.py` to the corresponding game controls.
# It might use a library like `pyautogui` or `pyinput` to simulate these keyboard/mouse inputs.
# This script maps commands to flags and writes them to a file.
# mapper.py
import sys

def command_to_flag(command):
    mapping = {
        "turn left": "00",
        "turn right": "01",
        "move forward": "10",
        "move backward": "11"
    }
    return mapping.get(command, "Error: Command not found")

def write_flag_to_file(flag):
    with open("command_flag.txt", "w") as file:
        file.write(flag)

if __name__ == "__main__":
    while True:  # Keep running until the user decides to exit
        command = input("Enter command (or type 'exit' to quit): ")
        if command.lower() == 'exit':  # Check if the user wants to exit
            print("Exiting...")
            break

        flag = command_to_flag(command)
        if flag.startswith("Error"):
            print(flag)
        else:
            write_flag_to_file(flag)
            print(f"Flag '{flag}' written to file.")
