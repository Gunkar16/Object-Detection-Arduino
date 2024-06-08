import serial
import subprocess
import pygame
import threading

# Initialize pygame mixer
pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Function to run a script and play sound simultaneously
def run_script_with_sound(script, sound_file):
    sound_thread = threading.Thread(target=play_sound, args=(sound_file,))
    script_thread = threading.Thread(target=subprocess.run, args=(['python', script],), kwargs={'check': True})
    
    # Start both threads
    sound_thread.start()
    script_thread.start()
    
    # Wait for both threads to complete
    sound_thread.join()
    script_thread.join()
    
def run_scripts(script1, script2, *args):
    script1_thread = threading.Thread(target=subprocess.run, args=(['python', script1] + list(args),), kwargs={'check': True})
    script2_thread = threading.Thread(target=subprocess.run, args=(['python', script2],), kwargs={'check': True})
    
    # Start both threads
    script1_thread.start()
    script2_thread.start()
    
    # Wait for both threads to complete
    script1_thread.join()
    script2_thread.join()
# Replace with the actual COM port where your Arduino is connected
# You can find this in the Arduino IDE or device manager
port = 'COM13'

# Set the baud rate to match the one you configured in your Arduino code (usually 9600)
baudrate = 9600

try:
    # Open the serial connection
    ser = serial.Serial(port, baudrate)
    print("Successfully connected to the Arduino")

    while True:
        # Read incoming data from the serial port (non-blocking)
        data = ser.readline().decode('utf-8').strip()

        # Check if data is received and if it matches the expected signal
        if data:
            if data == '1':
                print("Signal received from Arduino: 1")
                # Run capture.py script with "Image is being captured" sound in Hindi
                run_script_with_sound('capture.py', 'image_capture.mp3')
                # Run model.py script with "Processing the image" sound in Hindi
                run_script_with_sound('model.py', 'image_processing.mp3')
                # Read the detection results from the file
                with open("detection_results.txt", "r") as f:
                    detection_results = f.read().strip().split(',')
                # Run playHindi.py and draw.py scripts simultaneously with detection results
                run_scripts('play.py', 'draw.py', *detection_results)
            else:
                print(f"Unexpected data received: {data}")
except serial.SerialException as e:
    print(f"Error: {e}")
except subprocess.CalledProcessError as e:
    print(f"Subprocess error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    ser.close()