# Client/network/socket_sender.py

import websocket
import json
from utils.logger import log
from iracing import irsdk
from auth.token_service import get_valid_racetech_token

class SecureWebSocketSender:
    def __init__(self, url: str):
        self.url = url
        self.token = get_valid_racetech_token()
        self.ws = None

    def connect(self):
        try:
            self.ws = websocket.create_connection(
                self.url,
                header=[f"Authorization: Bearer {self.token}"]
            )
            log(f"[WS] Connected to {self.url}")
        except Exception as e:
            log(f"[WS] Failed to connect: {e}")
            self.ws = None

    def send(self, data: dict) -> bool:
        if self.ws:
            try:
                self.ws.send(json.dumps(data))
                log(f"[WS] Sent lap {data.get('lapNumber', '?')}")
                return True
            except Exception as e:
                log(f"[WS] Send failed: {e}")
                self.close()
        return False

    def close(self):
        if self.ws:
            try:
                self.ws.close()
                log("[WS] Closed connection")
            except:
                pass
        self.ws = None
