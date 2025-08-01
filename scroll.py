import pyautogui
import time



def scroll:
    print("Control Chrome scrolling with 'w' (up) and 's' (down). Press 'q' to quit.")

while True:
    key = input("Enter key (w/s/q): ").lower()

    if key == 'w':
        pyautogui.scroll(300)  # To scroll up
    elif key == 's':
        pyautogui.scroll(-300)  # To scroll down
    elif key == 'q':
        print("Exiting...")
        break
    else:
        print("Invalid key. Use 'w', 's' or 'q'.")

    time.sleep(0.1) 
