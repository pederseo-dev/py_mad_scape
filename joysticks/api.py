import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from config import PLAYERS, LIMIT_PLAYERS

class UserData(BaseModel):
    username: str

class MovementData(BaseModel):
    direction: str

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    """Sirve la página de controles"""
    return FileResponse("joysticks/interface.html")

@app.post("/register")
async def register_user(data: UserData, request: Request):
    """Registra un nuevo jugador"""
    ip = request.client.host if request.client else "unknown"
    
    if len(PLAYERS) >= LIMIT_PLAYERS:
        raise HTTPException(status_code=400, detail="Límite de jugadores alcanzado")
    
    if ip in PLAYERS:
        raise HTTPException(status_code=400, detail="Ya estás registrado")
    
    max_id = max([player_data['id'] for player_data in PLAYERS.values()]) if PLAYERS else 0
    nuevo_id = max_id + 1
    
    PLAYERS[ip] = {
        "id": nuevo_id,
        "username": data.username,
        "position": (1, 1),
        "direccion": "right",
        "points": 0
    }
    
    return {
        "username": data.username, 
        "ip": ip, 
        "player_id": nuevo_id,
        "status": "registered"
    }

@app.post("/move")
async def player_move(data: MovementData, request: Request):
    """Recibe movimiento de jugador"""
    ip = request.client.host if request.client else "unknown"
    
    if ip not in PLAYERS:
        raise HTTPException(status_code=404, detail="Jugador no registrado")
    
    direcciones_validas = ["up", "down", "left", "right"]
    if data.direction not in direcciones_validas:
        raise HTTPException(status_code=400, detail=f"Dirección inválida")
    
    PLAYERS[ip]["direccion"] = data.direction
    
    return {
        "status": "ok", 
        "player": PLAYERS[ip]['username'],
        "direction": data.direction
    }

@app.get("/players")
async def get_players():
    """Obtiene lista de jugadores conectados"""
    return {
        "total": len(PLAYERS),
        "limit": LIMIT_PLAYERS,
        "players": [
            {
                "username": data["username"],
                "id": data["id"],
                "points": data["points"]
            }
            for ip, data in PLAYERS.items()
        ]
    }

@app.get("/status")
async def get_status():
    """Estado del servidor"""
    return {
        "status": "online",
        "players_connected": len(PLAYERS),
        "slots_available": LIMIT_PLAYERS - len(PLAYERS)
    }

def run_api():
    """Ejecuta el servidor API"""
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="warning")

if __name__ == "__main__":
    run_api()