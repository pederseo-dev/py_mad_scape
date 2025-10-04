import requests
import pygame
from config import *

def encontrar_casas_fantasmas():
    """Encuentra todas las posiciones de casas de fantasmas (valor 2) en el mapa"""
    casas = []
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == 2:
                casas.append((x, y))
    return casas


def posicionar_jugadores():
    """Posiciona los jugadores en las casas de fantasmas"""
    casas = encontrar_casas_fantasmas()
    for i, (ip, player_data) in enumerate(PLAYERS.items()):
        if i < len(casas):
            x, y = casas[i]
            MAP[y][x] = f"p{player_data['id']}"  # p1, p2, p3, etc.
            # Actualizar la posición en el diccionario PLAYERS
            PLAYERS[ip]['position'] = (x, y)

def posicionar_enemigo():
    """Posiciona el enemigo en la esquina inferior del mapa"""
    x, y = ENEMY  # Usar la posición definida en config.py
    MAP[y][x] = "px"  # px representa al enemigo

def cargar_items():
    """Carga items en todas las posiciones con valor 0 (caminos)"""
    items_colocados = 0
    
    # Recorrer todo el mapa y colocar items en posiciones con valor 0
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == 0:  # Si es un camino libre
                MAP[y][x] = 4   # Colocar item (valor 4)
                items_colocados += 1
    
    print(f"🍎 Total de items colocados: {items_colocados}")
    return items_colocados

def contar_items_restantes():
    """Cuenta cuántos items quedan en el mapa"""
    items_restantes = 0
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == 4:  # Si hay un item
                items_restantes += 1
    return items_restantes

def detectar_colision_items():
    """Detecta si algún jugador está en la misma posición que un item"""
    for ip, player_data in PLAYERS.items():
        player_id = f"p{player_data['id']}"
        posicion = player_data['position']
        x, y = posicion
        
        # Verificar si hay un item en la posición del jugador
        if MAP[y][x] == 4:  # Si hay un item
            # Sumar puntos
            player_data['points'] += 10
            # Remover item del mapa
            MAP[y][x] = 0
            print(f"🎯 {player_data['username']} recolectó un item! Puntos: {player_data['points']}")
            
            # Verificar si se acabaron los items
            items_restantes = contar_items_restantes()
            if items_restantes == 0:
                print("🏆 ¡Todos los items han sido recolectados!")
                ganador, puntos = determinar_ganador()
                # Cambiar a vista final
                import config
                config.WINDOW_VIEW = FINAL_VIEW
            
            return True
    return False

def determinar_ganador():
    """Determina el jugador con más puntos"""
    max_puntos = 0
    ganador = None
    
    for ip, player_data in PLAYERS.items():
        if player_data['points'] > max_puntos:
            max_puntos = player_data['points']
            ganador = player_data['username']
    
    print(f"🏆 ¡{ganador} gana con {max_puntos} puntos!")
    return ganador, max_puntos


def mover_jugador(player_id, nueva_posicion):
    """Mueve un jugador a una nueva posición en el mapa"""
    # Buscar la posición actual del jugador en el mapa
    pos_actual = None
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == player_id:
                pos_actual = (x, y)
                break
        if pos_actual:
            break
    
    if pos_actual:
        # Limpiar posición actual
        MAP[pos_actual[1]][pos_actual[0]] = 0
        # Colocar en nueva posición
        x, y = nueva_posicion
        MAP[y][x] = player_id
        return True
    return False

def puede_moverse_a(player_id, direccion):
    """Verifica si un jugador puede moverse en una dirección específica"""
    # Buscar posición actual del jugador
    pos_actual = None
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == player_id:
                pos_actual = (x, y)
                break
        if pos_actual:
            break
    
    if not pos_actual:
        return False
    
    x, y = pos_actual
    
    # Calcular nueva posición según dirección
    if direccion == "up":
        nueva_pos = (x, y-1)
    elif direccion == "down":
        nueva_pos = (x, y+1)
    elif direccion == "left":
        nueva_pos = (x-1, y)
    elif direccion == "right":
        nueva_pos = (x+1, y)
    else:
        return False
    
    # Verificar límites del mapa
    if (0 <= nueva_pos[0] < len(MAP[0]) and 
        0 <= nueva_pos[1] < len(MAP)):
        # Verificar que no sea un muro (valor 1)
        if MAP[nueva_pos[1]][nueva_pos[0]] != 1:
            # Verificar que no sea otro jugador (empieza con 'p')
            if not str(MAP[nueva_pos[1]][nueva_pos[0]]).startswith('p'):
                # Verificar que no sea el enemigo
                if MAP[nueva_pos[1]][nueva_pos[0]] != "px":
                    return True
    
    return False

