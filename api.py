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
            font-family: 'Courier New', monospace;
            background: #000;
            background-image: 
                radial-gradient(circle at 20% 80%, #ff0080 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, #00ff80 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, #8000ff 0%, transparent 50%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #00ff00;
            padding: 20px;
            animation: scanlines 0.1s linear infinite;
        }
        
        @keyframes scanlines {
            0% { background-position: 0 0; }
            100% { background-position: 0 4px; }
        }
        
        .container {
            background: rgba(0, 0, 0, 0.9);
            border: 3px solid #00ff00;
            border-radius: 0;
            padding: 30px;
            max-width: 500px;
            width: 100%;
            box-shadow: 
                0 0 20px #00ff00,
                inset 0 0 20px rgba(0, 255, 0, 0.1);
            position: relative;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: -3px;
            left: -3px;
            right: -3px;
            bottom: -3px;
            background: linear-gradient(45deg, #ff0080, #00ff80, #8000ff, #ff0080);
            border-radius: 0;
            z-index: -1;
            animation: borderGlow 2s linear infinite;
        }
        
        @keyframes borderGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 3em;
            font-weight: bold;
            color: #00ff00;
            text-shadow: 
                0 0 10px #00ff00,
                0 0 20px #00ff00,
                0 0 30px #00ff00;
            letter-spacing: 3px;
            text-transform: uppercase;
            animation: titleGlow 1.5s ease-in-out infinite alternate;
        }
        
        @keyframes titleGlow {
            from { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00; }
            to { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00; }
        }
        
        .register-section {
            margin-bottom: 30px;
        }
        
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #00ff00;
            border-radius: 0;
            font-size: 1.2em;
            font-family: 'Courier New', monospace;
            margin-bottom: 15px;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            transition: all 0.3s;
            box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.2);
        }
        
        input:focus {
            outline: none;
            border-color: #ff0080;
            box-shadow: 
                0 0 15px #ff0080,
                inset 0 0 10px rgba(255, 0, 128, 0.2);
        }
        
        input::placeholder {
            color: rgba(0, 255, 0, 0.5);
        }
        
        button {
            width: 100%;
            padding: 15px;
            border: 2px solid #00ff00;
            border-radius: 0;
            font-size: 1.2em;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            transition: all 0.3s;
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .register-btn:hover {
            background: rgba(0, 255, 0, 0.1);
            box-shadow: 0 0 20px #00ff00;
            border-color: #ff0080;
            color: #ff0080;
        }
        
        .register-btn:active {
            background: rgba(255, 0, 128, 0.2);
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
            background: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            font-size: 2em;
            font-family: 'Courier New', monospace;
            border: 2px solid #00ff00;
            border-radius: 0;
            transition: all 0.3s;
            text-transform: uppercase;
        }
        
        .control-btn:hover {
            background: rgba(0, 255, 0, 0.1);
            box-shadow: 0 0 20px #00ff00;
            border-color: #ff0080;
            color: #ff0080;
        }
        
        .control-btn:active {
            background: rgba(255, 0, 128, 0.2);
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