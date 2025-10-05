import pygame
import math

# Colores base
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (33, 33, 222)
AZUL_OSCURO = (20, 20, 150)
GRIS = (100, 100, 100)
GRIS_OSCURO = (60, 60, 60)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# Colores de pingüinos
COLORES_PINGUINOS = [
    (255, 100, 100),  # Rojo
    (100, 100, 255),  # Azul  
    (100, 255, 100),  # Verde
    (255, 255, 100),  # Amarillo
    (255, 100, 255),  # Magenta
    (255, 150, 50)    # Naranja
]

def crear_pinguino_direccion(color_cuerpo, direccion, tamaño=32):
    """Crea un sprite de pingüino moderno y bonito con el color y dirección especificados"""
    surface = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
    
    # Cuerpo principal (más estilizado)
    pygame.draw.ellipse(surface, color_cuerpo, (tamaño//4, tamaño//2, tamaño//2, tamaño//2))
    
    # Cabeza (más grande y redonda)
    pygame.draw.circle(surface, color_cuerpo, (tamaño//2, tamaño//3), tamaño//3)
    
    # Panza blanca (más grande y centrada)
    pygame.draw.ellipse(surface, BLANCO, (tamaño//3, tamaño//2, tamaño//3, tamaño//3))
    
    # Pico según dirección (más pequeño y elegante)
    if direccion == "up":
        # Pico hacia arriba
        pygame.draw.polygon(surface, (255, 140, 40), [
            (tamaño//2, tamaño//3 - 3), 
            (tamaño//2 - 2, tamaño//3 - 1), 
            (tamaño//2 + 2, tamaño//3 - 1)
        ])
        # Ojos más arriba y expresivos
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 3, tamaño//3 - 2), 2)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 3, tamaño//3 - 2), 2)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 2, tamaño//3 - 3), 1)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 4, tamaño//3 - 3), 1)
        # Patas más pequeñas
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 - 2, tamaño - 3, 2, 3))
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 + 1, tamaño - 3, 2, 3))
        
    elif direccion == "down":
        # Pico hacia abajo
        pygame.draw.polygon(surface, (255, 140, 40), [
            (tamaño//2, tamaño//3 + 3), 
            (tamaño//2 - 2, tamaño//3 + 1), 
            (tamaño//2 + 2, tamaño//3 + 1)
        ])
        # Ojos normales
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 3, tamaño//3 - 1), 2)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 3, tamaño//3 - 1), 2)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 2, tamaño//3 - 2), 1)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 4, tamaño//3 - 2), 1)
        # Patas más separadas
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 - 4, tamaño - 3, 2, 3))
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 + 2, tamaño - 3, 2, 3))
        
    elif direccion == "left":
        # Pico hacia la izquierda
        pygame.draw.polygon(surface, (255, 140, 40), [
            (tamaño//2 - 3, tamaño//3), 
            (tamaño//2 - 1, tamaño//3 - 2), 
            (tamaño//2 - 1, tamaño//3 + 2)
        ])
        # Ojos hacia la izquierda
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 4, tamaño//3 - 1), 2)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 1, tamaño//3 - 1), 2)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 3, tamaño//3 - 2), 1)
        pygame.draw.circle(surface, BLANCO, (tamaño//2, tamaño//3 - 2), 1)
        # Patas normales
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 - 3, tamaño - 3, 2, 3))
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 + 1, tamaño - 3, 2, 3))
        
    else:  # right
        # Pico hacia la derecha
        pygame.draw.polygon(surface, (255, 140, 40), [
            (tamaño//2 + 3, tamaño//3), 
            (tamaño//2 + 1, tamaño//3 - 2), 
            (tamaño//2 + 1, tamaño//3 + 2)
        ])
        # Ojos hacia la derecha
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 1, tamaño//3 - 1), 2)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 4, tamaño//3 - 1), 2)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 2, tamaño//3 - 2), 1)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 5, tamaño//3 - 2), 1)
        # Patas normales
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 - 3, tamaño - 3, 2, 3))
        pygame.draw.rect(surface, (255, 140, 40), (tamaño//2 + 1, tamaño - 3, 2, 3))
    
    return surface

def crear_pinguino(color_cuerpo, tamaño=20):
    """Crea un sprite de pingüino básico (dirección down por defecto)"""
    return crear_pinguino_direccion(color_cuerpo, "down", tamaño)

def crear_fantasma_direccion(direccion, tamaño=32):
    """Crea un sprite de fantasma moderno con dirección específica"""
    surface = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
    
    # Colores del fantasma (rojo clásico)
    rojo_oscuro = (180, 0, 0)
    rojo_medio = (220, 0, 0)
    rojo_claro = (255, 0, 0)
    
    # Cuerpo del fantasma (forma de gota)
    pygame.draw.ellipse(surface, rojo_claro, (tamaño//4, tamaño//3, tamaño//2, tamaño//2))
    
    # Cabeza del fantasma (círculo)
    pygame.draw.circle(surface, rojo_claro, (tamaño//2, tamaño//3), tamaño//3)
    
    # Ojos según dirección
    if direccion == "up":
        # Ojos mirando hacia arriba
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 4, tamaño//3 - 2), 3)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 4, tamaño//3 - 2), 3)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 4, tamaño//3 - 3), 1)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 4, tamaño//3 - 3), 1)
        
    elif direccion == "down":
        # Ojos mirando hacia abajo
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 4, tamaño//3 - 1), 3)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 4, tamaño//3 - 1), 3)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 4, tamaño//3), 1)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 4, tamaño//3), 1)
        
    elif direccion == "left":
        # Ojos mirando hacia la izquierda
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 5, tamaño//3 - 1), 3)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 - 1, tamaño//3 - 1), 3)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 6, tamaño//3 - 1), 1)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 - 2, tamaño//3 - 1), 1)
        
    else:  # right
        # Ojos mirando hacia la derecha
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 1, tamaño//3 - 1), 3)
        pygame.draw.circle(surface, BLANCO, (tamaño//2 + 5, tamaño//3 - 1), 3)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 2, tamaño//3 - 1), 1)
        pygame.draw.circle(surface, NEGRO, (tamaño//2 + 6, tamaño//3 - 1), 1)
    
    # Patas onduladas del fantasma
    for i in range(4):
        x = tamaño//4 + i * (tamaño//8)
        y = tamaño - 4
        pygame.draw.rect(surface, rojo_claro, (x, y, tamaño//8, 4))
        # Hacer las patas onduladas
        if i % 2 == 0:
            pygame.draw.rect(surface, rojo_claro, (x + 2, y - 2, tamaño//8 - 4, 2))
        else:
            pygame.draw.rect(surface, rojo_claro, (x + 2, y + 2, tamaño//8 - 4, 2))
    
    return surface

def crear_fantasma(tamaño=32):
    """Crea un sprite de fantasma básico (dirección up por defecto)"""
    return crear_fantasma_direccion("up", tamaño)

def crear_punto_pacman(tamaño=32):
    """Crea un punto como en Pac-Man (puntito en el centro del cuadro)"""
    surface = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
    
    # Punto amarillo pequeño en el centro del cuadro
    pygame.draw.circle(surface, (255, 255, 0), (tamaño//2, tamaño//2), 3)
    
    return surface

def crear_muro_con_textura(ancho, alto):
    """Crea un muro con textura de ladrillos"""
    surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    
    # Fondo azul
    pygame.draw.rect(surface, AZUL, (0, 0, ancho, alto))
    
    # Líneas de ladrillos (ajustadas para mayor resolución)
    brick_height = alto // 4
    brick_width = ancho // 2
    
    for y in range(0, alto, brick_height):
        for x in range(0, ancho, brick_width):
            # Líneas horizontales
            pygame.draw.line(surface, AZUL_OSCURO, (x, y), (x + brick_width, y), 2)
            # Líneas verticales (alternadas)
            if (y // brick_height) % 2 == 0:
                pygame.draw.line(surface, AZUL_OSCURO, (x + brick_width//2, y), (x + brick_width//2, y + brick_height), 2)
            else:
                pygame.draw.line(surface, AZUL_OSCURO, (x, y), (x, y + brick_height), 2)
                pygame.draw.line(surface, AZUL_OSCURO, (x + brick_width, y), (x + brick_width, y + brick_height), 2)
    
    return surface

def crear_camino_con_guia(ancho, alto):
    """Crea un camino completamente negro"""
    surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    
    # Fondo completamente negro
    pygame.draw.rect(surface, NEGRO, (0, 0, ancho, alto))
    
    return surface

def crear_spawn_area(ancho, alto):
    """Crea el área de spawn (gris muy sutil)"""
    surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    
    # Fondo negro con un toque muy sutil de gris
    pygame.draw.rect(surface, (20, 20, 20), (0, 0, ancho, alto))
    
    # Borde muy sutil
    pygame.draw.rect(surface, (40, 40, 40), (0, 0, ancho, alto), 1)
    
    return surface

# Sprites pre-generados para mejor rendimiento
SPRITES = {
    'pinguinos': [crear_pinguino(color) for color in COLORES_PINGUINOS],
    'fantasma': crear_fantasma(),
    'punto': crear_punto_pacman(),
    'muro': crear_muro_con_textura(32, 32),
    'camino': crear_camino_con_guia(32, 32),
    'spawn': crear_spawn_area(32, 32)
}

def obtener_sprite_jugador(player_id, direccion="down"):
    """Obtiene el sprite del jugador por su ID y dirección"""
    if 0 <= player_id < len(COLORES_PINGUINOS):
        return crear_pinguino_direccion(COLORES_PINGUINOS[player_id], direccion)
    return crear_pinguino_direccion(COLORES_PINGUINOS[0], direccion)  # Default

def obtener_sprite_fantasma(direccion="up"):
    """Obtiene el sprite del fantasma según la dirección"""
    return crear_fantasma_direccion(direccion)

def obtener_sprite_celda(valor_celda, direccion_jugador="down", direccion_fantasma="up"):
    """Obtiene el sprite apropiado según el valor de la celda y direcciones"""
    if valor_celda == 0:
        return SPRITES['camino']
    elif valor_celda == 1:
        return SPRITES['muro']
    elif valor_celda == 2:
        return SPRITES['spawn']
    elif valor_celda == 4:
        return SPRITES['punto']
    elif str(valor_celda) == "px":
        return obtener_sprite_fantasma(direccion_fantasma)
    elif str(valor_celda).startswith('p'):
        # Extraer ID del jugador
        try:
            player_id = int(str(valor_celda)[1:]) - 1
            return obtener_sprite_jugador(player_id, direccion_jugador)
        except:
            return obtener_sprite_jugador(0, direccion_jugador)
    
    return SPRITES['camino']  # Default
