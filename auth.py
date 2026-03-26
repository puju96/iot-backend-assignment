from jose import jwt, JWTError
from fastapi import HTTPException, Header

SECRET = "secret"
ALGO = "HS256"

def create_token(username: str):
    return jwt.encode({"sub": username}, SECRET, algorithm=ALGO)

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")