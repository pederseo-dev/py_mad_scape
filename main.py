import pygame
import sys
import threading

from mapa import MAP
from config import *
from functions import *
from algoritmo import Algoritmo
from utils import obtener_url_servidor

try:
    from joysticks.api import run_api
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    url, ip = obtener_url_servidor(puerto=80)
except Exception:
    pass

pygame.init()

# Inicializar el mixer para música
pygame.mixer.init()

# Cargar música de fondo en loop automático
try:
    archivos_musica = ["music.wav", "musica.mp3", "musica.wav", "musica.ogg", "music.mp3", "background.mp3"]
    
    for archivo in archivos_musica:
        try:
            pygame.mixer.music.load(archivo)
            pygame.mixer.music.play(-1)  # Loop infinito
            print(f"🎵 Música cargada: {archivo}")
            break
        except Exception as e:
            print(f"❌ Error con {archivo}: {e}")
            continue
    else:
        print("⚠️ No se encontró archivo de música")
except Exception as e:
    print(f"⚠️ Error al cargar música: {e}")

window = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man Multiplayer - Hackathon")

clock = pygame.time.Clock()

def encontrar_jugador_mas_cercano():
    """Encuentra el jugador más cercano al enemigo"""
    if not ENEMIGO or not PLAYERS:
        return None
    
    enemigo_pos = ENEMIGO["position"]
    jugador_mas_cercano = None
    distancia_minima = float('inf')
    
    for ip, jugador in PLAYERS.items():
        jugador_pos = jugador["position"]
        
        distancia = ((enemigo_pos[0] - jugador_pos[0])**2 + 
                     (enemigo_pos[1] - jugador_pos[1])**2)**0.5
        
        if distancia < distancia_minima:
            distancia_minima = distancia
            jugador_mas_cercano = jugador
    
    return jugador_mas_cercano

def mover_enemigo():
    """Mueve el enemigo hacia el jugador más cercano usando A*"""
    if not ENEMIGO:
        return
    
    objetivo = encontrar_jugador_mas_cercano()
    if not objetivo:
        return
    
    inicio = ENEMIGO["position"]
    destino = objetivo["position"]
    
    algoritmo = Algoritmo(MAP, inicio, destino)
    camino = algoritmo.a_star()
    
    if camino and len(camino) > 1:
        pos_anterior = ENEMIGO["position"]
        siguiente_pos = camino[1]
        
        # Determinar dirección de movimiento para la animación
        dx = siguiente_pos[0] - pos_anterior[0]
        dy = siguiente_pos[1] - pos_anterior[1]
        
        if dx > 0:
            ENEMIGO["direccion"] = "right"
        elif dx < 0:
            ENEMIGO["direccion"] = "left"
        elif dy > 0:
            ENEMIGO["direccion"] = "down"
        elif dy < 0:
            ENEMIGO["direccion"] = "up"
        
        if "item_debajo" in ENEMIGO and ENEMIGO["item_debajo"]:
            MAP[pos_anterior[1]][pos_anterior[0]] = 4
        else:
            MAP[pos_anterior[1]][pos_anterior[0]] = 0
        
        valor_siguiente = MAP[siguiente_pos[1]][siguiente_pos[0]]
        ENEMIGO["item_debajo"] = (valor_siguiente == 4)
        
        ENEMIGO["position"] = siguiente_pos
        MAP[siguiente_pos[1]][siguiente_pos[0]] = "px"
        
        jugadores_a_eliminar = []
        for ip, jugador in PLAYERS.items():
            if ENEMIGO["position"] == jugador["position"]:
                jugadores_a_eliminar.append(ip)
        
        for ip in jugadores_a_eliminar:
            player_id = f"p{PLAYERS[ip]['id']}"
            x, y = PLAYERS[ip]['position']
            if MAP[y][x] == player_id:
                MAP[y][x] = 0
            del PLAYERS[ip]
            
        if len(PLAYERS) == 0:
            global WINDOW_VIEW
            WINDOW_VIEW = FINAL_VIEW

def iniciar_juego():
    """Inicia el juego automáticamente cuando hay suficientes jugadores"""
    global WINDOW_VIEW
    WINDOW_VIEW = GAME_VIEW
    posicionar_jugadores()
    posicionar_enemigo()
    cargar_items()

def procesar_eventos():
    """Procesa eventos del teclado y maneja cambios de estado del juego"""
    for evento in pygame.event.get():
        
        if evento.type == pygame.QUIT:
            return False
        
        elif evento.type == pygame.KEYDOWN:
            
            if evento.key == pygame.K_ESCAPE:
                return False
                    
            elif evento.key == pygame.K_r and WINDOW_VIEW == MENU_VIEW:
                test_players()
            
    
    return True

start = True
frame_count = 0
enemigo_frame_count = 0

juego_iniciado = False

while start:
    frame_count += 1
    enemigo_frame_count += 1
    
    if not procesar_eventos():
        start = False
        break
    
    if WINDOW_VIEW == MENU_VIEW:
        dibujar_pantalla_espera(window)
        
        # Iniciar automáticamente cuando hay 6 jugadores
        if len(PLAYERS) >= LIMIT_PLAYERS and not juego_iniciado:
            iniciar_juego()
            juego_iniciado = True

    elif WINDOW_VIEW == GAME_VIEW:
        if frame_count % VELOCIDAD_MOVIMIENTO == 0:
            fin_del_juego = procesar_movimientos()
            if fin_del_juego:
                WINDOW_VIEW = FINAL_VIEW
                determinar_ganador()
        
        if enemigo_frame_count % VELOCIDAD_ENEMIGO == 0:
            mover_enemigo()
            enemigo_frame_count = 0
            
        dibujar_pantalla_juego(window)
        dibujar_puntajes(window)

    else:
        dibujar_pantalla_final(window)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()