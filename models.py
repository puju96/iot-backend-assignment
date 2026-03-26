from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    name: str
    status: str

class IoTData(BaseModel):
    user_id: str
    metric_1: float
    metric_2: int
    metric_3: int
    timestamp: int