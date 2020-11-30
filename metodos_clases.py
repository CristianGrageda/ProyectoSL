
# --- MODULOS ---
import pygame, copy, random
from camara import *

pygame.init()

# --- FUNCION CONSTRUIR MAPA ---
def construir_mapa(mapa, muro, muro_roto, item, pozo, botiquin, mancha, misil, player):
    muros = []
    items = []
    pozos = []
    botiquines = []
    manchas = []
    x, y = 0, 0
    player.alien_muertos, player.items = 0, 0
    
    for fila in mapa:
        for columna in fila:
            if columna == "M":
                muros.append([muro, pygame.Rect(x, y, 50, 50)])
            elif columna == "N":
                muros.append([muro_roto, pygame.Rect(x, y, 50, 50)])
                player.alien_muertos += 4
            elif columna == "I":
                items.append([item, pygame.Rect(x, y, 50, 50)])
                player.items += 1
            elif columna == "B":
                botiquines.append([botiquin, pygame.Rect(x, y, 50, 50)])
            elif columna == "C":
                muros.append([misil, pygame.Rect(x, y, 50, 50)])
            elif columna == "R":
                pozos.append([pozo, pygame.Rect(x, y, 50, 50)])
                player.alien_muertos += 1
            elif columna == "S":
                manchas.append([mancha, pygame.Rect(x, y, 50, 50)])
                player.alien_muertos += 1
            x += 50
        x = 0
        y += 50
    return muros, items, pozos, botiquines, manchas

# --- FUNCION PINTAR MAPA ---
def pintar_mapa(ventana_juego, paredes, cam_x, cam_y):

    for fila in paredes:
        for columna in fila:
            ventana_juego.blit(columna[0], (columna[1].x - cam_x,columna[1].y - cam_y))

