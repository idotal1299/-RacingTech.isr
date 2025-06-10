from iracing.sdk_wrapper import IRacingWrapper
from iracing.session_manager import SessionManager, Lap
from network.socket_sender import SecureWebSocketSender
from config.config_loader import load_config
from utils.fallback_cache import UnsentLapManager
from utils.logger import log
from utils.process import is_iracing_running
from auth.token_service import get_valid_racetech_token
import sys
from PySide6.QtWidgets import QApplication
from gui.main import MainWindow

import time

def safe_log(msg):
    try:
        log(msg)
    except:
        print(msg)

def create_new_lap(sdk, lap_number, weather):
    fuel_start = sdk.get_value("FuelLevel")
    if fuel_start is None:
        return None
    return Lap(
        lap_number=lap_number,
        fuel_start=fuel_start,
        weather=weather
    )

def send_lap(lap, sender, cache):
    if not lap:
        return
    lap.close_lap()
    if lap.is_valid:
        if not sender.send(lap.to_dict()):
            cache.add(lap.to_dict())
    else:
        log(f"[INFO] Skipped invalid lap {lap.lap_number}")

def main():
    current_lap = None
    sender = None
    cache = None

    try:
        safe_log("RaceTech Client started")

        config = load_config()
        SEND_INTERVAL = config.get("send_interval", 0.5)
        WS_URL = config["server_url"]

        # Start GUI login flow and get token
        from gui.main import main as gui_main
        racetech_token = gui_main()
        if not racetech_token:
            safe_log("[FATAL] User did not complete login. Exiting.")
            return
        safe_log("Received RaceTech Token.")

        sender = SecureWebSocketSender(WS_URL, racetech_token)
        cache = UnsentLapManager("unsent_laps.json")

        while not is_iracing_running():
            safe_log("Waiting for iRacing...")
            time.sleep(3)

        sdk = IRacingWrapper()
        while not sdk.is_initialized():
            safe_log("Waiting for iRacing session...")
            time.sleep(2)

        session = SessionManager(sdk)
        sender.connect()
        cache.flush(sender)

        while sdk.is_initialized():
            try:
                if not session.is_session_active():
                    time.sleep(SEND_INTERVAL)
                    continue

                session.check_session_change()

                if session.is_new_lap():
                    send_lap(current_lap, sender, cache)
                    current_lap = create_new_lap(sdk, session.last_lap_number, session.weather)
                    if not current_lap:
                        safe_log("[ERROR] Failed to create new lap.")
                        continue

                point = sdk.get_telemetry_point()
                if point and current_lap:
                    current_lap.add_telemetry_point(point)

                time.sleep(SEND_INTERVAL)

            except Exception as inner_error:
                safe_log(f"[ERROR] Loop error: {inner_error}")

    except KeyboardInterrupt:
        safe_log("Client manually stopped.")
    except Exception as e:
        safe_log(f"[FATAL] Unexpected error: {e}")
    finally:
        try:
            send_lap(current_lap, sender, cache)
            if sender:
                sender.close()
            if cache:
                cache.save()
            safe_log("Graceful shutdown complete.")
        except Exception as final_error:
            safe_log(f"[ERROR] During shutdown: {final_error}")

if __name__ == "__main__":
    main()
