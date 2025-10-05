import pygame
from config import *
from utils import obtener_url_servidor, generar_qr

QR_CODE = None
SERVER_URL = None

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
            MAP[y][x] = f"p{player_data['id']}"
            PLAYERS[ip]['position'] = (x, y)

def posicionar_enemigo():
    """Posiciona el enemigo en la esquina inferior del mapa"""
    x, y = ENEMY
    MAP[y][x] = "px"

def cargar_items():
    """Carga items en todas las posiciones con valor 0 (caminos)"""
    items_colocados = 0
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == 0:
                MAP[y][x] = 4
                items_colocados += 1
    return items_colocados

def contar_items_restantes():
    """Cuenta cuántos items quedan en el mapa"""
    items_restantes = 0
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == 4:
                items_restantes += 1
    return items_restantes

def determinar_ganador():
    """Determina el jugador con más puntos"""
    max_puntos = 0
    ganador = None
    
    for ip, player_data in PLAYERS.items():
        if player_data['points'] > max_puntos:
            max_puntos = player_data['points']
            ganador = player_data['username']
    
    return ganador, max_puntos

def mover_jugador(player_id, nueva_posicion):
    """Mueve un jugador a una nueva posición en el mapa"""
    pos_actual = None
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if MAP[y][x] == player_id:
                pos_actual = (x, y)
                break
        if pos_actual:
            break
    
    if pos_actual:
        MAP[pos_actual[1]][pos_actual[0]] = 0
        x, y = nueva_posicion
        MAP[y][x] = player_id
        return True
    return False

def puede_moverse_a(player_id, direccion):
    """Verifica si un jugador puede moverse en una dirección específica"""
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
    
    if (0 <= nueva_pos[0] < len(MAP[0]) and 
        0 <= nueva_pos[1] < len(MAP)):
        valor = MAP[nueva_pos[1]][nueva_pos[0]]
        
        if valor == 1:
            return False
        if str(valor).startswith('p') and str(valor) != player_id:
            return False
        if valor == "px":
            return False
        
        return True
    
    return False

def procesar_movimientos():
    """Procesa movimientos continuos de todos los jugadores estilo Pac-Man"""
    for ip, player_data in PLAYERS.items():
        player_id = f"p{player_data['id']}"
        direccion_actual = player_data['direccion']
        
        if puede_moverse_a(player_id, direccion_actual):
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
                else:
                    continue
                
                if MAP[nueva_pos[1]][nueva_pos[0]] == 4:
                    player_data['points'] += 10
                    
                    items_restantes = contar_items_restantes()
                    if items_restantes == 1:
                        mover_jugador(player_id, nueva_pos)
                        player_data['position'] = nueva_pos
                        return True
                
                if mover_jugador(player_id, nueva_pos):
                    player_data['position'] = nueva_pos
    
    return False

def test_players():
    """Agrega jugadores de prueba"""
    if len(PLAYERS) < 6:
        nueva_ip = f"127.0.0.{len(PLAYERS)+1}"
        
        if nueva_ip not in PLAYERS:
            max_id = max([player_data['id'] for player_data in PLAYERS.values()]) if PLAYERS else -1
            nuevo_id = max_id + 1
            
            PLAYERS[nueva_ip] = {
                "id": nuevo_id,
                "username": f"Jugador{len(PLAYERS)+1}",
                "position": (1, 1),
                "direccion": "right",
                "points": 0
            }

