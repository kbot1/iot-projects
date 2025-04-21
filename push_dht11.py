import serial
import json
import time
import subprocess
from datetime import datetime
import os

# -------- CONFIGURATION --------
PORT = '/dev/cu.usbmodem2101'  # Remplace par ton port exact
BAUDRATE = 9600
REPO_PATH = '/Users/kevinberthelot/Documents/iot-projects/dht11-dashboard'
JSON_FILE = os.path.join(REPO_PATH, 'data.json')
PUSH_INTERVAL = 10  # secondes
# --------------------------------

def get_data_from_serial():
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
            line = ser.readline().decode('utf-8').strip()
            if ',' in line:
                millis, temp, hum = line.split(',')
                return {
                    'timestamp': datetime.now().isoformat(),
                    'temperature': float(temp),
                    'humidity': float(hum)
                }
    except serial.SerialException as e:
        print(f"[🔒 Port occupé] {e}")
        time.sleep(5)  # Réessaie après 5 sec
    except Exception as e:
        print(f"[Erreur série] {e}")
        time.sleep(5)
    return None

def write_json(data, path):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[Erreur écriture JSON] {e}")

def push_to_github(path):
    try:
        subprocess.run(['git', 'add', 'data.json'], cwd=path, check=True)
        subprocess.run(['git', 'commit', '-m', f"Update {datetime.now().isoformat()}"], cwd=path, check=True)
        subprocess.run(['git', 'push'], cwd=path, check=True)
        print("✅ Données poussées sur GitHub")
    except subprocess.CalledProcessError as e:
        print(f"[Erreur Git] {e}")


