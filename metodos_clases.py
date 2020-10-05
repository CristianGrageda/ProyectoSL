
# --- MODULOS ---
import pygame, copy, random
from camara import *

pygame.init()

# --- FUNCION CONSTRUIR MAPA ---
def construir_mapa(mapa, muro, item, pozo):
    muros = []
    items = []
    pozos = []
    x, y = 0, 0
    
    for fila in mapa:
        for columna in fila:
            if columna == "M":
                muros.append([muro, pygame.Rect(x, y, 50, 50)])
            elif columna == "I":
                items.append([item, pygame.Rect(x, y, 50, 50)])
            elif columna == "R":
                pozos.append([pozo, pygame.Rect(x, y, 50, 50)])
            x += 50
        x = 0
        y += 50
    return muros, items, pozos

# --- FUNCION PINTAR MAPA ---
def pintar_mapa(ventana_juego, paredes, cam_x, cam_y):

    for fila in paredes:
        for columna in fila:
            ventana_juego.blit(columna[0], (columna[1].x - cam_x,columna[1].y - cam_y))

############################## CLASE FONDO ##############################
class Fondo(pygame.sprite.Sprite):
    def __init__(self, camara, camara_seguir, camara_limitada):
        pygame.display.set_caption("Juego Pygame")
        self.salvapantalla = pygame.image.load("multimedia/fondo.gif").convert()
        self.image = pygame.image.load("multimedia/fondo_1.gif").convert()
        self.rect = self.image.get_rect()
        self.camara = camara
        self.camara_seguir = camara_seguir
        self.camara_limitada = camara_limitada

    # -- METODO PARA CAMBIAR SEGUIMIENTO DE CAMARA --
    def modo_de_camara(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.camara.cambiar_modo(self.camara_seguir)
            elif event.key == pygame.K_2:
                self.camara.cambiar_modo(self.camara_limitada)

    # -- METODO PARA PINTAR FONDO --
    def update(self, ventana, x, y):
            
        ventana.blit(self.salvapantalla,(0,0))
        ventana.blit(self.image, (0 - x, 0 - y))

############################## CLASE PLAYER ##############################
class Player(pygame.sprite.Sprite):
    def __init__(self, mitad_ancho, mitad_alto):
        # - datos -
        self.pulsado = True
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.medio_x, self.medio_y = 30, 45
        self.posicion = 0
        self.borde_izquierdo, self.borde_derecho = 0, 1600
        self.borde_arriba, self.borde_abajo = 0, 1200
        self.sonido_item = pygame.mixer.Sound("sonidos/item.wav")
        self.sonido_disparo = pygame.mixer.Sound("sonidos/disparo.wav")
        self.sonido_caminar = pygame.mixer.Sound("sonidos/caminar.wav")
        # - carga de imagen y configuracion de frames -
        self.sheet = pygame.image.load('multimedia/player.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(41, 34, 57, 84))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = mitad_ancho - self.medio_x, mitad_alto - self.medio_y
        self.frame = 0 
        self.retardo_frame = 0
        self.izquierda_direccion = { 0: (35, 268, 66, 84), 1: (185, 268, 66, 84), 2: (335, 268, 66, 84), 3: (485, 268, 66, 84), 4: (635, 268, 66, 84), 5: (785, 268, 66, 84), 6: (935, 268, 66, 84) }
        self.derecha_direccion = { 0: (39, 385, 66, 84), 1: (189, 385, 66, 84), 2: (339, 385, 66, 84), 3: (489, 385, 66, 84), 4: (639, 385, 66, 84), 5: (789, 385, 66, 84), 6: (939, 385, 66, 84) }
        self.arriba_direccion = { 0: (41, 151, 57, 84), 1: (191, 151, 57, 84), 2: (341, 151, 57, 84), 3: (491, 151, 57, 84), 4: (641, 151, 57, 84), 5: (791, 151, 57, 84), 6: (941, 151, 57, 84) }
        self.abajo_direccion = { 0: (41, 34, 57, 84), 1: (191, 34, 57, 84), 2: (341, 34, 57, 84), 3: (491, 34, 57, 84), 4: (641, 34, 57, 84), 5: (791, 34, 57, 84), 6: (941, 34, 57, 84) }

    # --- CAMBIO DE FRAME CON UN RETARDO DE 5 INCREMENTOS ---
    def get_frame(self, frame_set):
        self.retardo_frame += 1

        if self.retardo_frame == 5:
            self.frame += 1
            self.retardo_frame = 0
            if self.frame == 1 or self.frame == 4:
                self.sonido_caminar.play()
        if self.frame > (len(frame_set) - 2):
            self.frame = 0
        return frame_set[self.frame]

    # --- SELECCIONAMOS UN FRAGMENTO DE LA IMAGEN ---
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    # --- ACTUALIZA FRAMES (movimiento y direccion de sprite) ---
    def animacion(self, direccion):
    	# - Movimientos -
        if direccion == 'izquierda':
            self.clip(self.izquierda_direccion)
        if direccion == 'derecha':
            self.clip(self.derecha_direccion)
        if direccion == 'arriba':
            self.clip(self.arriba_direccion)
        if direccion == 'abajo':
            self.clip(self.abajo_direccion)

        # - Quieto -
        if direccion == 'quieto_izquierda':
            self.clip(self.izquierda_direccion[0])
        if direccion == 'quieto_derecha':
            self.clip(self.derecha_direccion[0])
        if direccion == 'quieto_arriba':
            self.clip(self.arriba_direccion[0])
        if direccion == 'quieto_abajo':
            self.clip(self.abajo_direccion[0])
        
        # - Creo que carga el fragmento seleccionado de la imagen -
        self.image = self.sheet.subsurface(self.sheet.get_clip())


    # --- ACTUALIZA AL JUGADOR ---
    def update(self, evento, paredes, all_sprites, cam):
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclado = pygame.key.get_pressed()
        self.evento = evento
        # -- Detecta teclas presionadas para iniciar movimiento y animacion --
        if teclado[pygame.K_LEFT]:
            self.velocidad_x = -5
            self.animacion('izquierda')
            self.posicion = 3
        if teclado[pygame.K_RIGHT]:
            self.velocidad_x = 5
            self.animacion('derecha')
            self.posicion = 2
        if teclado[pygame.K_UP]:
            self.velocidad_y = -5
            self.animacion('arriba')
            self.posicion = 1
        if teclado[pygame.K_DOWN]:
            self.velocidad_y = 5
            self.animacion('abajo')
            self.posicion = 0

        # -- Detecta la ultima letra presionada para detener la animacion --
        if self.evento.type == pygame.KEYUP:
            if self.evento.key == pygame.K_LEFT and (teclado[pygame.K_RIGHT] == False and teclado[pygame.K_UP] == False and teclado[pygame.K_DOWN] == False):
                self.animacion('quieto_izquierda')
                self.posicion = 3
            elif self.evento.key == pygame.K_RIGHT and (teclado[pygame.K_LEFT] == False and teclado[pygame.K_UP] == False and teclado[pygame.K_DOWN] == False):
                self.animacion('quieto_derecha')
                self.posicion = 2
            elif self.evento.key == pygame.K_UP and (teclado[pygame.K_RIGHT] == False and teclado[pygame.K_LEFT] == False and teclado[pygame.K_DOWN] == False):
                self.animacion('quieto_arriba')
                self.posicion = 1
            elif self.evento.key == pygame.K_DOWN and (teclado[pygame.K_RIGHT] == False and teclado[pygame.K_UP] == False and teclado[pygame.K_LEFT] == False):
                self.animacion('quieto_abajo')
                self.posicion = 0
        # -- Dispara con Espacio (la bala sale segun la posicion del Jugador) --
        if self.evento.type == pygame.KEYDOWN:        
            if self.evento.key == pygame.K_SPACE and self.pulsado:
                self.sonido_disparo.stop()
                if self.posicion == 0:
                    self.disparar(all_sprites, self.rect.centerx-15, self.rect.centery)
                elif self.posicion == 1:
                    self.disparar(all_sprites, self.rect.centerx+10, self.rect.centery)
                elif self.posicion == 2:
                    self.disparar(all_sprites, self.rect.centerx, self.rect.centery+10)
                elif self.posicion == 3:
                    self.disparar(all_sprites, self.rect.centerx, self.rect.centery+10)
                self.sonido_disparo.play()
                self.pulsado = False
        if self.evento.type == pygame.KEYUP:        
            if self.evento.key == pygame.K_SPACE:
                self.pulsado = True
        
            
        # -- Actualiza movimientos del Jugador --
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # -- Colision con paredes (0=pared , 1=item) --
        for pared in paredes[0]:
            if pared[1].colliderect(self.rect):
                self.rect.x -= self.velocidad_x
                self.rect.y -= self.velocidad_y

        for item in copy.copy(paredes[1]):
            if self.rect.collidepoint(item[1].centerx, item[1].centery):
                paredes[1].remove(item)
                self.sonido_item.play()
    # -- Al pulsar espacio se crea un disparo (Clase) --
    def disparar(self, allsprites, x, y):
        bullet = Disparo(x, y, self.posicion)
        allsprites.add(bullet)
        

############################## CLASE DISPARO ##############################
class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, posicion):
        super().__init__()
        self.image = pygame.image.load("multimedia/disparo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # - Velocidad de la bala -
        self.speedy = 15
        # - Direccion hacia donde ira la bala -
        self.p = posicion

    # -- ACTUALIZA DISPARO --
    def update(self, paredes, camara, ventana):
        # -- Direccion de la bala segun donde mira el Jugador --
        if self.p == 0:
            self.rect.y += self.speedy
        elif self.p == 1:
            self.rect.y -= self.speedy
        elif self.p == 2:
            self.rect.x += self.speedy
        elif self.p == 3:
            self.rect.x -= self.speedy
        
        # -- Si la bala colisiona con algo, desaparece --
        for pared in paredes[0]:
            if pared[1].colliderect(self.rect):
                self.kill()
        for pared in paredes[1]:
            if pared[1].colliderect(self.rect):
                self.kill()

        # -- Pintar bala --
        ventana.blit(self.image,(self.rect.x - camara.offset.x, self.rect.y - camara.offset.y))

############################## CLASE ENEMIGO ##############################
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("multimedia/arania.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = random.randrange(1,5)
        self.speed_y = random.randrange(1,5)

    # -- ACTUALIZA ENEMIGO --
    def update(self, paredes, camara, ventana):
        # -- Se mueve en vertical --
        self.rect.y += self.speed_y

        # -- Si colisiona con pared, rebota --
        for pared in paredes[0]:
            if pared[1].colliderect(self.rect):
                self.speed_y *= -1
        # -- Pintar Enemigo --
        ventana.blit(self.image,(self.rect.x - camara.offset.x, self.rect.y - camara.offset.y))

        