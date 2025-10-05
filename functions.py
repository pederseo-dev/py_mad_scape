import pygame
from config import *
from utils import obtener_url_servidor, generar_qr
from sprites import obtener_sprite_jugador, obtener_sprite_celda, obtener_sprite_fantasma, COLORES_PINGUINOS

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
            # Asegurar que los IDs empiecen en 1
            max_id = max([player_data['id'] for player_data in PLAYERS.values()]) if PLAYERS else 0
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
    
    # Fondo negro retro
    ventana.fill((0, 0, 0))  # Negro puro
    
    if QR_CODE is None:
        SERVER_URL, ip = obtener_url_servidor(puerto=80)
        QR_CODE = generar_qr(SERVER_URL, qr_size=200)
    
    # Título con estilo retro
    font_titulo = pygame.font.Font(None, 64)
    titulo = font_titulo.render("PYMAD SCAPE", True, (0, 255, 0))  # Verde neón
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 40))
    
    # Subtítulo
    font_subtitulo = pygame.font.Font(None, 24)
    subtitulo = font_subtitulo.render("MULTIPLAYER ARCADE", True, (255, 0, 128))  # Rosa neón
    ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 90))
    
    # QR Code con marco retro
    qr_x = ANCHO//2 - 110
    qr_y = 130
    pygame.draw.rect(ventana, (0, 255, 0), (qr_x - 10, qr_y - 10, 220, 220), 3)
    pygame.draw.rect(ventana, (255, 0, 128), (qr_x - 5, qr_y - 5, 210, 210), 2)
    ventana.blit(QR_CODE, (qr_x, qr_y))
    
    # URL con estilo
    font_url = pygame.font.Font(None, 20)
    url_texto = font_url.render(f"Escanea o visita: {SERVER_URL}", True, (255, 255, 255))
    ventana.blit(url_texto, (ANCHO//2 - url_texto.get_width()//2, qr_y + 230))
    
    # Información de jugadores con estilo retro
    font_info = pygame.font.Font(None, 28)
    info_texto = f"PLAYERS: {len(PLAYERS)}/6"
    info = font_info.render(info_texto, True, (0, 255, 0))
    ventana.blit(info, (ANCHO//2 - info.get_width()//2, qr_y + 260))
    
    # Mostrar jugadores con sus pingüinos
    font_jugadores = pygame.font.Font(None, 22)
    y_offset = qr_y + 300
    
    # Título de la sección de jugadores
    titulo_jugadores = font_jugadores.render("CONNECTED PLAYERS:", True, (255, 0, 128))
    ventana.blit(titulo_jugadores, (ANCHO//2 - titulo_jugadores.get_width()//2, y_offset))
    y_offset += 35
    
    # Mostrar cada jugador con su pingüino
    for i, ip in enumerate(PLAYERS.keys()):
        if ip in PLAYERS:
            player_data = PLAYERS[ip]
            username = player_data['username']
            player_id = player_data['id'] - 1  # Convertir a índice 0-based
            
            # Asegurar que el player_id esté en el rango correcto (0-5)
            if player_id >= len(COLORES_PINGUINOS):
                player_id = player_id % len(COLORES_PINGUINOS)
            
            # Obtener sprite del pingüino
            pinguino_sprite = obtener_sprite_jugador(player_id)
            
            # Posición del pingüino (lado izquierdo)
            pinguino_x = ANCHO//2 - 120
            pinguino_y = y_offset - 5
            
            # Dibujar pingüino
            ventana.blit(pinguino_sprite, (pinguino_x, pinguino_y))
            
            # Texto del jugador (lado derecho)
            texto = f"{username} (P{player_id + 1})"
            superficie = font_jugadores.render(texto, True, (255, 255, 255))
            ventana.blit(superficie, (ANCHO//2 - 60, y_offset))
            
            y_offset += 30
    
    if len(PLAYERS) < 6:
        instrucciones = font_jugadores.render("WAITING FOR PLAYERS...", True, (0, 255, 0))
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, y_offset + 20))
        
        # Instrucción para agregar jugadores de prueba
        prueba = font_jugadores.render("PRESS R FOR TEST PLAYER", True, (255, 0, 128))
        ventana.blit(prueba, (ANCHO//2 - prueba.get_width()//2, y_offset + 50))
        
    else:
        iniciar = font_jugadores.render("STARTING GAME...", True, (0, 255, 0))
        ventana.blit(iniciar, (ANCHO//2 - iniciar.get_width()//2, y_offset + 20))

def determinar_direccion_fantasma():
    """Determina la dirección de movimiento del fantasma basada en su posición anterior"""
    if not ENEMIGO:
        return "up"
    
    # Usar la dirección almacenada en el enemigo
    return ENEMIGO.get('direccion', 'up')

def dibujar_pantalla_juego(window):
    """Dibuja la pantalla del juego con sprites animados"""
    window.fill(NEGRO)
    
    # Determinar dirección del fantasma
    direccion_fantasma = determinar_direccion_fantasma()
    
    for fila in range(len(MAP)):
        for columna in range(len(MAP[fila])):
            x = columna * TAMANO_CELDA
            y = fila * TAMANO_CELDA
            
            valor = MAP[fila][columna]
            
            # Determinar dirección del jugador si es un jugador
            direccion_jugador = "down"  # Default
            if str(valor).startswith('p') and str(valor) != "px":
                # Buscar la dirección del jugador en PLAYERS
                try:
                    player_id = int(str(valor)[1:])
                    for ip, player_data in PLAYERS.items():
                        if player_data['id'] == player_id:
                            direccion_jugador = player_data.get('direccion', 'down')
                            break
                except:
                    pass
            
            # Obtener el sprite apropiado para esta celda con direcciones
            if str(valor) == "px":
                sprite = obtener_sprite_fantasma(direccion_fantasma)
            elif str(valor).startswith('p') and str(valor) != "px":
                try:
                    player_id = int(str(valor)[1:]) - 1
                    sprite = obtener_sprite_jugador(player_id, direccion_jugador)
                except:
                    sprite = obtener_sprite_jugador(0, direccion_jugador)
            else:
                sprite = obtener_sprite_celda(valor)
            
            # Escalar el sprite al tamaño de la celda si es necesario
            if sprite.get_width() != TAMANO_CELDA or sprite.get_height() != TAMANO_CELDA:
                sprite = pygame.transform.scale(sprite, (TAMANO_CELDA, TAMANO_CELDA))
            
            # Dibujar el sprite
            window.blit(sprite, (x, y))

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
    # Fondo negro retro
    window.fill((0, 0, 0))
    
    if len(PLAYERS) == 0:
        # Game Over
        font_titulo = pygame.font.Font(None, 80)
        titulo = font_titulo.render("GAME OVER", True, (255, 0, 0))
        window.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 180))
        
        font_mensaje = pygame.font.Font(None, 32)
        mensaje = font_mensaje.render("ALL PLAYERS CAUGHT!", True, (0, 255, 0))
        window.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 280))
        
        # Dibujar fantasma en el centro
        fantasma_sprite = obtener_sprite_fantasma("down")
        fantasma_sprite = pygame.transform.scale(fantasma_sprite, (64, 64))
        window.blit(fantasma_sprite, (ANCHO//2 - 32, 320))
        
    else:
        # Ganador
        max_puntos = 0
        ganador = None
        
        for ip, player_data in PLAYERS.items():
            if player_data['points'] > max_puntos:
                max_puntos = player_data['points']
                ganador = player_data['username']
        
        font_titulo = pygame.font.Font(None, 80)
        titulo = font_titulo.render("WINNER", True, (0, 255, 0))
        window.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 180))
        
        font_ganador = pygame.font.Font(None, 48)
        texto_ganador = f"{ganador}"
        superficie_ganador = font_ganador.render(texto_ganador, True, (255, 0, 128))
        window.blit(superficie_ganador, (ANCHO//2 - superficie_ganador.get_width()//2, 280))
        
        font_puntos = pygame.font.Font(None, 32)
        texto_puntos = f"{max_puntos} POINTS"
        superficie_puntos = font_puntos.render(texto_puntos, True, (255, 255, 0))
        window.blit(superficie_puntos, (ANCHO//2 - superficie_puntos.get_width()//2, 330))
        
        # Dibujar pingüino ganador
        for ip, player_data in PLAYERS.items():
            if player_data['username'] == ganador:
                player_id = player_data['id'] - 1
                pinguino_ganador = obtener_sprite_jugador(player_id, "down")
                pinguino_ganador = pygame.transform.scale(pinguino_ganador, (64, 64))
                window.blit(pinguino_ganador, (ANCHO//2 - 32, 370))
                break
    
    font_instrucciones = pygame.font.Font(None, 24)
    instrucciones = font_instrucciones.render("PRESS ESC TO EXIT", True, (0, 255, 0))
    window.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, 450))