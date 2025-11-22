# Gameshow Buzzer Controller for 8 Players (Fastest Finger First)
# Uses 8 NPN Transistors for High-Side Switching (one per player).
# Each transistor requires a Base Resistor (1kΩ) and a Pull-Up Resistor (10kΩ).
# Logic: Pi LOW (0V) -> 2N2222 OFF -> Controller Pin HIGH (V+) -> Buzzer ON

from gpiozero import Button, DigitalOutputDevice
from signal import pause

# --- Configuration ---
# Define the GPIO pins for the 8 players (BCM numbering)
# Input Pins (Buttons)
# BUTTON_PINS = [2, 3]
BUTTON_PINS = [2, 3, 4, 17, 27, 22, 10, 9]

# Output Pins (NPN Transistor Bases for controlling the lights/buzzers)
# CONTROL_PINS = [5, 6]
CONTROL_PINS = [5, 6, 13, 19, 26, 20, 21, 16]

# --- State Management ---
buzzed_in = False
first_buzzer_id = -1 # Stores the index (0-7) of the player who buzzed first

# Initialize devices
buzzer_buttons = []
buzzer_controls = []

# Initialize all 8 devices
# for i in range(2):
for i in range(8):
    # Buttons: Input device connected to the button
    buzzer_buttons.append(Button(BUTTON_PINS[i]))

    # Controls: Output device connected to the NPN base.
    # Set initial_value=True to keep the NPN ON initially, which PULLS the controller pin LOW (OFF).
    buzzer_controls.append(DigitalOutputDevice(CONTROL_PINS[i], initial_value=True))


# --- Handler Function ---
def create_handle_buzz(player_id):
    """Creates a function closure to handle a button press for a specific player ID."""
    def handle_buzz():
        global buzzed_in, first_buzzer_id
        if not buzzed_in:
            # 1. Update state
            buzzed_in = True
            first_buzzer_id = player_id

            # 2. Activate buzzer (sets the specific GPIO pin LOW, turning NPN OFF, which turns Buzzer ON)
            # Use the player_id to index the correct control pin
            buzzer_controls[player_id].off()

            # 3. Log event
            print("-" * 30)
            print(f"!!! BUZZER PRESSED! Player {player_id + 1} is FIRST FINGER! (GPIO {CONTROL_PINS[player_id]})")
            print("SUPPLYING V+ VIA PULL-UP RESISTOR to activate light/buzzer.")
            print("-" * 30)

        else:
            # Log ignored presses
            print(f"Ignored: Player {player_id + 1} pressed, but system already locked by Player {first_buzzer_id + 1}.")

    return handle_buzz


# --- Attach Handlers ---
for i in range(8):
    # Attach a unique handler function (created via closure) to each button's press event
    buzzer_buttons[i].when_pressed = create_handle_buzz(i)

# --- Startup Message ---
print("--- 8-Player NPN High-Side Driver Ready (Fastest Finger First) ---")
print("Button Pins (Input):", BUTTON_PINS)
print("Control Pins (Output):", CONTROL_PINS)
print("Press Ctrl+C to stop the script.")

# Keep the script running to listen for button presses
pause()

