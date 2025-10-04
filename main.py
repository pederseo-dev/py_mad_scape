import pygame
import sys
from mapa import MAP
from config import *
from functions import *


# Inicializar Pygame
pygame.init()

# Crear window
window = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man Multiplayer - Hackathon")

# Reloj para controlar FPS
clock = pygame.time.Clock()

def procesar_eventos():
    """Procesa eventos del teclado y maneja cambios de estado del juego"""
    global WINDOW_VIEW  # Permite modificar la variable global WINDOW_VIEW
    
    # Obtener todos los eventos de pygame (teclado, mouse, etc.)
    for evento in pygame.event.get():
        
        # EVENTO: Usuario cierra la ventana (X)
        if evento.type == pygame.QUIT:
            return False  # Salir del juego
        
        # EVENTO: Usuario presiona una tecla
        elif evento.type == pygame.KEYDOWN:
            
            # TECLA ESC: Salir del juego
            if evento.key == pygame.K_ESCAPE:
                return False  # Salir del juego

            # TECLA ESPACIO: Iniciar juego (solo si estamos en menú y hay 6 jugadores)
            elif evento.key == pygame.K_SPACE and WINDOW_VIEW == MENU_VIEW:
                if len(PLAYERS) == 6:  # Verificar que hay exactamente 6 jugadores
                    WINDOW_VIEW = GAME_VIEW  # Cambiar a pantalla de juego
                    posicionar_jugadores()   # Colocar jugadores en el mapa
                    posicionar_enemigo()     # Colocar enemigo en esquina inferior
                    cargar_items()           # Cargar items en el mapa
                    print("🎮 ¡Juego iniciado!")
                    
            # TECLA R: Agregar jugador de prueba (solo para testing)
            elif evento.key == pygame.K_r and WINDOW_VIEW == MENU_VIEW:
                test_players()
            
            # CONTROLES DE MOVIMIENTO (solo en pantalla de juego)
            elif WINDOW_VIEW == GAME_VIEW:
                # Jugador 1 (WASD)
                if evento.key == pygame.K_w:
                    PLAYERS["127.0.0.1"]["direccion"] = "up"
                elif evento.key == pygame.K_s:
                    PLAYERS["127.0.0.1"]["direccion"] = "down"
                elif evento.key == pygame.K_a:
                    PLAYERS["127.0.0.1"]["direccion"] = "left"
                elif evento.key == pygame.K_d:
                    PLAYERS["127.0.0.1"]["direccion"] = "right"
                
                # Jugador 2 (Flechas)
                elif evento.key == pygame.K_UP:
                    PLAYERS["127.0.0.2"]["direccion"] = "up"
                elif evento.key == pygame.K_DOWN:
                    PLAYERS["127.0.0.2"]["direccion"] = "down"
                elif evento.key == pygame.K_LEFT:
                    PLAYERS["127.0.0.2"]["direccion"] = "left"
                elif evento.key == pygame.K_RIGHT:
                    PLAYERS["127.0.0.2"]["direccion"] = "right"
                
                # Jugador 3 (IJKL)
                elif evento.key == pygame.K_i:
                    PLAYERS["127.0.0.3"]["direccion"] = "up"
                elif evento.key == pygame.K_k:
                    PLAYERS["127.0.0.3"]["direccion"] = "down"
                elif evento.key == pygame.K_j:
                    PLAYERS["127.0.0.3"]["direccion"] = "left"
                elif evento.key == pygame.K_l:
                    PLAYERS["127.0.0.3"]["direccion"] = "right"
                
                # Jugador 4 (Numpad)
                elif evento.key == pygame.K_KP8:
                    PLAYERS["127.0.0.4"]["direccion"] = "up"
                elif evento.key == pygame.K_KP5:
                    PLAYERS["127.0.0.4"]["direccion"] = "down"
                elif evento.key == pygame.K_KP4:
                    PLAYERS["127.0.0.4"]["direccion"] = "left"
                elif evento.key == pygame.K_KP6:
                    PLAYERS["127.0.0.4"]["direccion"] = "right"
    return True

# Bucle principal
start = True
frame_count = 0  # Contador de frames para controlar velocidad
while start:
    frame_count += 1  # Incrementar contador de frames
    
    # Procesar eventos
    if not procesar_eventos():
        start = False
        break
    
    # Dibujar según el estado actual
    if WINDOW_VIEW == MENU_VIEW:
        dibujar_pantalla_espera(window)

    elif WINDOW_VIEW == GAME_VIEW:
        # Procesar movimientos solo cada VELOCIDAD_MOVIMIENTO frames
        # Esto mantiene 60 FPS de renderizado pero reduce velocidad de movimiento
        if frame_count % VELOCIDAD_MOVIMIENTO == 0:
            procesar_movimientos()
            detectar_colision_items()  # Detectar colisiones con items
        dibujar_pantalla_juego(window)
        dibujar_puntajes(window)  # Mostrar puntajes en pantalla

    else:
        dibujar_pantalla_final(window)
    
    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(FPS)

# Salir
pygame.quit()
sys.exit()