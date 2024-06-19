from queue import Queue
from datetime import datetime, timedelta
import threading
import time

notifications = Queue()


def cleanup_notifications(interval=10, max_age_minutes=1):
    while True:
        try:
            time.sleep(interval)
            while not notifications.empty():
                msg, timestamp = notifications.queue[0]
                if datetime.now() - timestamp > timedelta(minutes=max_age_minutes):
                    notifications.get()
                    print("Cleaned up an old notification")
                else:
                    break
        except Exception as e:
            print(f"Error during cleanup: {e}")


def start_cleanup_thread():
    thread = threading.Thread(target=cleanup_notifications)
    thread.daemon = True
    thread.start()
