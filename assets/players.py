import threading
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

# Modelo de datos recibido
class UserData(BaseModel):
    username: str

app = FastAPI()

# Estado del juego
players = [] # []

@app.post("/register")
async def register_user(data: UserData, request: Request):
    # Obtener IP del cliente directamente del socket
    ip = request.client.host if request.client else "unknown"
    
    # Aquí podrías guardar username e ip en DB o imprimir
    print(f"Nuevo usuario: {data.username}, IP: {ip}")
    
    return {"username": data.username, "ip": ip, "status": "ok"}


def run_api():
    uvicorn.run("players:app", host="0.0.0.0", port=80, reload=False) 



