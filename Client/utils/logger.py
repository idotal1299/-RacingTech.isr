from datetime import datetime

def log_to_file(msg: str):
    print(msg)
    with open("client_log.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def log(message):
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('ascii', errors='ignore').decode())  # מסנן אימוג'ים שלא נתמכים
