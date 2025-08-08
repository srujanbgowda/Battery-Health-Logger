import psutil
import time
import csv
from datetime import datetime
from plyer import notification

LOG_FILE = "battery_log.csv"

def get_battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged
    return percent, plugged

def log_to_csv(percent, plugged, temperature=None):
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), percent, plugged, temperature])

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

def main():
    print("🔋 Battery Logger Started. Logging every 60 seconds.")
    
    # Create CSV file with headers if it doesn't exist
    try:
        with open(LOG_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Battery %", "Charging", "Temperature (°C)"])
    except FileExistsError:
        pass  # File already exists

    while True:
        percent, plugged = get_battery_status()
        
        # Optional: Mock temperature (replace with actual sensor data if available)
        temperature = None

        # Log to CSV
        log_to_csv(percent, plugged, temperature)

        # Notify based on conditions
        if percent <= 20 and not plugged:
            send_notification("⚠ Battery Low", f"Battery is at {percent}%. Plug in your charger.")
        elif percent == 100 and plugged:
            send_notification("🔌 Fully Charged", "Battery is 100%. Unplug your charger.")

        print(f"[{datetime.now()}] Battery: {percent}%, Charging: {plugged}")
        
        # Wait for 60 seconds
        time.sleep(60)

if __name__ == "__main__":
    main()