def dibujar_pantalla_espera(ventana):
    """Dibuja la pantalla de espera con QR"""
    global QR_CODE, SERVER_URL
    
    ventana.fill(NEGRO)
    
    if QR_CODE is None:
        SERVER_URL, ip = obtener_url_servidor(puerto=80)
        QR_CODE = generar_qr(SERVER_URL, qr_size=200)
    
    font_titulo = pygame.font.Font(None, 48)
    titulo = font_titulo.render("PYMAD SCAPE", True, BLANCO)
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
    
    qr_x = ANCHO//2 - 100
    qr_y = 120
    ventana.blit(QR_CODE, (qr_x, qr_y))
    
    font_url = pygame.font.Font(None, 24)
    url_texto = font_url.render(f"Escanea o visita: {SERVER_URL}", True, BLANCO)
    ventana.blit(url_texto, (ANCHO//2 - url_texto.get_width()//2, qr_y + 220))
    
    font_info = pygame.font.Font(None, 32)
    info_texto = f"Jugadores conectados: {len(PLAYERS)}/6"
    info = font_info.render(info_texto, True, BLANCO)
    ventana.blit(info, (ANCHO//2 - info.get_width()//2, qr_y + 270))
    
    font_jugadores = pygame.font.Font(None, 24)
    y_offset = qr_y + 320
    for i, ip in enumerate(PLAYERS.keys()):
        if ip in PLAYERS:
            username = PLAYERS[ip]['username']
            texto = f"Jugador {i+1}: {username}"
            superficie = font_jugadores.render(texto, True, BLANCO)
            ventana.blit(superficie, (ANCHO//2 - superficie.get_width()//2, y_offset))
            y_offset += 30
    
    if len(PLAYERS) < 6:
        instrucciones = font_jugadores.render("Esperando mas jugadores...", True, GRIS)
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, y_offset + 20))
        
        # Instrucción para agregar jugadores de prueba
        prueba = font_jugadores.render("Presiona R para agregar jugador de prueba", True, GRIS)
        ventana.blit(prueba, (ANCHO//2 - prueba.get_width()//2, y_offset + 50))
    else:
        iniciar = font_jugadores.render("Iniciando juego...", True, BLANCO)
        ventana.blit(iniciar, (ANCHO//2 - iniciar.get_width()//2, y_offset + 20))

def dibujar_pantalla_juego(window):
    """Dibuja la pantalla del juego"""
    window.fill(NEGRO)
    
    for fila in range(len(MAP)):
        for columna in range(len(MAP[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            
            valor = MAP[fila][columna]
            
            if valor == 0:
                color = NEGRO
            elif valor == 1:
                color = AZUL
            elif valor == 2:
                color = GRIS
            elif valor == 4:
                color = (255, 255, 0)
            elif str(valor) == "px":
                color = ROJO
            elif str(valor).startswith('p'):
                color = BLANCO
            else:
                color = NEGRO
            
            pygame.draw.rect(window, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
            
            if valor == 1:
                pygame.draw.rect(window, AZUL, (x, y, TAMANO_CELDA, TAMANO_CELDA), 1)
            elif str(valor) == "px":
                pygame.draw.rect(window, ROJO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)
            elif str(valor).startswith('p'):
                pygame.draw.rect(window, BLANCO, (x, y, TAMANO_CELDA, TAMANO_CELDA), 2)

def dibujar_puntajes(window):
    """Dibuja los puntajes de los jugadores en pantalla"""
    font = pygame.font.Font(None, 24)
    y_offset = 10
    
    items_restantes = contar_items_restantes()
    texto_items = f"Items restantes: {items_restantes}"
    superficie_items = font.render(texto_items, True, (255, 255, 0))
    window.blit(superficie_items, (10, y_offset))
    y_offset += 30
    
    for i, (ip, player_data) in enumerate(PLAYERS.items()):
        if i < 4:
            texto = f"{player_data['username']}: {player_data['points']} pts"
            superficie = font.render(texto, True, BLANCO)
            window.blit(superficie, (10, y_offset))
            y_offset += 25

def dibujar_pantalla_final(window):
    """Dibuja la pantalla de fin de juego con el ganador"""
    window.fill(NEGRO)
    
    if len(PLAYERS) == 0:
        font_titulo = pygame.font.Font(None, 72)
        titulo = font_titulo.render("GAME OVER", True, ROJO)
        window.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
        
        font_mensaje = pygame.font.Font(None, 36)
        mensaje = font_mensaje.render("Todos fueron atrapados!", True, BLANCO)
        window.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 300))
    else:
        max_puntos = 0
        ganador = None
        
        for ip, player_data in PLAYERS.items():
            if player_data['points'] > max_puntos:
                max_puntos = player_data['points']
                ganador = player_data['username']
        
        font_titulo = pygame.font.Font(None, 72)
        titulo = font_titulo.render("GANADOR", True, BLANCO)
        window.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
        
        font_ganador = pygame.font.Font(None, 48)
        texto_ganador = f"{ganador}"
        superficie_ganador = font_ganador.render(texto_ganador, True, (255, 255, 0))
        window.blit(superficie_ganador, (ANCHO//2 - superficie_ganador.get_width()//2, 300))
        
        font_puntos = pygame.font.Font(None, 36)
        texto_puntos = f"{max_puntos} puntos"
        superficie_puntos = font_puntos.render(texto_puntos, True, BLANCO)
        window.blit(superficie_puntos, (ANCHO//2 - superficie_puntos.get_width()//2, 350))
    
    font_instrucciones = pygame.font.Font(None, 24)
    instrucciones = font_instrucciones.render("Presiona ESC para salir", True, GRIS)
    window.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, 450))