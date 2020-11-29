import pygame
from menu import *
from metodos_clases import *
from camara import *


class Game():
    def __init__(self):
        pygame.init()
        # -- JUEGO EN EJECUCION, COMENZAR A JUGAR, JUEGO YA INICIALIZADO(para manejar el pause) --
        self.ejecucion, self.jugar, self.inicio = True, False, False
        self.nivel = 1
        # -- VARIABLES PARA INTERACTUAR CON EL MENU --
        self.TECLA_ARRIBA, self.TECLA_ABAJO, self.TECLA_ENTER, self.TECLA_ATRAS = False, False, False, False
        self.ANCHO, self.ALTO = 800, 600
        # -- SUPERFICIE PARA PINTAR EL JUEGO Y VENTANA PARA PROYECCION FINAL --
        self.ventana_atras = pygame.Surface((self.ANCHO, self.ALTO))
        self.ventana = pygame.display.set_mode(((self.ANCHO, self.ALTO)))
        # -- FUENTES DE LETRAS --
        self.fuente_1 = 'fuentes/Super Retro M54.ttf'
        self.fuente_2 = 'fuentes/Target Shooting.otf'
        self.fuente_3 = 'fuentes/Open 24 Display St.ttf'
        # -- SONIDOS E IMAGENES DEL MENU --
        self.sonido_cursor = pygame.mixer.Sound("sonidos/cursor_menu.wav")
        self.sonido_seleccion = pygame.mixer.Sound("sonidos/seleccion_menu.wav")
        self.sonido_deseleccion = pygame.mixer.Sound("sonidos/deseleccion_menu.wav")
        self.fondo_controles = pygame.image.load("multimedia/controles.png").convert()
        self.fondo_menu = pygame.image.load("multimedia/menu_principal.png").convert()
        self.fondo_creditos = pygame.image.load("multimedia/creditos.png").convert()
        self.vida_jugador = pygame.image.load("multimedia/vida_soldado.png").convert_alpha()
        # -- COLORES Y MITAD DE VENTANA --
        self.NEGRO, self.BLANCO, self.VERDE = (0, 0, 0), (255, 255, 255), (0, 125, 15)
        self.MITAD_ANCHO = self.ANCHO/2
        self.MITAD_ALTO = self.ALTO/2
        # -- CREACION DE LOS MENUS --
        self.menu_principal = MenuPrincipal(self)
        self.menu_niveles = MenuNivel(self)
        self.menu_controles = MenuControles(self)
        self.menu_creditos = MenuCreditos(self)
        self.menu_datos = MenuDatos(self)
        # -- ASIGNA ESTADO DEL MENU PARA SABER EN CUAL MENU ESTAR --
        self.estado_menu = self.menu_principal
        self.seleccion = "Nada" # Selecciona opcion de "Menu de datos" 
        self.reloj = pygame.time.Clock() # Crea Reloj

        
        
    def nivel_uno(self):
        # --- CARGA DE IMAGENES PARA MAPA ---
        self.muro = pygame.image.load("multimedia/muro.png").convert()
        self.muro_roto = pygame.image.load("multimedia/muro_roto.png").convert()
        self.item = pygame.image.load("multimedia/item.png").convert_alpha()
        self.pozo = pygame.image.load("multimedia/pozo.png").convert_alpha()
        self.botiquin = pygame.image.load("multimedia/botiquin.png").convert_alpha()
        self.mancha = pygame.image.load("multimedia/mancha.png").convert_alpha()
        # --- MAPA ---
        self.crear_mapa = [
            "MMMMMMMMMNMMMMMMMMMMMMMMMMMNMMMM",
            "M                 MI           M",
            "MR    R      R    M       R   RM",
            "M    M    R       M  R         M",
            "MI  RM            MNMM         M",
            "MMMMMM            M            M",
            "M                 M            M",
            "MR           MMMMMMR  I        M",
            "MI MR             MMMMMMMMM    N",
            "M                RMI  B  IM    M",
            "MR                M       M    M",
            "NMMMMMMMMMMMMR    MR     RM R  M",
            "M      I   BN     M       M    M",
            "MR      R   M     M       M    M",
            "M  M        M     M   R   M    M",
            "M  MR       M     M       M    M",
            "MIRM        M     M       M    M",
            "MMMM  R     M     MR     RM    M",
            "M           M     M       M    M",
            "MI         RM     M       MR   M",
            "MR          M     M     R N    M",
            "M  M           R               M",
            "MB M R                        IM",
            "MMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMM"
        ]

        # --- CREACION DE DATOS NECESARIOS ---
        self.player = Player(self.MITAD_ANCHO, self.MITAD_ALTO, self.nivel) # Crea Jugador
        self.camara = Camara(self.player) # Crea Camara y sus movimientos
        self.camara_seguir = Seguir(self.camara,self.player)
        self.camara_limitada = Limite(self.camara,self.player)
        self.camara.cambiar_modo(self.camara_seguir)
        self.fondo = Fondo(self.camara, self.camara_seguir, self.camara_limitada, self.nivel) # Crea Fondo
        # --- CREAMOS EL MAPA ---
        self.mapa = construir_mapa(self.crear_mapa, self.muro, self.muro_roto, self.item, self.pozo, self.botiquin, self.mancha, self.player)
        # --- AGREGA SPRITES NECESARIOS ---
        self.all_sprites = pygame.sprite.Group()
        self.aliens = []
        self.aliens = crear_aliens(self.all_sprites, self.crear_mapa, self.aliens, self.player.mas_respawn)
    
    def nivel_dos(self):
        self.nivel_uno()
        # --- MAPA ---
        self.crear_mapa = [
            "MMMMMMMMMMMMNMMMMMMMMMMMMMMMMMMMMMNMMMMM",
            "MI          M          IM              M",
            "M  R     R  M  R        MR            RN",
            "M           MMS         M     R    M   M",
            "MB          M          RMB         M   M",
            "M                       MMS       RM   M",
            "M                   R   M          N   N",
            "NMMMMMMMMMM   MMMMMMMMMMMMMMMMMM   MR  M",
            "M                       M          M   M",
            "MR               R      MMS  R     M R M",
            "M    M                            RM   M",
            "MB I MMS                           M   M",
            "MMMMMMMMMMMMMMMMMMMMMMMMMMMNMMMMMMMMB RM",
            "M                                      M",
            "M R     S      R     I S   R           M",
            "M   MMMMMMMMMMMNMMMMMMMMMMMMMNMMMMMMMMMN",
            "M                    BM               IM",
            "N      R    R         M  R    R    B  RM",
            "M           S   R     M   MMMMMMMMMMMMMM",
            "M                   RIM                M",
            "M   MMMMMNMMMMMMMMMMMMMMSR            RM",
            "M                                     IM",
            "MR    S        R            R  S       M",
            "NMMMMMMNMMMMMMMM    NMMMMMMMMMMMM   MMMN",
            "MB             M    M                  M",
            "MI      R      M    MR                RM",
            "MR             M RR M        R         M",
            "M                   NMS              S N",
            "MR                  MMMMMMMM     MMMMMMM",
            "M              M    M       R   R      M",
            "MIS     R     MM   BMS        I      B M",
            "MMMMMMMMNMMMMMMNMMMMMMMMMMMMMMMMMMNMMMMN"
        ]
        # --- CREAMOS EL MAPA ---
        self.mapa = construir_mapa(self.crear_mapa, self.muro, self.muro_roto, self.item, self.pozo, self.botiquin, self.mancha, self.player)
        # --- AGREGA SPRITES NECESARIOS ---
        self.all_sprites = pygame.sprite.Group()
        self.aliens = []
        self.aliens = crear_aliens(self.all_sprites, self.crear_mapa, self.aliens, self.player.mas_respawn)
    
    """def nivel_final(self):
        self.player = Player(self.MITAD_ANCHO, self.MITAD_ALTO, self.nivel) # Crea Jugador
        pass"""


    def bucle_juego(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonidos/fondo1.mp3")
        # -- AL EMPEZAR A JUGAR SE DECLARA EL JUEGO COMO "INICIALIZADO" --
        if self.jugar:
            self.inicio = True
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()
        while self.jugar:
            teclado = pygame.key.get_pressed()
            for event in pygame.event.get():
                # -- CERRAR EL JUEGO AL CERRAR VENTANA --
                if event.type == pygame.QUIT:
                    pygame.quit()
                # -- IR AL MENU AL PRESIONAR ESC --
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.jugar = False
                    self.estado_menu = self.menu_principal
                    pygame.mixer.music.stop()
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
            self.player.update(self.mapa, self.all_sprites, self.camara, self.aliens)
            self.camara.scroll()
            
            # --- CUANDO SE RECOGEN 4, 8 Y 9 ITEMS APARECEN MAS ALIENS AEREOS ---
            if (self.player.items == 6 or self.player.items == 3 or self.player.items == 2) and self.player.mas_respawn:
                self.aliens = crear_aliens(self.all_sprites, self.crear_mapa, self.aliens, self.player.mas_respawn)
                self.player.mas_respawn = False
            
            
            # --- Pintamos en la ventana ---
            self.fondo.update(self.ventana_atras, self.camara.offset.x, self.camara.offset.y)
            pintar_mapa(self.ventana_atras, self.mapa, self.camara.offset.x, self.camara.offset.y)
            self.all_sprites.update(self.mapa, self.camara, self.ventana_atras, self.aliens, self.player)
            self.ventana_atras.blit(self.player.image, (self.player.rect.x - self.camara.offset.x, self.player.rect.y - self.camara.offset.y))
            pintar_vida(self.ventana_atras, 0, 531, self.player.vida, self.BLANCO, self.VERDE, self.vida_jugador)
            self.pintar_record("A L I E N S : ", 18, 650, 553, self.player.alien_muertos)
            self.pintar_record("I T E M S : ", 18, 650, 569, self.player.items)
            self.ventana.blit(self.ventana_atras, (0,0))

            # --- Actualiza ventana ---
            pygame.display.flip()

            # --- FPS ---
            self.reloj.tick(50)
            self.resetear_teclas()

            # --- SI EL JUGADOR SE QUEDA SIN VIDA, MUESTRA MENSAJE DE DERROTA ---
            if self.player.vida <= 0:
                self.inicio = False
                self.jugar = False
                self.seleccion = "Derrota"
                self.estado_menu = self.menu_datos
                pygame.mixer.music.stop()
            
            # --- SI EL JUGADOR RECOGE TODOS LOS ITEMS Y MATA A TODOS, GANA ---
            if self.player.items == 0 and self.player.alien_muertos == 0:
                self.inicio = False
                self.jugar = False
                self.seleccion = "Logro"
                self.estado_menu = self.menu_datos
                pygame.mixer.music.stop()


    # ---- DETECTA LAS OPCIONES SELECCIONADAS EN LOS MENU ----
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
                    self.sonido_deseleccion.play()
                    self.TECLA_ATRAS = True
                if event.key == pygame.K_DOWN:
                    self.sonido_cursor.play()
                    self.TECLA_ABAJO = True
                if event.key == pygame.K_UP:
                    self.sonido_cursor.play()
                    self.TECLA_ARRIBA = True
                    
    # ---- RESETEA LAS TECLAS EN LOS MENU ----
    def resetear_teclas(self):
        self.TECLA_ARRIBA, self.TECLA_ABAJO, self.TECLA_ENTER, self.TECLA_ATRAS = False, False, False, False

    # ---- PINTA LOS TEXTOS DE LOS MENUS
    def pintar_texto(self, texto, tamanio, x, y ):
        fuente = pygame.font.Font(self.fuente_1, tamanio)
        texto_superficie = fuente.render(texto, True, self.BLANCO)
        texto_rect = texto_superficie.get_rect()
        texto_rect.center = (x,y)
        self.ventana_atras.blit(texto_superficie,texto_rect)
    
    # ---- PINTA EL "CURSOR" PARA SELECCIONAR OPCIONES EN EL MENU ----
    def pintar_cursor(self, texto, tamanio, x, y ):
        fuente = pygame.font.Font(self.fuente_2, tamanio)
        texto_superficie = fuente.render(texto, True, self.BLANCO)
        texto_rect = texto_superficie.get_rect()
        texto_rect.center = (x,y)
        self.ventana_atras.blit(texto_superficie,texto_rect)

    # ---- PINTA LOS PUNTOS QUE FALTAN PARA EL PROXIMO NIVEL ----
    def pintar_record(self, texto, tamanio, x, y, puntos):
        texto = texto + str(puntos)
        fuente = pygame.font.Font(self.fuente_3, tamanio)
        texto_superficie = fuente.render(texto, True, self.BLANCO)
        texto_rect = texto_superficie.get_rect()
        texto_rect.center = (x,y)
        self.ventana_atras.blit(texto_superficie,texto_rect)



