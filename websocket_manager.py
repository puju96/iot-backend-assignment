class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, user_id, websocket):
        await websocket.accept()
        self.connections.setdefault(user_id, []).append(websocket)

    async def disconnect(self, user_id, websocket):
        self.connections[user_id].remove(websocket)

    async def broadcast(self, user_id, message):
        for ws in self.connections.get(user_id, []):
            await ws.send_json(message)

manager = ConnectionManager()