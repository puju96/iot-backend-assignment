from fastapi import FastAPI, WebSocket, HTTPException, Depends, Query
from database import users_collection, iot_collection
from models import User, IoTData
from auth import create_token, verify_token
from websocket_manager import manager
import time

app = FastAPI()

# ---------------- AUTH ----------------
@app.post("/auth/login")
async def login():
    token = create_token("admin")
    return {"access_token": token}


# ---------------- USERS ----------------
@app.post("/users")
async def create_user(user: User, user_auth=Depends(verify_token)):
    await users_collection.insert_one(user.dict())
    return {"message": "User created"}

@app.get("/users/{user_id}")
async def get_user(user_id: str, user_auth=Depends(verify_token)):
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(404, "User not found")
    return user


# ---------------- IOT INGEST ----------------
@app.post("/iot/data")
async def ingest_data(data: IoTData, user_auth=Depends(verify_token)):

    if not (0 <= data.metric_1 <= 100):
        raise HTTPException(400, "metric_1 invalid")

    if not (0 <= data.metric_2 <= 200):
        raise HTTPException(400, "metric_2 invalid")

    if data.timestamp > int(time.time()):
        raise HTTPException(400, "future timestamp")

    user = await users_collection.find_one({"user_id": data.user_id})
    if not user or user["status"] != "active":
        raise HTTPException(400, "invalid user")

    await iot_collection.insert_one(data.dict())

    # broadcast
    await manager.broadcast(data.user_id, {
        "event": "NEW_DATA",
        "data": data.dict()
    })

    return {"message": "stored"}


# ---------------- FETCH ----------------
@app.get("/users/{user_id}/iot/latest")
async def latest(user_id: str, user_auth=Depends(verify_token)):
    data = await iot_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(1).to_list(1)
    return data

@app.get("/users/{user_id}/iot/history")
async def history(user_id: str, limit: int = 50, user_auth=Depends(verify_token)):
    data = await iot_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit).to_list(limit)
    return data


# ---------------- WEBSOCKET ----------------
@app.websocket("/ws/subscribe")
async def websocket_subscribe(websocket: WebSocket, user_id: str = Query(...), token: str = Query(...)):

    # validate token
    try:
        verify_token(f"Bearer {token}")
    except:
        await websocket.close()
        return

    await manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except:
        await manager.disconnect(user_id, websocket)