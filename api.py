import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
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
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PYMAD SCAPE - Control</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            padding: 20px;
        }
        
        .container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .register-section {
            margin-bottom: 30px;
        }
        
        input {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.9);
        }
        
        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .register-btn {
            background: #4CAF50;
            color: white;
        }
        
        .register-btn:hover {
            background: #45a049;
            transform: scale(1.05);
        }
        
        .controls {
            display: none;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        
        .controls.active {
            display: flex;
        }
        
        .control-row {
            display: flex;
            gap: 10px;
        }
        
        .control-btn {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 2em;
            border: 2px solid white;
        }
        
        .control-btn:active {
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0.95);
        }
        
        .status {
            text-align: center;
            margin-top: 20px;
            font-size: 1.2em;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 PYMAD SCAPE</h1>
        
        <div id="register-section" class="register-section">
            <input type="text" id="username" placeholder="Ingresa tu nombre" maxlength="15">
            <button class="register-btn" onclick="register()">Registrarse</button>
        </div>
        
        <div id="controls" class="controls">
            <div class="control-row">
                <button class="control-btn" onclick="move('up')">↑</button>
            </div>
            <div class="control-row">
                <button class="control-btn" onclick="move('left')">←</button>
                <button class="control-btn" onclick="move('down')">↓</button>
                <button class="control-btn" onclick="move('right')">→</button>
            </div>
        </div>
        
        <div id="status" class="status"></div>
    </div>

    <script>
        const API_URL = window.location.origin;
        let playerRegistered = false;

        async function register() {
            const username = document.getElementById('username').value.trim();
            
            if (!username) {
                showStatus('❌ Por favor ingresa un nombre', 'error');
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    playerRegistered = true;
                    document.getElementById('register-section').classList.add('hidden');
                    document.getElementById('controls').classList.add('active');
                    showStatus(`✅ ¡Bienvenido ${data.username}!`, 'success');
                } else {
                    showStatus(`❌ ${data.detail}`, 'error');
                }
            } catch (error) {
                showStatus('❌ Error de conexión con el servidor', 'error');
            }
        }
        
        async function move(direction) {
            if (!playerRegistered) return;
            
            try {
                const response = await fetch(`${API_URL}/move`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ direction })
                });
                
                if (response.ok) {
                    showStatus(`🎮 Moviendo: ${direction}`, 'success');
                } else {
                    const data = await response.json();
                    showStatus(`❌ ${data.detail}`, 'error');
                }
            } catch (error) {
                showStatus('❌ Error al enviar movimiento', 'error');
            }
        }
        
        function showStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.textContent = message;
            statusDiv.style.color = type === 'error' ? '#ff6b6b' : '#4CAF50';
            
            setTimeout(() => {
                if (playerRegistered) {
                    statusDiv.textContent = '🎮 Usa los botones para moverte';
                    statusDiv.style.color = 'white';
                }
            }, 2000);
        }

        document.addEventListener('keydown', (e) => {
            if (!playerRegistered) return;
            
            switch(e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    move('up');
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    move('down');
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    move('left');
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    move('right');
                    break;
            }
        });
    </script>
</body>
</html>
    """

@app.post("/register")
async def register_user(data: UserData, request: Request):
    """Registra un nuevo jugador"""
    ip = request.client.host if request.client else "unknown"
    
    if len(PLAYERS) >= LIMIT_PLAYERS:
        raise HTTPException(status_code=400, detail="Límite de jugadores alcanzado")
    
    if ip in PLAYERS:
        raise HTTPException(status_code=400, detail="Ya estás registrado")
    
    max_id = max([player_data['id'] for player_data in PLAYERS.values()]) if PLAYERS else -1
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