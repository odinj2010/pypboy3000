from gpiozero import Button # Import the Button class from the gpiozero library
from time import sleep # Import the sleep function from the time module

# Define Button objects for various GPIO pins.
# Each button is associated with a specific GPIO BCM pin number.
button4 = Button(4) # GPIO 4, physical pin 7. Comment indicates it's used for "Stats".
button17 = Button(17) # GPIO 17, physical pin 11. Comment indicates it's used for "Items".
button18 = Button(18) # GPIO 18, physical pin 12.
button27 = Button(27) # GPIO 27, physical pin 13. Comment indicates it's used for "MAP".
button22 = Button(22) # GPIO 22, physical pin 15.
# button23 = Button(23) # GPIO 23, physical pin 16. This line is commented out,
# with a note that it "Reboots system if called pin 16".
button24 = Button(24) # GPIO 24, physical pin 18. Comment indicates "No edge detection pin 18".
# button25 = Button(25) # GPIO 25, physical pin 22. This line is commented out.

# Start an infinite loop to continuously check button states
while True: 
    # Check if button4 (GPIO 4) is currently pressed
    if button4.is_pressed: 
        print("4 Pressed pin7") # If pressed, print a message indicating the button and pin
    elif button17.is_pressed: # Else, check if button17 (GPIO 17) is pressed
        print("17 Pressed pin 11") # If pressed, print a message
    elif button18.is_pressed: # Else, check if button18 (GPIO 18) is pressed
        print("18 Pressed pin 12") # If pressed, print a message
    # elif button27.is_pressed: # This block for button27 (GPIO 27) is commented out
    #     print("27 Pressed pin 13") 
    elif button22.is_pressed: # Else, check if button22 (GPIO 22) is pressed
        print("22 Pressed pin 15") # If pressed, print a message
    elif button24.is_pressed: # Else, check if button24 (GPIO 24) is pressed
       print("24 Pressed pin 18") # If pressed, print a message
    # elif button25.is_pressed: # This block for button25 (GPIO 25) is commented out
    #     print("25 Pressed pin 22") 
    else: # If none of the above buttons are pressed
        print("Released") # Print "Released"
    sleep(1) # Pause execution for 1 second before the next check
