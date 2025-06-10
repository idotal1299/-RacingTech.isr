# BackEnd/API/ws_lap.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from database.postgres import SessionLocal
from services.laps import save_lap_from_ws
import os

router = APIRouter()

SECRET_KEY = os.getenv("RACETECH_SECRET", "my-very-secret-key")
ALGORITHM = "HS256"

@router.websocket("/ws/lap")
async def websocket_lap(websocket: WebSocket):
    await websocket.accept()
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=4401)
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError("Missing sub in token")
    except JWTError:
        await websocket.close(code=4401)
        return

    # התחברות למסד נתונים
    db = SessionLocal()

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except Exception:
                await websocket.send_json({"error": "Invalid JSON"})
                continue

            try:
                lap = save_lap_from_ws(data, user_id, db)
                await websocket.send_json({
                    "status": "ok",
                    "lap_id": lap.id,
                    "lap_time_ms": lap.lap_time_ms
                })
            except Exception as e:
                await websocket.send_json({"status": "error", "message": str(e)})

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user {user_id}")
    finally:
        db.close()
