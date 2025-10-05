import pygame
from mapa import MAP

# Colores
NEGRO = (0, 0, 0)
AZUL = (33, 33, 222)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
ROJO = (255, 0, 0)

VELOCIDAD_MOVIMIENTO = 20
VELOCIDAD_ENEMIGO = 21 #ligeramente mas rapido
frame_count = 0

# Estados del juego
MENU_VIEW = 'menu'
GAME_VIEW = 'game'
FINAL_VIEW = 'final'

WINDOW_VIEW = MENU_VIEW

# Configuración
FPS = 60

# Calcular dimensiones de la ventana
TAMANO_CELDA = 32  # Aumentado para mejor definición
filas = len(MAP)
columnas = len(MAP[0])
ANCHO = columnas * TAMANO_CELDA
ALTO = filas * TAMANO_CELDA

LIMIT_PLAYERS = 6

PLAYERS = {}

ENEMIGO = {
    "position": (columnas - 2, filas - 2),
    "activo": True
}

ENEMY = (columnas - 2, filas - 2)