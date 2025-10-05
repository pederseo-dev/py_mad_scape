import socket

def obtener_ip_local():
    """Obtiene la IP local de la máquina en la red"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generar_qr(url, qr_size=200):
    """Genera un código QR para la URL proporcionada"""
    try:
        import qrcode
        from PIL import Image
        import pygame
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        img_str = img.tobytes()
        img_size = img.size
        
        py_image = pygame.image.fromstring(img_str, img_size, 'RGB')
        
        return py_image
        
    except ImportError:
        import pygame
        surface = pygame.Surface((qr_size, qr_size))
        surface.fill((255, 255, 255))
        
        font = pygame.font.Font(None, 24)
        texto = font.render("QR no disponible", True, (0, 0, 0))
        surface.blit(texto, (qr_size//2 - texto.get_width()//2, qr_size//2))
        
        return surface
        
    except Exception:
        import pygame
        surface = pygame.Surface((qr_size, qr_size))
        surface.fill((255, 255, 255))
        
        font = pygame.font.Font(None, 20)
        texto = font.render("Error en QR", True, (255, 0, 0))
        surface.blit(texto, (qr_size//2 - texto.get_width()//2, qr_size//2))
        
        return surface

def obtener_url_servidor(puerto=80):
    """Obtiene la URL completa del servidor"""
    ip = obtener_ip_local()
    url = f"http://{ip}:{puerto}"
    return url, ip