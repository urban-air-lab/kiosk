import time
from gpiozero import Button, MotionSensor
from datetime import datetime

APP_FILE = "/home/kiosk/kiosk/state/current_app.txt"
APPS_FILE = "/home/kiosk/kiosk/state/apps.txt"
MOTION_FILE = "/home/kiosk/kiosk/state/last_motion.txt"

# GPIO Pins
button1 = Button(23, pull_up=True)
button2 = Button(24, pull_up=True)
button3 = Button(25, pull_up=True)

pir = MotionSensor(18)

def load_apps():
    # Fehlerbehandlung, falls Datei nicht existiert
    try:
        with open(APPS_FILE) as f:
            return [l.strip() for l in f.readlines() if l.strip()]
    except FileNotFoundError:
        print(f"Error: {APPS_FILE} not found.")
        return []

def get_current_app():
    try:
        with open(APP_FILE) as f:
            return f.read().strip()
    except:
        return None

def set_app(app):
    with open(APP_FILE, "w") as f:
        f.write(app)

def switch_app(direction):
    apps = load_apps()
    if not apps:
        return

    current = get_current_app()

    if current not in apps:
        set_app(apps[0])
        return

    idx = apps.index(current)
    idx = (idx + direction) % len(apps)
    set_app(apps[idx])
    print(f"Switched app to: {apps[idx]}") # Debug Output

def update_motion():
    with open(MOTION_FILE, "w") as f:
        f.write(str(time.time()))

button1.when_pressed = lambda: switch_app(-1)
button3.when_pressed = lambda: switch_app(1)

def set_brightness(value):
    value = max(0, min(255, value))
    try:
        with open("/sys/class/backlight/rpi_backlight/brightness", "w") as f:
            f.write(str(value))
    except IOError:
        print("Could not set brightness (check permissions/hardware).")

pir.when_motion = update_motion

print("GPIO Controller läuft...")

IDLE_TIMEOUT = 60  # Sekunden
BRIGHT = 200
DIM = 20

while True:
    try:
        with open(MOTION_FILE) as f:
            last = float(f.read().strip())
    except:
        last = 0

    if time.time() - last < IDLE_TIMEOUT:
        set_brightness(BRIGHT)
    else:
        set_brightness(DIM)

    time.sleep(1)
