import pygame
from mapa import MAP
# Cargar imágenes y escalarlas al tamaño de celda
# Colores
NEGRO = (0, 0, 0)
AZUL = (33, 33, 222)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
ROJO = (255, 0, 0)


VELOCIDAD_MOVIMIENTO = 3  # Solo mover cada 3 frames (60 FPS / 3 = 20 FPS efectivos)
frame_count = 0

# Estados del juego
MENU_VIEW = 'menu'
GAME_VIEW = 'game'
FINAL_VIEW = 'final'

# Estado actual
WINDOW_VIEW = MENU_VIEW

# Configuración
FPS = 60

# Calcular dimensiones de la ventana
TAMANO_CELDA = 20
filas = len(MAP)
columnas = len(MAP[0])
ANCHO = columnas * TAMANO_CELDA
ALTO = filas * TAMANO_CELDA

LIMIT_PLAYERS = 6
PLAYERS = {"127.0.0.1": {"id":0, "username": "olaf", "position": (1,1), "direccion": "up","points":0},
           "127.0.0.2": {"id":1, "username": "jorge", "position": (1,1), "direccion": "up","points":0},
           "127.0.0.3": {"id":2, "username": "pedro", "position": (1,1), "direccion": "right","points":0},
           "127.0.0.4": {"id":3, "username": "luis", "position": (1,1), "direccion": "right","points":0},
           "127.0.0.5": {"id":4, "username": "Jugador5", "position": (1,1), "direccion": "right","points":0},
           "127.0.0.6": {"id":5, "username": "Jugador6", "position": (1,1), "direccion": "right","points":0}
}
ENEMY = (columnas -2, filas -2)

# TILES = {
#     0: pygame.transform.scale(pygame.image.load("assets/path.png"), (TAMANO_CELDA, TAMANO_CELDA)),
#     1: pygame.transform.scale(pygame.image.load("assets/wall.png"), (TAMANO_CELDA, TAMANO_CELDA)),
#     2: pygame.transform.scale(pygame.image.load("assets/food.png"), (TAMANO_CELDA, TAMANO_CELDA)),
#     "p1": pygame.transform.scale(pygame.image.load("assets/player1.png"), (TAMANO_CELDA, TAMANO_CELDA)),
#     "p2": pygame.transform.scale(pygame.image.load("assets/player2.png"), (TAMANO_CELDA, TAMANO_CELDA)),
# }