def procesar_movimientos():
    """Procesa movimientos continuos de todos los jugadores estilo Pac-Man"""
    for ip, player_data in PLAYERS.items():
        player_id = f"p{player_data['id']}"
        direccion_actual = player_data['direccion']
        
        # Intentar moverse en la dirección actual
        if puede_moverse_a(player_id, direccion_actual):
            # Calcular nueva posición
            pos_actual = None
            for y in range(len(MAP)):
                for x in range(len(MAP[y])):
                    if MAP[y][x] == player_id:
                        pos_actual = (x, y)
                        break
                if pos_actual:
                    break
            
            if pos_actual:
                x, y = pos_actual
                if direccion_actual == "up":
                    nueva_pos = (x, y-1)
                elif direccion_actual == "down":
                    nueva_pos = (x, y+1)
                elif direccion_actual == "left":
                    nueva_pos = (x-1, y)
                elif direccion_actual == "right":
                    nueva_pos = (x+1, y)
                
                # Mover al jugador
                if mover_jugador(player_id, nueva_pos):
                    # Actualizar posición en el diccionario PLAYERS
                    player_data['position'] = nueva_pos


def test_players():
    if len(PLAYERS) < 6:  # Solo si no hay 6 jugadores aún
        # Crear una IP única para el nuevo jugador
        nueva_ip = f"127.0.0.{len(PLAYERS)+1}"  # 127.0.0.1, 127.0.0.2, etc.
        
        # Verificar que la IP no exista ya en PLAYERS
        if nueva_ip not in PLAYERS:
            # Obtener el siguiente ID disponible
            max_id = max([player_data['id'] for player_data in PLAYERS.values()]) if PLAYERS else -1
            nuevo_id = max_id + 1
            
            # Crear nuevo jugador en el diccionario PLAYERS
            PLAYERS[nueva_ip] = {
                "id": nuevo_id,                        # ID único basado en el máximo existente
                "username": f"Jugador{len(PLAYERS)+1}", # Nombre (Jugador1, Jugador2, etc.)
                "position": (1, 1),                    # Posición inicial en el mapa
                "direccion": "right",                  # Dirección inicial
                "points": 0                           # Puntuación inicial
            }
        # Nota: No usamos PLAYERS.append() porque PLAYERS es un diccionario, no una lista



