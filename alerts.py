import datetime

seen = set()

def send_unique_alert(message):

    if message not in seen:
        seen.add(message)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full = f"[HIGH] {timestamp} - {message}"

        print(full)

        with open("alerts_log.txt", "a") as f:
            f.write(full + "\n")