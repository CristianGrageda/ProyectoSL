import pygame
from menu import *
from metodos_clases import *
from camara import *


class Game():
    def __init__(self):
        pygame.init()
        self.ejecucion, self.jugar = True, False
        self.TECLA_ARRIBA, self.TECLA_ABAJO, self.TECLA_ENTER, self.TECLA_ATRAS = False, False, False, False
        self.ANCHO, self.ALTO = 800, 600
        self.ventana_atras = pygame.Surface((self.ANCHO, self.ALTO))
        self.ventana = pygame.display.set_mode(((self.ANCHO, self.ALTO)))
        self.fuente_1 = 'fuentes/Super Retro M54.ttf'
        self.fuente_2 = 'fuentes/Target Shooting.otf'
        self.sonido_cursor = pygame.mixer.Sound("sonidos/cursor_menu.wav")
        self.sonido_seleccion = pygame.mixer.Sound("sonidos/seleccion_menu.wav")
        self.fondo_controles = pygame.image.load("multimedia/controles.png").convert()
        self.fondo_menu = pygame.image.load("multimedia/menu_principal.png").convert()
        self.fondo_creditos = pygame.image.load("multimedia/creditos.png").convert()
        #self.font_name = pygame.font.get_default_font()
        self.NEGRO, self.BLANCO = (0, 0, 0), (255, 255, 255)
        self.menu_principal = MenuPrincipal(self)
        self.menu_controles = MenuControles(self)
        self.menu_creditos = MenuCreditos(self)
        self.estado_menu = self.menu_principal
        self.MITAD_ANCHO = self.ANCHO/2
        self.MITAD_ALTO = self.ALTO/2
        # --- MAPA ---
        """
        Para crear muros de 50x50 debe ser de:
        32 columnas <-- (Ancho de imagen)1600/50
        24 filas <-- (Alto de images)1200/50
        """
        self.mapa_1 = [
            "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
            "MR    R      R    MI          RM",
            "M                 M       R    M",
            "M    M    R       M  R         M",
            "MI   M            MMMM         M",
            "MMMMMM            M            M",
            "M                 M            M",
            "MR           MMMMMMR  I        M",
            "MI MR            RMMMMMMMMM    M",
            "M                 MI     IM    M",
            "MR                M       M    M",
            "MMMMMMMMMMMMMR    M      RM    M",
            "M           M     M       M    M",
            "M       R   M     M       M    M",
            "M  M        M     M   R   M    M",
            "M  MR       M     M       M    M",
            "MIRM        M     M       M    M",
            "MMMM        M     MR      M    M",
            "M           M     M       M    M",
            "M          RM     M       M    M",
            "MR          M     M     R M    M",
            "M              R               M",
            "M    R                        IM",
            "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
        ]

        # --- CARGA DE IMAGENES PARA MAPA ---
        self.muro = pygame.image.load("multimedia/muro.png")
        self.item = pygame.image.load("multimedia/item.png")
        self.pozo = pygame.image.load("multimedia/pozo.png")

        # --- CREACION DE DATOS NECESARIOS ---
        self.reloj = pygame.time.Clock() # Crea Reloj
        self.player = Player(self.MITAD_ANCHO, self.MITAD_ALTO) # Crea Jugador
        self.camara = Camara(self.player) # Crea Camara y sus movimientos
        self.camara_seguir = Seguir(self.camara,self.player)
        self.camara_limitada = Limite(self.camara,self.player)
        self.camara.cambiar_modo(self.camara_seguir)
        self.fondo = Fondo(self.camara, self.camara_seguir, self.camara_limitada) # Crea Fondo

        # --- CREAMOS EL MAPA ---
        self.nivel_1 = construir_mapa(self.mapa_1, self.muro, self.item, self.pozo)

        # --- AGREGA SPRITES NECESARIOS ---
        self.all_sprites = pygame.sprite.Group()
        self.aliens = crear_aliens(self.all_sprites, self.mapa_1)
    
    def resetear_juego(self):
        # --- MAPA ---
        self.mapa_1 = [
            "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
            "MR    R      R    MI          RM",
            "M                 M       R    M",
            "M    M    R       M  R         M",
            "MI   M            MMMM         M",
            "MMMMMM            M            M",
            "M                 M            M",
            "MR           MMMMMMR  I        M",
            "MI MR            RMMMMMMMMM    M",
            "M                 MI     IM    M",
            "MR                M       M    M",
            "MMMMMMMMMMMMMR    M      RM    M",
            "M           M     M       M    M",
            "M       R   M     M       M    M",
            "M  M        M     M   R   M    M",
            "M  MR       M     M       M    M",
            "MIRM        M     M       M    M",
            "MMMM        M     MR      M    M",
            "M           M     M       M    M",
            "M          RM     M       M    M",
            "MR          M     M     R M    M",
            "M              R               M",
            "M    R                        IM",
            "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
        ]

        # --- CARGA DE IMAGENES PARA MAPA ---
        self.muro = pygame.image.load("multimedia/muro.png")
        self.item = pygame.image.load("multimedia/item.png")
        self.pozo = pygame.image.load("multimedia/pozo.png")

        # --- CREACION DE DATOS NECESARIOS ---
        self.reloj = pygame.time.Clock() # Crea Reloj
        self.player = Player(self.MITAD_ANCHO, self.MITAD_ALTO) # Crea Jugador
        self.camara = Camara(self.player) # Crea Camara y sus movimientos
        self.camara_seguir = Seguir(self.camara,self.player)
        self.camara_limitada = Limite(self.camara,self.player)
        self.camara.cambiar_modo(self.camara_seguir)
        self.fondo = Fondo(self.camara, self.camara_seguir, self.camara_limitada) # Crea Fondo
        # --- CREAMOS EL MAPA ---
        self.nivel_1 = construir_mapa(self.mapa_1, self.muro, self.item, self.pozo)
        # --- AGREGA SPRITES NECESARIOS ---
        self.all_sprites = pygame.sprite.Group()
        self.aliens = crear_aliens(self.all_sprites, self.mapa_1)

    def bucle_juego(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonidos/fondo1.mp3")
        if self.jugar:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()
        while self.jugar:
            # --- SI SE CIERRA VENTANA O PRESIONA ESC, SE CIERRA EL JUEGO ---
            teclado = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.jugar = False
                    pygame.mixer.music.stop()
                    self.resetear_juego()
                # -- EVENTOS DE MOVIMIENTO DEL JUGADOR (JUGADOR QUIETO, DISPARO) --
                if event.type == pygame.KEYDOWN:     
                    if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and self.player.pulsado:
                        self.player.sonido_disparo.stop()
                        if self.player.posicion == 0:
                            self.player.disparar(self.all_sprites, self.player.rect.centerx-15, self.player.rect.centery)
                        elif self.player.posicion == 1:
                            self.player.disparar(self.all_sprites, self.player.rect.centerx+10, self.player.rect.centery)
                        elif self.player.posicion == 2:
                            self.player.disparar(self.all_sprites, self.player.rect.centerx, self.player.rect.centery+10)
                        elif self.player.posicion == 3:
                            self.player.disparar(self.all_sprites, self.player.rect.centerx, self.player.rect.centery+10)
                        self.player.sonido_disparo.play()
                        self.player.pulsado = False
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (teclado[pygame.K_RIGHT] == False and teclado[pygame.K_UP] == False and teclado[pygame.K_DOWN] == False):
                        self.player.animacion('quieto_izquierda')
                        self.player.posicion = 3
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (teclado[pygame.K_LEFT] == False and teclado[pygame.K_UP] == False and teclado[pygame.K_DOWN] == False):
                        self.player.animacion('quieto_derecha')
                        self.player.posicion = 2
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and (teclado[pygame.K_RIGHT] == False and teclado[pygame.K_LEFT] == False and teclado[pygame.K_DOWN] == False):
                        self.player.animacion('quieto_arriba')
                        self.player.posicion = 1
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (teclado[pygame.K_RIGHT] == False and teclado[pygame.K_UP] == False and teclado[pygame.K_LEFT] == False):
                        self.player.animacion('quieto_abajo')
                        self.player.posicion = 0 
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.player.pulsado = True
                
                # -- Cambiar modo de Camara
                self.fondo.modo_de_camara(event)
                    
            
            # --- Eventos de Player y Movimiento de Camara ---
            self.player.update(self.nivel_1, self.all_sprites, self.camara)
            self.camara.scroll()
            
            
            # --- Pintamos en la ventana ---
            self.fondo.update(self.ventana_atras, self.camara.offset.x, self.camara.offset.y)
            pintar_mapa(self.ventana_atras, self.nivel_1, self.camara.offset.x, self.camara.offset.y)
            self.all_sprites.update(self.nivel_1, self.camara, self.ventana_atras, self.aliens)
            self.ventana_atras.blit(self.player.image, (self.player.rect.x - self.camara.offset.x, self.player.rect.y - self.camara.offset.y))
            
            self.ventana.blit(self.ventana_atras, (0,0))

            # --- Actualiza ventana ---
            pygame.display.flip()

            # --- FPS ---
            self.reloj.tick(50)
            self.resetear_teclas()



    def chequear_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ejecucion, self.jugar = False, False
                self.estado_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.sonido_seleccion.play()
                    self.TECLA_ENTER = True
                if event.key == pygame.K_BACKSPACE:
                    self.TECLA_ATRAS = True
                if event.key == pygame.K_DOWN:
                    self.sonido_cursor.play()
                    self.TECLA_ABAJO = True
                if event.key == pygame.K_UP:
                    self.sonido_cursor.play()
                    self.TECLA_ARRIBA = True
                    

    def resetear_teclas(self):
        self.TECLA_ARRIBA, self.TECLA_ABAJO, self.TECLA_ENTER, self.TECLA_ATRAS = False, False, False, False

    def pintar_texto(self, texto, tamanio, x, y ):
        fuente = pygame.font.Font(self.fuente_1, tamanio)
        texto_superficie = fuente.render(texto, True, self.BLANCO)
        texto_rect = texto_superficie.get_rect()
        texto_rect.center = (x,y)
        self.ventana_atras.blit(texto_superficie,texto_rect)
    
    def pintar_cursor(self, texto, tamanio, x, y ):
        fuente = pygame.font.Font(self.fuente_2, tamanio)
        texto_superficie = fuente.render(texto, True, self.BLANCO)
        texto_rect = texto_superficie.get_rect()
        texto_rect.center = (x,y)
        self.ventana_atras.blit(texto_superficie,texto_rect)





