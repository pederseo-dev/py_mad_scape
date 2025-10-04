import threading
import pygame
import sys
from maps import MAP
from players import run_api

def mover_jugador(mapa, jugador, nueva_pos):
    # Buscar jugador en el mapa y borrarlo
    for i, fila in enumerate(mapa):
        for j, celda in enumerate(fila):
            if celda == jugador:
                mapa[i][j] = 0  # dejar camino vacío
    # Poner en nueva posición
    x, y = nueva_pos
    mapa[y][x] = jugador


# Hilo para el servidor
api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

# Inicializar Pygame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
AZUL = (33, 33, 222)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)

# Configuración
TAMANO_CELDA = 20
FPS = 60

# Calcular dimensiones de la ventana
filas = len(MAP)
columnas = len(MAP[0])
ANCHO = columnas * TAMANO_CELDA
ALTO = filas * TAMANO_CELDA

# Cargar imágenes y escalarlas al tamaño de celda
TILES = {
    0: pygame.transform.scale(pygame.image.load("assets/path.png"), (TAMANO_CELDA, TAMANO_CELDA)),
    1: pygame.transform.scale(pygame.image.load("assets/wall.png"), (TAMANO_CELDA, TAMANO_CELDA)),
    2: pygame.transform.scale(pygame.image.load("assets/food.png"), (TAMANO_CELDA, TAMANO_CELDA)),
    "p1": pygame.transform.scale(pygame.image.load("assets/player1.png"), (TAMANO_CELDA, TAMANO_CELDA)),
    "p2": pygame.transform.scale(pygame.image.load("assets/player2.png"), (TAMANO_CELDA, TAMANO_CELDA)),
}

# Crear ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualizador de Matriz - Pac-Man")

# Reloj para controlar FPS
reloj = pygame.time.Clock()

def dibujar_matriz(superficie, MAP):
    """Dibuja la MAP en la superficie"""
    for fila in range(len(MAP)):
        for columna in range(len(MAP[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            
            valor = MAP[fila][columna]
            
            # Asignar color según el valor
            if valor == 0:  # Camino
                color = NEGRO
            elif valor == 1:  # Muro
                color = AZUL
            elif valor == 2:  # Casa de fantasmas
                color = GRIS
            else:
                color = BLANCO
            
            # Dibujar rectángulo
            pygame.draw.rect(superficie, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            
            # Dibujar borde para mejor visualización
            if valor == 1:
                pygame.draw.rect(superficie, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)

def close_event():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

# Bucle principal
ejecutando = True
while ejecutando:
    # Manejar eventos
    close_event()
    
    # Dibujar fondo
    ventana.fill(NEGRO)

    dibujar_matriz(ventana, MAP)
    
    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(FPS)

# Salir
pygame.quit()
sys.exit()