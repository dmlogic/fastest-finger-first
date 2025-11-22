# Gameshow Buzzer Controller using NPN Transistor for High-Side Switching
# This circuit requires two resistors: a Base Resistor (1kΩ) and a Pull-Up Resistor (10kΩ).
# Logic: Pi LOW (0V) -> 2N2222 OFF -> Controller Pin HIGH (V+) -> Buzzer ON

from gpiozero import Button, DigitalOutputDevice
from signal import pause

# --- Configuration ---
BUTTON_PIN = 2  # The GPIO pin (BCM number) connected to the button
CONTROL_PIN = 5 # The GPIO pin (BCM number) connected to the NPN transistor's base

# Initialize devices
# Set initial_value=True to keep the 2N2222 ON initially, which PULLS the controller pin LOW (OFF).
buzzer_control = DigitalOutputDevice(CONTROL_PIN, initial_value=True)
buzzer_button = Button(BUTTON_PIN)

# --- State Management ---
buzzed_in = False

def handle_buzz():
    """Activates the buzzer by setting the GPIO pin LOW (0V).
    This turns the 2N2222 OFF, allowing the 10kΩ pull-up to pull the controller pin HIGH."""
    global buzzed_in
    if not buzzed_in:
        # 1. Update state
        buzzed_in = True

        # 2. Activate buzzer (sets GPIO pin 3 LOW, turning NPN OFF, which turns Buzzer ON)
        buzzer_control.off()

        # 3. Log event
        print("-" * 30)
        print("!!! BUZZER PRESSED! SUPPLYING V+ VIA PULL-UP RESISTOR !!!")
        print("-" * 30)

    else:
        print("Ignored: System already locked in a buzz.")


# Attach the function to the button's press event
buzzer_button.when_pressed = handle_buzz

print("--- NPN High-Side Driver Ready ---")
print(f"Waiting for button press on GPIO {BUTTON_PIN}...")
print(f"NPN Control (LOW=Buzzer ON) on GPIO {CONTROL_PIN}.")
print("Press Ctrl+C to stop the script.")

# Keep the script running to listen for button presses
pause()
