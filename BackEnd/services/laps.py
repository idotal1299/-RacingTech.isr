# BackEnd/services/laps.py

from sqlalchemy.orm import Session
from models.lap import Lap

def save_lap_from_ws(data: dict, user_id: str, db: Session):
    lap = Lap(
        user_id=user_id,
        lap_number=data["lap_number"],
        track_name=data["track_name"],
        car_model=data["car_name"],
        lap_time_ms=data["lap_time"],
        sectors=data["sectors"],
        fuel_left_liters=data["fuel_left"],
        is_valid=data["is_valid"],
        weather=data.get("weather"),
        track_temp=data.get("track_temp"),
        air_temp=data.get("air_temp"),
        wind_speed=data.get("wind_speed"),
        wind_direction=data.get("wind_direction"),
        humidity=data.get("humidity"),
        fog_percent=data.get("fog_percent"),
        cloud_percent=data.get("cloud_percent"),
        screenshot_url=data.get("screenshot_url")
    )
    db.add(lap)
    db.commit()
    db.refresh(lap)
    return lap