############################## CLASE FONDO ##############################
class Fondo(pygame.sprite.Sprite):
    def __init__(self, camara, camara_seguir, camara_limitada, nivel):
        pygame.display.set_caption("Juego Pygame")
        self.salvapantalla = pygame.image.load("multimedia/fondo.png").convert()
        if nivel == 1:
            self.image = pygame.image.load("multimedia/fondo_1.gif").convert()
        elif nivel == 2:
            self.image = pygame.image.load("multimedia/fondo_2.gif").convert()
        elif nivel == 3:
            self.image = pygame.image.load("multimedia/fondo_final.png").convert()
        self.rect = self.image.get_rect()
        if nivel == 1 or nivel == 2:
            self.camara = camara
            self.camara_seguir = camara_seguir
            self.camara_limitada = camara_limitada

    # -- METODO PARA CAMBIAR SEGUIMIENTO DE CAMARA --
    def modo_de_camara(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                self.camara.cambiar_modo(self.camara_seguir)
            elif evento.key == pygame.K_2:
                self.camara.cambiar_modo(self.camara_limitada)

    # -- METODO PARA PINTAR FONDO --
    def update(self, ventana, x, y):
            
        ventana.blit(self.salvapantalla,(0,0))
        ventana.blit(self.image, (0 - x, 0 - y))

############################## CLASE PLAYER ##############################
class Player(pygame.sprite.Sprite):
    def __init__(self, mitad_ancho, mitad_alto, nivel):
        # - datos -
        self.nivel = nivel
        self.vida_total = 100
        self.vida = self.vida_total
        self.pulsado = True
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.medio_x, self.medio_y = 30, 45
        self.sonido_item = pygame.mixer.Sound("sonidos/item.wav")
        self.sonido_disparo = pygame.mixer.Sound("sonidos/disparo.wav")
        self.sonido_caminar = pygame.mixer.Sound("sonidos/caminar.wav")
        self.sonido_vida = pygame.mixer.Sound("sonidos/vida.wav")
        self.mas_respawn = False
        self.posicion = 0

        if self.nivel == 1 or self.nivel == 2:
            self.items = 0
            self.alien_muertos = 0
            
            if self.nivel == 1:
                self.borde_izquierdo, self.borde_derecho = 0, 1600
                self.borde_arriba, self.borde_abajo = 0, 1200
            elif self.nivel == 2:
                self.borde_izquierdo, self.borde_derecho = 0, 2000
                self.borde_arriba, self.borde_abajo = 0, 1600
            elif self.nivel == 3:
                self.borde_izquierdo, self.borde_derecho = 0, 1600
                self.borde_arriba, self.borde_abajo = 0, 1200
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

        elif self.nivel == 3:
            self.botiquin_disponible = 3
            self.misil_disponible = 2
            self.oleada_aranias = 10
            self.oleada_aereos = 2
            self.sonido_misil = pygame.mixer.Sound("sonidos/disparar_misil.wav")
            self.sheet = pygame.image.load('multimedia/player_final.png').convert_alpha()
            self.sheet.set_clip(pygame.Rect(4, 6, 35, 96))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = mitad_ancho - self.medio_x, mitad_alto - self.medio_y
            self.frame = 0 
            self.retardo_frame = 0
            self.izquierda_direccion = { 0: (4, 6, 35, 96), 1: (101, 6, 35, 96), 2: (198, 6, 35, 96), 3: (295, 6, 35, 96), 4: (392, 6, 35, 96), 5: (489, 6, 35, 96), 6: (586, 6, 35, 96) }
            self.derecha_direccion = self.izquierda_direccion
            
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
    def update(self, mapa, all_sprites, cam, aliens):
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclado = pygame.key.get_pressed()
        if self.nivel == 1 or self.nivel == 2:
            # -- Detecta teclas presionadas para iniciar movimiento y animacion --
            if teclado[pygame.K_LEFT] or teclado[pygame.K_a]:
                self.velocidad_x = -5
                self.animacion('izquierda')
                self.posicion = 3
            if teclado[pygame.K_RIGHT] or teclado[pygame.K_d]:
                self.velocidad_x = 5
                self.animacion('derecha')
                self.posicion = 2
            if teclado[pygame.K_UP] or teclado[pygame.K_w]:
                self.velocidad_y = -5
                self.animacion('arriba')
                self.posicion = 1
            if teclado[pygame.K_DOWN] or teclado[pygame.K_s]:
                self.velocidad_y = 5
                self.animacion('abajo')
                self.posicion = 0

            # - Colision con item, item desaparece -
            for item in copy.copy(mapa[1]):
                if self.rect.collidepoint(item[1].centerx, item[1].centery):
                    mapa[1].remove(item)
                    self.sonido_item.play()
                    self.items -= 1
                    # - Al llegar a 6, 3 o 2 items, reaparecer enemigos tipo 1 -
                    if self.items == 6 or self.items == 3 or self.items == 2:
                        self.mas_respawn = True
            # - Colision con botiquin, botiquin desaparece y suma vida del jugador -
            for botiquin in copy.copy(mapa[3]):
                if self.rect.collidepoint(botiquin[1].centerx, botiquin[1].centery):
                    # - Solo suma vida cuando el jugador tenga vida menos a 100, sino no cura -
                    if self.vida < self.vida_total:
                        mapa[3].remove(botiquin)
                        self.sonido_vida.play()
                        self.vida += 15
                        if self.vida > self.vida_total:
                            self.vida = self.vida_total
            # - Colision con aliens, resta vida segun tipo de alien -
            for alien in aliens:
                if alien.tipo == 0:
                    if self.rect.collidepoint(alien.rect.centerx, alien.rect.centery):
                        self.vida -= 1
                elif alien.tipo == 1:
                    if self.rect.colliderect(alien.rect):
                        self.vida -= 0.5
                elif alien.tipo == 2:
                    if self.rect.colliderect(alien.rect):
                        self.vida -= 2
        elif self.nivel == 3:
            # -- Detecta teclas presionadas para iniciar movimiento y animacion --
            if teclado[pygame.K_LEFT] or teclado[pygame.K_a]:
                self.velocidad_x = -5
                self.animacion('izquierda')
                self.posicion = 3
            if teclado[pygame.K_RIGHT] or teclado[pygame.K_d]:
                self.velocidad_x = 5
                self.animacion('derecha')
                self.posicion = 2
            # - Colision con aliens, resta vida segun tipo de alien -
            for alien in aliens:
                if alien.tipo == 0:
                    if self.rect.collidepoint(alien.rect.centerx, alien.rect.centery):
                        self.vida -= 2
                        alien.kill()
                        aliens.remove(alien)
                        self.oleada_aranias -= 1
                elif alien.tipo == 1:
                    if self.rect.colliderect(alien.rect):
                        self.vida -= 1
                        alien.kill()
                        aliens.remove(alien)
        # -- Actualiza movimientos del Jugador --
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        # -- Colision con el mapa (0=pared , 1=item , 3=botiquin) --
        # - Colision con pared, el personaje se queda quieto -
        for pared in mapa[0]:
            if pared[1].colliderect(self.rect):
                self.rect.x -= self.velocidad_x
                self.rect.y -= self.velocidad_y
        



    # -- Al pulsar espacio se crea un disparo (Clase) --
    def disparar(self, allsprites, x, y, tipo):
        bullet = Disparo(x, y, self.posicion, tipo)
        allsprites.add(bullet)
        

############################## CLASE DISPARO ##############################
class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, posicion, tipo):
        super().__init__()
        self.tipo = tipo
        if self.tipo == 0:
            self.image = pygame.image.load("multimedia/disparo.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
            # - Velocidad de la bala -
            self.speedy = 15
            # - Direccion hacia donde ira la bala -
            self.p = posicion
            self.s_pared = pygame.mixer.Sound("sonidos/disparo_pared.wav")
        elif self.tipo == 1:
            self.image = pygame.image.load("multimedia/misil.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
            # - Velocidad de la bala -
            self.speedy = 10
            self.s_pared = pygame.mixer.Sound("sonidos/misil_explota.wav")
            self.sonido_dolor_boss = pygame.mixer.Sound("sonidos/sonido_dolor.wav")

    # -- ACTUALIZA DISPARO --
    def update(self, paredes, camara_x, camara_y, ventana, aliens, player, allsprites):
        if self.tipo == 0:
            # -- Direccion de la bala segun donde mira el Jugador --
            if player.nivel == 1 or player.nivel == 2:
                if self.p == 0:
                    self.rect.y += self.speedy
                elif self.p == 1:
                    self.rect.y -= self.speedy
                elif self.p == 2:
                    self.rect.x += self.speedy
                elif self.p == 3:
                    self.rect.x -= self.speedy
            
                # -- Si la bala colisiona las paredes o items, desaparece --
                for pared in paredes[0]:
                    if pared[1].colliderect(self.rect):
                        self.kill()
                for pared in paredes[1]:
                    if pared[1].colliderect(self.rect):
                        self.kill()

            elif player.nivel == 3:
                camara_x = 7
                self.rect.y -= self.speedy
                if self.rect.y < 0:
                    self.kill()

            # -- Si la bala colisiona con los aliens, desaparece y le resta vida --               
            for alien in aliens:
                if alien.rect.colliderect(self.rect):
                    self.s_pared.play()
                    self.kill()
                    if player.nivel == 1 or player.nivel == 2:
                        alien.vida -= 1
                    elif player.nivel == 3:
                        alien.vida -= 2

                    if alien.vida <= 0:
                        alien.kill()
                        aliens.remove(alien)
                        player.alien_muertos -= 1
                        alien.sonido_muerte.play()
                        if player.nivel == 3 and alien.tipo == 0:
                            player.oleada_aranias -= 1
        elif self.tipo == 1:
            self.rect.y -= self.speedy
            for alien in aliens:
                if alien.rect.colliderect(self.rect) and alien.tipo != 9:
                    alien.vida -= 2
                    if alien.vida <= 0:
                        alien.kill()
                        aliens.remove(alien)
                        player.alien_muertos -= 1
                        alien.sonido_muerte.play()
                        if alien.tipo == 0:
                            player.oleada_aranias -= 1

                if alien.rect.collidepoint(self.rect.centerx, self.rect.centery) and alien.tipo == 9:
                    self.s_pared.play()
                    self.kill()
                    alien.vida -= 50
                    self.sonido_dolor_boss.play()
                    if alien.vida <= 0:
                        alien.vida = 0
                        alien.kill()
                        aliens.remove(alien)
                    


                

        # -- Pintar bala --
        ventana.blit(self.image,(self.rect.x - camara_x, self.rect.y - camara_y))

############################## CLASE ENEMIGO ##############################
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        if tipo == 0:
            self.tipo = 0
            self.vida = 5
            self.speed_x = random.randrange(3,5)
            self.speed_y = random.randrange(3,5)
            self.direccion = random.randint(0,1)
            self.vertical = 1
            self.horizontal = 1
            self.sheet = pygame.image.load('multimedia/alien.png').convert_alpha()
            self.sheet.set_clip(pygame.Rect(9, 18, 43, 33))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.rect = self.image.get_rect()
            self.frame = 0 
            self.retardo_frame = 0
            self.arriba_direccion = { 0: (9, 18, 43, 33), 1: (72, 12, 44, 36), 2: (137, 10, 43, 37), 3: (201, 19, 43, 30) }
            self.izquierda_direccion = { 0: (16, 79, 32, 37), 1: (71, 79, 40, 37), 2: (132, 82, 41, 34), 3: (203, 79, 35, 37) }
            self.abajo_direccion = { 0: (9, 142, 43, 36), 1: (73, 144, 43, 39), 2: (135, 148, 47, 35), 3: (201, 146, 43, 33) }
            self.derecha_direccion = { 0: (15, 207, 32, 37), 1: (80, 207, 40, 37), 2: (146, 210, 42, 34), 3: (209, 207, 35, 37) }
            self.rect.x = x
            self.rect.y = y
        elif tipo == 1:
            self.tipo = 1
            self.vida = 2
            self.speed_x = random.randrange(2,3)
            self.speed_y = random.randrange(2,3)
            self.sheet = pygame.image.load('multimedia/alien_volador.png').convert_alpha()
            self.sheet.set_clip(pygame.Rect(7, 5, 52, 36))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.rect = self.image.get_rect()
            self.frame = 0 
            self.retardo_frame = 0
            self.arriba_direccion = { 0: (7, 5, 52, 36), 1: (77, 3, 42, 41), 2: (137, 11, 52, 25), 3: (202, 9, 52, 29) }
            self.rect.x = x
            self.rect.y = y
        elif tipo == 2:
            self.tipo = 2
            self.vida = 20
            self.speed_x = 2
            self.sheet = pygame.image.load('multimedia/slime.png').convert_alpha()
            self.sheet.set_clip(pygame.Rect(0, 0, 150, 150))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.rect = self.image.get_rect()
            self.frame = 0 
            self.retardo_frame = 0
            self.derecha_direccion = { 0: (0, 0, 150, 150), 1: (150, 0, 150, 150), 2: (300, 0, 150, 150), 3: (450, 0, 150, 150), 4: (600, 0, 150, 150), 5: (750, 0, 150, 150)}
            self.izquierda_direccion = { 0: (0, 150, 150, 150), 1: (150, 150, 150, 150), 2: (300, 150, 150, 150), 3: (450, 150, 150, 150), 4: (600, 150, 150, 150), 5: (750, 150, 150, 150)}
            self.rect.x = x-50
            self.rect.y = y-50
        self.sonido_muerte = pygame.mixer.Sound("sonidos/alien_muerte.wav")

    # --- CAMBIO DE FRAME CON UN RETARDO DE 5 INCREMENTOS ---
    def get_frame(self, frame_set):
        self.retardo_frame += 1

        if self.retardo_frame == 4:
            self.frame += 1
            self.retardo_frame = 0
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
        
        # - Creo que carga el fragmento seleccionado de la imagen -
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    # -- ACTUALIZA ENEMIGO --
    def update(self, paredes, camara_x, camara_y, ventana, aliens, player, allsprites):
        if self.tipo == 0:
            if player.nivel == 1 or player.nivel == 2:
                if self.direccion == 0:
                    # -- Se mueve en vertical --
                    self.rect.y += self.speed_y
                    if self.vertical > 0:
                        self.animacion('abajo')
                    else:
                        self.animacion('arriba')
                    # -- Si colisiona con pared, rebota --
                    for pared in paredes[0]:
                        if pared[1].colliderect(self.rect):
                            self.speed_y *= -1
                            self.vertical *= -1
                else:
                    # -- Se mueve en Horizontal --
                    self.rect.x += self.speed_x
                    if self.horizontal > 0:
                        self.animacion('derecha')
                    else:
                        self.animacion('izquierda')
                    # -- Si colisiona con pared, rebota --
                    for pared in paredes[0]:
                        if pared[1].colliderect(self.rect):
                            self.speed_x *= -1
                            self.horizontal *= -1
            elif player.nivel == 3:
                self.speed_y = 1
                self.rect.y += self.speed_y
                self.animacion('abajo')
                if self.rect.y > 600:
                    self.kill()
                    aliens.remove(self)
                    player.oleada_aranias -= 1
                    player.vida -= 2
        elif self.tipo == 1:
            if player.nivel == 1 or player.nivel == 2:
                self.animacion('arriba')
                if self.rect.centerx < player.rect.centerx:
                    self.rect.x += self.speed_x
                else:
                    self.rect.x -= self.speed_x
                if self.rect.centery < player.rect.centery:
                    self.rect.y += self.speed_y
                else:
                    self.rect.y -= self.speed_y
            elif player.nivel == 3:
                self.speed_y = 2
                self.animacion('arriba')
                self.rect.y += self.speed_y
                if self.rect.y > 300:
                    if self.rect.centerx < player.rect.centerx:
                        self.rect.x += self.speed_x
                    else:
                        self.rect.x -= self.speed_x
                
                # -- Si colisiona con pared, rebota --
                for pared in paredes[0]:
                    if self.rect.colliderect(pared[1]):
                        self.speed_x *= -1
                if self.rect.y > 600:
                    self.kill()
                    aliens.remove(self)
                    player.vida -= 2

        elif self.tipo == 2:
            self.rect.x += self.speed_x
            if self.speed_x > 0:
                self.animacion('derecha')
            else:
                self.animacion('izquierda')
            # -- Si colisiona con pared, rebota --
            for pared in paredes[0]:
                if pared[1].collidepoint(self.rect.centerx, self.rect.centery):
                    self.speed_x *= -1
        # -- Pintar Enemigo --
        ventana.blit(self.image,(self.rect.x - camara_x, self.rect.y - camara_y))
# --- FUNCION CREAR A LOS ALIENS ---
def crear_aliens(allsprites, mapa, aliens, mas_respawn, nivel, player):
    if nivel == 1 or nivel == 2:
        ax, ay = 0, 0
        if mas_respawn:
            for fila in mapa:
                for columna in fila:
                    if columna == "N":
                        aliens.append(Enemigo(ax, ay, 1))
                    ax += 50
                ax = 0
                ay += 50
        else:
            for fila in mapa:
                for columna in fila:
                    if columna == "R":
                        aliens.append(Enemigo(ax, ay, 0))
                    if columna == "N":
                        aliens.append(Enemigo(ax, ay, 1))
                    if columna == "S":
                        aliens.append(Enemigo(ax, ay, 2))
                    ax += 50
                ax = 0
                ay += 50
    elif nivel == 3:
        for i in range(15):
            aliens.append(Enemigo(random.randint(150,600), random.randint(-700,-50), 0))
        player.oleada_aranias = 15
        player.oleada_aereos -= 1
        if player.oleada_aereos == 0:
            for i in range(20):
                aliens.append(Enemigo(random.randint(170,600), random.randint(-250,-10), 1))
            player.oleada_aereos = 2

    for alien in aliens:
        allsprites.add(alien)
    return aliens

def pintar_vida(ventana, x, y, vida, vida_total, BLANCO, VERDE, imagen):
    barra_ancho = 100
    barra_alto = 10
    llenar_barra = (vida/vida_total) * barra_ancho
    llenar_barra = pygame.Rect(x+112, y+9, llenar_barra, barra_alto)
    ventana.blit(imagen, (x, y))
    pygame.draw.rect(ventana, VERDE, llenar_barra)

def pintar_vida_final(ventana, x, y, vida, vida_total, VERDE, AMARILLO, ROJO):
    barra_ancho = 50
    barra_alto = 390
    llenar_barra = (vida/vida_total) * barra_alto
    llenar_barra = pygame.Rect(x, y, barra_ancho, -llenar_barra )
    if vida >= vida_total/2:
        COLOR = VERDE
    elif vida < vida_total/2 and vida >= vida_total/4:
        COLOR = AMARILLO
    elif vida < vida_total/4:
        COLOR = ROJO
    pygame.draw.rect(ventana, COLOR, llenar_barra)

############################## CLASE ENEMIGO FINAL ##############################
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.vida_total = 1000
        self.vida = self.vida_total
        self.tipo = 9
        self.contador = 0
        self.sheet = pygame.image.load('multimedia/boss.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(4, 10, 213, 212))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.frame = 0 
        self.retardo_frame = 0
        self.animar_movimiento = { 0: (4, 10, 213, 212), 1: (249, 10, 213, 212) }
        self.rect.x = x
        self.rect.y = y
        self.sonido_rugido = pygame.mixer.Sound("sonidos/boss_rugido.wav")
        self.sonido_muerte = pygame.mixer.Sound("sonidos/boss_muerte.wav")

    # --- CAMBIO DE FRAME CON UN RETARDO DE 5 INCREMENTOS ---
    def get_frame(self, frame_set):
        self.retardo_frame += 1

        if self.retardo_frame == 5:
            self.frame += 1
            self.retardo_frame = 0
        if self.frame > (len(frame_set) - 1):
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
    def animacion(self):
        # - Movimientos -
        self.clip(self.animar_movimiento)
        
        # - Creo que carga el fragmento seleccionado de la imagen -
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    # -- ACTUALIZA BOSS --
    def update(self, paredes, camara_x, camara_y, ventana, aliens, player, allsprites):
        self.animacion()
        # - Se dispara tras un contador de 150 -
        self.contador += 1
        if self.contador == 150:
            self.sonido_rugido.play()
            self.disparar(allsprites, self.rect.centerx, self.rect.centery, player.rect.centerx)
            # - Cuando el Boss tiene la mitad de la vida, dispara dos veces -
            if self.vida < self.vida_total / 2:
                self.disparar(allsprites, self.rect.centerx, self.rect.centery, 350)
            self.contador = 0
        ventana.blit(self.image,(self.rect.x - camara_x, self.rect.y - camara_y))
    
    # -- Al pulsar espacio se crea un disparo (Clase) --
    def disparar(self, allsprites, x, y, o_x):
        bullet = DisparoBoss(x, y, o_x)
        allsprites.add(bullet)

############################## CLASE DISPARO BOSS ##############################
class DisparoBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, o_x):
        super().__init__()
        self.image = pygame.image.load("multimedia/disparo_boss.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        # - Velocidad de disparo -
        self.speedy = 5
        self.speedx = 2
        # - Objetivo -
        self.objetivo_x = o_x

    # -- ACTUALIZA DISPARO --
    def update(self, paredes, camara_x, camara_y, ventana, aliens, player, allsprites):
        # -- Direccion del disparo segun donde esta el Jugador --
        self.rect.y += self.speedy
        if self.rect.x > self.objetivo_x:
            self.rect.x -= self.speedx
        elif self.rect.x < self.objetivo_x:
            self.rect.x += self.speedx
        else:
            self.rect.x = self.objetivo_x
        
        if self.rect.colliderect(player.rect):
            player.vida -= 5
            self.kill()
        if self.rect.y > 600:
            self.kill()
        

        # -- Pintar Disparo --
        ventana.blit(self.image,(self.rect.x - camara_x, self.rect.y - camara_y))
