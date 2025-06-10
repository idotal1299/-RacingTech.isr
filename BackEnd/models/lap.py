from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from database.postgres import Base

class Lap(Base):
    __tablename__ = "laps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)

    lap_number = Column(Integer, nullable=False)
    track_name = Column(String, nullable=False)
    car_model = Column(String, nullable=False)

    lap_time_ms = Column(Integer, nullable=False)
    lap_start_time = Column(DateTime, nullable=True)
    lap_end_time = Column(DateTime, nullable=True)
    lap_duration_ms = Column(Integer, nullable=True)

    telemetry = Column(JSON, nullable=True)  # נקודות טלמטריה

    sectors = Column(JSON, nullable=False)
    fuel_left_liters = Column(Float, nullable=False)
    is_valid = Column(Boolean, default=True)

    weather = Column(String, nullable=True)
    track_temp = Column(Float, nullable=True)
    air_temp = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(String, nullable=True)
    humidity = Column(Float, nullable=True)
    fog_percent = Column(Float, nullable=True)
    cloud_percent = Column(Float, nullable=True)

    screenshot_url = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
