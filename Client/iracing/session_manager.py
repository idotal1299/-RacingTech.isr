import time
import uuid

class SessionManager:
    def __init__(self, sdk):
        self.sdk = sdk
        self.reset_session()
        self.last_session_unique_id = sdk.get_value("SessionUniqueID")
        self.last_lap_number = -1

    def reset_session(self):
        self.session_id = str(uuid.uuid4())
        self.track = self.sdk.get_value("WeekendInfo:TrackDisplayName")
        self.driver = self.sdk.get_value("DriverInfo:Drivers:0:UserName")
        self.car = self.sdk.get_value("DriverInfo:Drivers:0:CarScreenName")
        self.setup = self.sdk.get_value("DriverSetupName")
        self.weather = {
            "airTemp": self.sdk.get_value("AirTemp"),
            "trackTemp": self.sdk.get_value("TrackTemp")
        }
        self.start_time = time.time()
        self.laps = []

    def to_dict(self):
        return {
            "sessionId": self.session_id,
            "track": self.track,
            "driver": self.driver,
            "car": self.car,
            "setup": self.setup,
            "weather": self.weather,
            "startTime": self.start_time,
            "laps": [lap.to_dict() for lap in self.laps]
        }

    def check_session_change(self):
        current_id = self.sdk.get_value("SessionUniqueID")
        if current_id != self.last_session_unique_id:
            print("🟢 New session detected.")
            self.last_session_unique_id = current_id
            self.reset_session()

    def is_session_active(self):
        state = self.sdk.get_value("SessionState")
        return state in [1, 2, 3]  # GetInCar, Warmup, Racing

    def is_new_lap(self):
        current_lap = self.sdk.get_value("Lap")
        if current_lap != self.last_lap_number:
            self.last_lap_number = current_lap
            return True
        return False


class Lap:
    def __init__(self, lap_number: int, fuel_start, weather):
        self.lap_number = lap_number
        self.start_time = time.time()
        self.end_time = None
        self.fuel_start = fuel_start
        self.weather = weather
        self.telemetry = []
        self.is_valid = True

    def add_telemetry_point(self, point: dict):
        self.telemetry.append(point)
        if not point.get("IsOnTrack", 1):
            self.is_valid = False
        if point.get("LapCurrentLapInvalid", 0):
            self.is_valid = False
        if point.get("Speed", 100) < 1 and point.get("Throttle", 0) > 0.5:
            self.is_valid = False

    def close_lap(self):
        self.end_time = time.time()

    def lap_duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def to_dict(self):
        return {
            "lapNumber": self.lap_number,
            "lapStartTime": self.start_time,
            "lapEndTime": self.end_time,
            "lapDuration": self.lap_duration(),
            "fuelStart": self.fuel_start,
            "weather": self.weather,
            "telemetry": self.telemetry,
            "isValid": self.is_valid
        }
