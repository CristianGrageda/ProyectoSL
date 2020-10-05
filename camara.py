import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

# --- CLASE CAMARA ---
class Camara:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.ANCHO, self.ALTO = 800, 600
        self.CONST = vec(-self.ANCHO / 2 + player.rect.w / 2,-self.ALTO / 2 + player.rect.h / 2)

    # -- Metodo para cambiar el modo de la camara --
    def cambiar_modo(self, modo):
        self.modo = modo

    # -- Metodo que mueve la camara segun el modo --
    def scroll(self):
        self.modo.scroll()

class CamScroll(ABC):
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

# --- CLASE PARA QUE LA CAMARA SIGA AL JUGADOR ---
class Seguir(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    # -- Movimiento de camara --
    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

# --- CLASE PARA QUE LA CAMARA SIGA AL JUGADOR CON BORDES LIMITADOS ---
class Limite(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    # -- Movimiento de camara --
    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.borde_izquierdo, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.borde_derecho - self.camera.ANCHO)
        self.camera.offset.y = max(self.player.borde_arriba, self.camera.offset.y)
        self.camera.offset.y = min(self.camera.offset.y, self.player.borde_abajo - self.camera.ALTO)