def dibujar_pantalla_espera(ventana):
    """Dibuja la pantalla de espera"""
    ventana.fill(NEGRO)
    
    # Título
    font_titulo = pygame.font.Font(None, 48)
    titulo = font_titulo.render("PYMAD SCAPE", True, BLANCO)
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
    
    # Información de jugadores
    font_info = pygame.font.Font(None, 32)
    info_texto = f"Jugadores conectados: {len(PLAYERS)}/6"
    info = font_info.render(info_texto, True, BLANCO)
    ventana.blit(info, (ANCHO//2 - info.get_width()//2, 200))
    
    # Lista de jugadores
    font_jugadores = pygame.font.Font(None, 24)
    y_offset = 250
    for i, ip in enumerate(PLAYERS.keys()):
        if ip in PLAYERS:
            username = PLAYERS[ip]['username']
            texto = f"Jugador {i+1}: {username}"
            superficie = font_jugadores.render(texto, True, BLANCO)
            ventana.blit(superficie, (ANCHO//2 - superficie.get_width()//2, y_offset))
            y_offset += 30
    
    # Instrucciones
    if len(PLAYERS) < 6:
        instrucciones = font_jugadores.render("Esperando más jugadores...", True, GRIS)
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, y_offset + 20))
    else:
        iniciar = font_jugadores.render("¡Presiona ESPACIO para iniciar!", True, BLANCO)
        ventana.blit(iniciar, (ANCHO//2 - iniciar.get_width()//2, y_offset + 20))


def dibujar_pantalla_juego(window):
    """Dibuja la pantalla del juego"""
    window.fill(NEGRO)
    
    # Dibujar el mapa
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
            elif valor == 4:  # Items
                color = (255, 255, 0)  # AMARILLO para los items
            elif str(valor) == "px":  # Enemigo (verificar ANTES que los jugadores)
                color = ROJO  # ROJO para el enemigo
            elif str(valor).startswith('p'):  # Jugadores
                color = BLANCO
            else:
                color = NEGRO
            
            # Dibujar rectángulo
            pygame.draw.rect(window, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            
            # Dibujar borde para mejor visualización
            if valor == 1:
                pygame.draw.rect(window, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
            elif str(valor) == "px":  # Borde para enemigo (verificar ANTES que los jugadores)
                pygame.draw.rect(window, ROJO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)
            elif str(valor).startswith('p'):  # Borde para jugadores
                pygame.draw.rect(window, BLANCO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)

def dibujar_puntajes(window):
    """Dibuja los puntajes de los jugadores en pantalla"""
    font = pygame.font.Font(None, 24)
    y_offset = 10
    
    # Mostrar items restantes
    items_restantes = contar_items_restantes()
    texto_items = f"Items restantes: {items_restantes}"
    superficie_items = font.render(texto_items, True, (255, 255, 0))  # Amarillo
    window.blit(superficie_items, (10, y_offset))
    y_offset += 30
    
    # Mostrar puntajes de jugadores
    for i, (ip, player_data) in enumerate(PLAYERS.items()):
        if i < 4:  # Solo mostrar los primeros 4 jugadores
            texto = f"{player_data['username']}: {player_data['points']} pts"
            superficie = font.render(texto, True, BLANCO)
            window.blit(superficie, (10, y_offset))
            y_offset += 25

def dibujar_pantalla_final(window):
    """Dibuja la pantalla de fin de juego con el ganador"""
    window.fill(NEGRO)  # Fondo negro
    
    # Determinar ganador
    max_puntos = 0
    ganador = None
    
    for ip, player_data in PLAYERS.items():
        if player_data['points'] > max_puntos:
            max_puntos = player_data['points']
            ganador = player_data['username']
    
    # Título principal
    font_titulo = pygame.font.Font(None, 72)
    titulo = font_titulo.render("GANADOR", True, BLANCO)
    window.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
    
    # Nombre del ganador
    font_ganador = pygame.font.Font(None, 48)
    texto_ganador = f"{ganador}"
    superficie_ganador = font_ganador.render(texto_ganador, True, (255, 255, 0))  # Amarillo
    window.blit(superficie_ganador, (ANCHO//2 - superficie_ganador.get_width()//2, 300))
    
    # Puntos del ganador
    font_puntos = pygame.font.Font(None, 36)
    texto_puntos = f"{max_puntos} puntos"
    superficie_puntos = font_puntos.render(texto_puntos, True, BLANCO)
    window.blit(superficie_puntos, (ANCHO//2 - superficie_puntos.get_width()//2, 350))
    
    # Instrucciones
    font_instrucciones = pygame.font.Font(None, 24)
    instrucciones = font_instrucciones.render("Presiona ESC para salir", True, GRIS)
    window.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, 450))

# class simular_jugadores:
#     def __init__(self):
#         jugadores_activos = {}  # {player_id: {"ip":ip, "username": "Jugador1", "posicion": (x, y), "direccion": "right"}}
#         self.siguiente_id = 1  # Para asignar p1, p2, p3...





# #-----------------------------------------------------------------------------------------------
# def mover_jugador(mapa, jugador, nueva_pos):
#     # Buscar jugador en el mapa y borrarlo
#     for i, fila in enumerate(mapa):
#         for j, celda in enumerate(fila):
#             if celda == jugador:
#                 mapa[i][j] = 0  # dejar camino vacío
#     # Poner en nueva posición
#     x, y = nueva_pos
#     mapa[y][x] = jugador

# def aplicar_movimiento(mapa, jugador, direccion):
#     """Aplica un movimiento a un jugador en el mapa"""
#     # Buscar posición actual del jugador
#     pos_actual = None
#     for i, fila in enumerate(mapa):
#         for j, celda in enumerate(fila):
#             if celda == jugador:
#                 pos_actual = (j, i)  # (x, y)
#                 break
#         if pos_actual:
#             break
    
#     if not pos_actual:
#         return False
    
#     x, y = pos_actual
#     nueva_pos = None
    
#     # Calcular nueva posición según dirección
#     if direccion == "up" and y > 0 and mapa[y-1][x] == 0:
#         nueva_pos = (x, y-1)
#     elif direccion == "down" and y < len(mapa)-1 and mapa[y+1][x] == 0:
#         nueva_pos = (x, y+1)
#     elif direccion == "left" and x > 0 and mapa[y][x-1] == 0:
#         nueva_pos = (x-1, y)
#     elif direccion == "right" and x < len(mapa[0])-1 and mapa[y][x+1] == 0:
#         nueva_pos = (x+1, y)
    
#     if nueva_pos:
#         mover_jugador(mapa, jugador, nueva_pos)
#         return True
#     return False


# def procesar_movimientos_remotos():
#     """Procesa movimientos recibidos desde la API"""
#     try:
#         response = requests.get("http://localhost:80/movements", timeout=1)
#         if response.status_code == 200:
#             data = response.json()
#             return data.get("movements", [])
#     except:
#         pass
#     return []

# def mover_jugadores_remotos(MAP):
#     # Procesar movimientos remotos
#     movimientos = procesar_movimientos_remotos()
#     for movimiento in movimientos:
#         jugador_nombre = movimiento["player"]
#         direccion = movimiento["direction"]
        
#         # Asignar jugador según el nombre (puedes personalizar esta lógica)
#         if "1" in jugador_nombre or "player1" in jugador_nombre.lower():
#             aplicar_movimiento(MAP, "p1", direccion)
#         elif "2" in jugador_nombre or "player2" in jugador_nombre.lower():
#             aplicar_movimiento(MAP, "p2", direccion)
#         else:
#             # Si no hay especificación, usar p1 por defecto
#             aplicar_movimiento(MAP, "p1", direccion)
    

# ------------------------------------------------------------------------------------#