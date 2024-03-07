from pynput.mouse import Button, Controller

mouse = Controller()

# Move the mouse
mouse.position = (100, 100)

# Click the mouse
mouse.click(Button.left, 1)

# Scroll
mouse.scroll(0, 2)  # Scroll vertically
