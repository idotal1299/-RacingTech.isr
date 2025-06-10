from iracing import irsdk
import time

class IRacingWrapper:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.ir.startup()

    def is_initialized(self):
        return self.ir.is_initialized

    def get_value(self, key: str):
        try:
            return self.ir[key]
        except:
            return None

    def get_telemetry_point(self):
        return {
            "timestamp": time.time(),
            "LapDistPct": self.get_value("LapDistPct"),
            "Speed": self.get_value("Speed"),
            "Throttle": self.get_value("Throttle"),
            "Brake": self.get_value("Brake"),
            "SteeringWheelAngle": self.get_value("SteeringWheelAngle"),
            "RPM": self.get_value("RPM"),
            "Gear": self.get_value("Gear"),
            "LapCurrentLapInvalid": self.get_value("LapCurrentLapInvalid"),
            "IsOnTrack": self.get_value("IsOnTrack"),
            "SessionTime": self.get_value("SessionTime")
        }
