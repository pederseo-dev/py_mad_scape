#!/usr/bin/env python3
"""
Cliente de ejemplo para conectarse al juego Pac-Man Multiplayer
Los jugadores pueden usar este script para controlar el juego desde sus dispositivos
"""

import requests
import time
import sys

# Configuración del servidor (cambia la IP por la IP de tu computadora)
SERVER_URL = "http://192.168.1.100:80"  # Cambia esta IP por la de tu computadora

def registrar_jugador(nombre):
    """Registra un jugador en el juego"""
    try:
        response = requests.post(f"{SERVER_URL}/register", 
                               json={"username": nombre})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['status']}")
            return True
        else:
            print(f"❌ Error al registrarse: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Verifica la IP y que el juego esté ejecutándose.")
        return False

def enviar_movimiento(direccion):
    """Envía un movimiento al servidor"""
    try:
        response = requests.post(f"{SERVER_URL}/move", 
                               json={"direction": direccion})
        if response.status_code == 200:
            data = response.json()
            print(f"🎮 {data['player']} se movió: {direccion}")
            return True
        else:
            print(f"❌ Error al mover: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor.")
        return False

def obtener_estado():
    """Obtiene el estado actual del juego"""
    try:
        response = requests.get(f"{SERVER_URL}/status")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Estado: {data['active_players']} jugadores activos")
            return data
        return None
    except:
        return None

def main():
    print("🎮 Cliente Pac-Man Multiplayer")
    print("=" * 40)
    
    # Obtener nombre del jugador
    nombre = input("Ingresa tu nombre de jugador: ").strip()
    if not nombre:
        nombre = "Jugador"
    
    # Registrar jugador
    if not registrar_jugador(nombre):
        return
    
    print("\n🎯 Controles:")
    print("w - Arriba")
    print("s - Abajo") 
    print("a - Izquierda")
    print("d - Derecha")
    print("q - Salir")
    print("h - Ver estado del juego")
    print("\n¡Presiona las teclas para moverte!")
    
    # Mapeo de teclas
    controles = {
        'w': 'up',
        's': 'down',
        'a': 'left',
        'd': 'right'
    }
    
    while True:
        try:
            tecla = input().lower().strip()
            
            if tecla == 'q':
                print("👋 ¡Hasta luego!")
                break
            elif tecla == 'h':
                obtener_estado()
            elif tecla in controles:
                enviar_movimiento(controles[tecla])
            else:
                print("❌ Tecla no válida. Usa w,a,s,d para moverte o q para salir")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
