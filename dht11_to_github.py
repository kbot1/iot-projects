import serial
import json
import time
import subprocess
from datetime import datetime

# 🔧 CONFIGURATION
PORT = '/dev/tty.usbmodem2101'  # Remplace par le vrai port
BAUDRATE = 9600
GITHUB_REPO_PATH = '/Users/tonnomutilisateur/chemin/vers/ton/repo'  # Remplace par le chemin réel

def get_data_from_serial():
    with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
        line = ser.readline().decode('utf-8').strip()
        if ',' in line:
            millis, temp, hum = line.split(',')
            return {
                'timestamp': datetime.now().isoformat(),
                'temperature': float(temp),
                'humidity': float(hum)
            }
        return None

def write_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def push_to_github():
    subprocess.run(['git', 'add', 'data.json'], cwd=GITHUB_REPO_PATH)
    subprocess.run(['git', 'commit', '-m', f'Update {datetime.now().isoformat()}'], cwd=GITHUB_REPO_PATH)
    subprocess.run(['git', 'push'], cwd=GITHUB_REPO_PATH)

def main():
    print("Lecture série en cours...")
    while True:
        try:
            data = get_data_from_serial()
            if data:
                print(f"📡 {data}")
                json_path = f"{GITHUB_REPO_PATH}/data.json"
                write_json(data, json_path)
                push_to_github()
            time.sleep(10)  # Intervalle entre les lectures/pushs
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
