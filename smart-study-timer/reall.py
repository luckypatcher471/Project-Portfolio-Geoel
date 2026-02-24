import serial.tools.list_ports
import serial
import time # Required for timing functions

# --- Configuration and Setup ---

# List available ports
ports = serial.tools.list_ports.comports()
portsList = []
print("Available Serial Ports:")
for onePort in ports:
    portsList.append(str(onePort))
    # Display the full description for easier selection
    print(f" - {onePort}") 

# Initialize variables
portVar = None
serialInst = serial.Serial()

# Get user input for port selection
# We ask for only the number, e.g., '3' for COM3
val = input("Select Port (just the number, e.g., '3' for COM3): COM")

# Find the matching port string
for portEntry in portsList:
    # Check if the port string starts with the required COM prefix
    if portEntry.startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        break

# --- Port Validation and Connection ---

if portVar is None:
    print(f"\nError: COM{val} not found or invalid selection.")
    exit()

print(f"\nAttempting to open port: {portVar} at 9600 baud...")

try:
    # Configuration
    serialInst.baudrate = 9600
    serialInst.port = portVar
    # Set a read timeout (good practice for stability)
    serialInst.timeout = 1 
    serialInst.open()
except serial.SerialException as e:
    # Enhanced error handling for the common PermissionError
    print(f"\nFATAL ERROR: Could not open port {portVar}.")
    print(f"Check if another program (like Arduino IDE's Serial Monitor) is using it.")
    print(f"Error details: {e}")
    exit()

# --- Timer State Management ---
start_time = None
is_timer_running = False

print("\n--- Serial Timer Initialized ---")
print("Waiting for '1' to START the timer and '0' to STOP it.")
print("Press Ctrl+C to exit the program.")

# --- Main Loop ---
while True:
    try:
        # Check if data is waiting
        if serialInst.in_waiting > 0:
            # Read a line of data
            packet = serialInst.readline()
            
            # Decode the bytes and remove leading/trailing whitespace (including \n and \r)
            data = packet.decode('utf-8').strip()
            
            # Print the raw data for visibility
            print(f"Received: '{data}'", end=" ")

            # --- Timer Logic ---
            
            if data == '1':
                if not is_timer_running:
                    # Start the timer by recording the current time
                    start_time = time.time()
                    is_timer_running = True
                    print("-> TIMER STARTED!")
                else:
                    print("(Timer already running.)")
            
            elif data == '0':
                if is_timer_running:
                    end_time = time.time()
                    # Calculate duration
                    elapsed_time = end_time - start_time
                    
                    # Format and display the result
                    print(f"\n--- TIMER STOPPED! ---")
                    print(f"Duration: {elapsed_time:.3f} seconds")
                    print("----------------------")
                    
                    # Reset the state
                    is_timer_running = False
                    start_time = None 
                else:
                    print("(Timer is not running.)")

            else:
                # Print current running status if other data is received
                if is_timer_running:
                    current_elapsed = time.time() - start_time
                    print(f"(Running: {current_elapsed:.2f}s)")
                else:
                    print("")
                
    except KeyboardInterrupt:
        print("\nExiting program due to keyboard interrupt.")
        break
    except serial.SerialException:
        print("\nSerial port disconnected or error occurred.")
        break
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        break

# Close the serial connection gracefully
if serialInst.is_open:
    serialInst.close()
    print("Serial port closed.")