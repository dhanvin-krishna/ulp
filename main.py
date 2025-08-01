import sounddevice as sd
import numpy as np
import time
import threading
import pyautogui
import time

# Adjustable parameters
THRESHOLD_MULTIPLIER = 3.0     # Sound must be 3x louder than ambient to count as clap
CLAP_GAP = 0.5                 # Max seconds between claps to count as a double clap
CALIBRATION_TIME = 2          # Seconds to measure background noise

# Global clap time storage
clap_times = []


clap_times = []
commd = 0

def calibrate_threshold():
    print(" Calibrating background noise... Please stay quiet.")
    recording = sd.rec(int(CALIBRATION_TIME * 44100), samplerate=44100, channels=1)
    sd.wait()
    ambient_level = np.mean(np.abs(recording))
    threshold = ambient_level * THRESHOLD_MULTIPLIER
    print(f" Calibration complete.\nAmbient Level: {ambient_level:.5f}, Clap Threshold: {threshold:.5f}\n")
    return threshold

def detect_claps(threshold):
    global clap_times

    def callback(indata, frames, time_info, status):
        if status:
            print(f"Warning: {status}")

        volume = np.mean(np.abs(indata))  # More stable than norm
        current_time = time.time()

        if volume > threshold:
            # Ignore very quick repeats
            if not clap_times or (current_time - clap_times[-1]) > 0.2:
                clap_times.append(current_time)

                if len(clap_times) >= 2 and (clap_times[-1] - clap_times[-2]) < CLAP_GAP:
                    print("Double Clap Detected!")
                    commd=2
                    pyautogui.scroll(300) 
                    clap_times.clear()
                elif len(clap_times) == 1:
                    # Wait to see if a second clap comes
                    def confirm_single_clap():
                        time.sleep(CLAP_GAP)
                        if len(clap_times) == 1:
                            print("Single Clap Detected!")
                            commd = 1
                            pyautogui.scroll(-300) 
                            clap_times.clear()
                    threading.Thread(target=confirm_single_clap, daemon=True).start()

    try:
        print(" Listening for claps... Press Ctrl+C to stop.\n")
        with sd.InputStream(callback=callback, channels=1, samplerate=44100):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error: {e}")

# Main
if __name__ == "__main__":
    threshold = calibrate_threshold()
    detect_claps(threshold)


