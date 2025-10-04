from config import PLAYERS, LIMIT_PLAYERS
import threading

id = 1

def registrar_jugador(ip, username):
    global id  # Necesitas esto para modificar las variables globales
    
    # Verificar si el jugador ya existe por IP
    for player_ip, data in PLAYERS.items():
        if player_ip == ip:
            print(f"Jugador ya registrado: {username} desde {ip}")
            return player_ip
    
    # Verificar límite de jugadores
    if len(PLAYERS) >= LIMIT_PLAYERS:
        print("Límite de jugadores alcanzado")
        return None
    
    # Crear nuevo jugador con la estructura correcta
    PLAYERS[ip] = {
        "id": id,  # ID único
        "username": username, 
        "position": (1, 1),  # Usar 'position' en lugar de 'posicion'
        "direccion": "right",  # Dirección inicial más común
        "points": 0
    }
    
    id += 1
    print(f"Jugador registrado: {username} desde {ip}")
    return ip

def get_player_by_ip(ip):
    """Busca un jugador por su IP"""
    if ip in PLAYERS:
        return ip
    return None

def player_movement(player_ip, direction):
    """Actualiza la dirección de un jugador por IP"""
    if player_ip in PLAYERS:
        PLAYERS[player_ip]["direccion"] = direction
        return True
    else:
        print(f"❌ Jugador no encontrado para IP: {player_ip}")
        return False

# def controlar_p1():
#     while True:
#         mov = input("Movimiento: ").lower()
#         if mov != "up" and mov != "down" and mov != "left" and mov != "right":
#             print("Movimiento no válido")
#             continue
        
#         player_movement("127.0.0.1", mov)
# # Crear hilo para controlar p1
# thread = threading.Thread(target=controlar_p1, daemon=True)
# thread.start()