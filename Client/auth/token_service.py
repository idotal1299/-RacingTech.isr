# Client/auth/token_service.py

import os
import json
import pickle
import requests
import time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# נתיבים
CONFIG_PATH = os.path.join("config", "client_secret.json")
GOOGLE_TOKEN_PATH = os.path.join("cache", "token.pickle")
RACETECH_TOKEN_PATH = os.path.join("cache", "racetech_token.json")
AUTH_API_URL = "https://your-racetech-server.com/auth/google"  # תחליף כשיהיה שרת פעיל

# הרשאות
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

def get_or_refresh_google_token():
    creds = None
    if os.path.exists(GOOGLE_TOKEN_PATH):
        with open(GOOGLE_TOKEN_PATH, 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CONFIG_PATH, SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print("[ERROR] Failed to open browser automatically for Google login. Please open the following URL manually:")
                print(flow.authorization_url)
                import webbrowser
                webbrowser.open(flow.authorization_url)
                input("After authorizing, press Enter to continue...")

        os.makedirs(os.path.dirname(GOOGLE_TOKEN_PATH), exist_ok=True)
        with open(GOOGLE_TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)

    return creds.id_token

def request_racetech_token(google_token: str):
    response = requests.post(AUTH_API_URL, json={"token": google_token}, timeout=10)
    response.raise_for_status()
    data = response.json()
    racetech_token = data.get("racetech_token")
    if not racetech_token:
        raise Exception("No racetech_token in response.")

    token_data = {
        "token": racetech_token,
        "issued_at": int(time.time())
    }
    os.makedirs(os.path.dirname(RACETECH_TOKEN_PATH), exist_ok=True)
    with open(RACETECH_TOKEN_PATH, "w") as f:
        json.dump(token_data, f)

    return racetech_token

def get_valid_racetech_token():
    try:
        if os.path.exists(RACETECH_TOKEN_PATH):
            with open(RACETECH_TOKEN_PATH, "r") as f:
                data = json.load(f)
                token = data.get("token")
                issued_at = data.get("issued_at", 0)
                if int(time.time()) - issued_at < 3600:
                    return token

        google_token = get_or_refresh_google_token()
        return request_racetech_token(google_token)

    except Exception as e:
        print(f"[WARNING] Could not reach RaceTech server: {e}")
        return "OFFLINE-TOKEN"

def clear_racetech_token():
    if os.path.exists(RACETECH_TOKEN_PATH):
        os.remove(RACETECH_TOKEN_PATH)
    if os.path.exists(GOOGLE_TOKEN_PATH):
        os.remove(GOOGLE_TOKEN_PATH)
    print("RaceTech token cleared.")

def is_racetech_token_valid():
    if not os.path.exists(RACETECH_TOKEN_PATH):
        return False
    try:
        with open(RACETECH_TOKEN_PATH, "r") as f:
            data = json.load(f)
            issued_at = data.get("issued_at", 0)
            return int(time.time()) - issued_at < 3600
    except Exception as e:
        print(f"[ERROR] Could not validate RaceTech token: {e}")
        return False