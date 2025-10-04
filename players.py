import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import queue

# Modelos de datos
class UserData(BaseModel):
    username: str

class MovementData(BaseModel):
    direction: str  # "up", "down", "left", "right"

# Inicializar FastAPI
app = FastAPI()

# Estado del juego - diccionario simple: IP -> username
LIMIT_PLAYERS = 6
PLAYERS = {}  # PLAYERS = {"player": PLAYERS[ip],"direction": data.direction,"ip": ip,"player":"p1"}
MOVEMENTS = queue.Queue()

@app.post("/register")
async def register_user(data: UserData, request: Request):
    """Registra un nuevo jugador"""
    ip = request.client.host if request.client else "unknown"
    if len(PLAYERS) >= LIMIT_PLAYERS:
        raise HTTPException(status_code=400, detail="Límite de jugadores alcanzado")
    PLAYERS[ip] = data.username
    print(f"Jugador registrado: {data.username} desde {ip}")
    return {"username": data.username, "ip": ip, "status": "ok"}

@app.post("/move")
async def player_move(data: MovementData, request: Request):
    """Recibe movimiento de jugador"""
    ip = request.client.host if request.client else "unknown"
    
    # Verificar si el jugador está registrado
    if ip not in PLAYERS:
        raise HTTPException(status_code=404, detail="Jugador no registrado")
    
    # Agregar movimiento a la lista
    movement = {
        "player": PLAYERS[ip],
        "direction": data.direction,
        "ip": ip,
        "player_id": f"p{len(PLAYERS)}"
    }
    MOVEMENTS.put(movement)
    
    print(f"{PLAYERS[ip]} se movió: {data.direction}")
    return {"status": "ok", "player": PLAYERS[ip]}

def run_api():
    """Ejecuta el servidor API"""
    print("controles del servidor iniciados")
    uvicorn.run("PLAYERS:app", host="0.0.0.0", port=80, reload=False)