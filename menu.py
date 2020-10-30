import pygame

# ------------ CLASE MENU ----------------
class Menu():
    def __init__(self, game):
        self.game = game
        self.ANCHO_M, self.ALTO_M = self.game.ANCHO / 2, self.game.ALTO / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 130

    def pintar_cursor(self):
        self.game.pintar_cursor('T', 40, self.cursor_rect.x, self.cursor_rect.y)

    def pintar_pantalla(self):
        self.game.ventana.blit(self.game.ventana_atras, (0, 0))
        pygame.display.update()
        self.game.resetear_teclas()

# ------------- CLASE MENU PRINCIPAL ---------------
class MenuPrincipal(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.estado = "Inicio"
        self.continuarx, self.continuary = self.ANCHO_M, self.ALTO_M + 30
        self.iniciox, self.inicioy = self.ANCHO_M, self.ALTO_M + 70
        self.controlesx, self.controlesy = self.ANCHO_M, self.ALTO_M + 110
        self.creditosx, self.creditosy = self.ANCHO_M, self.ALTO_M + 150
        self.salirx, self.saliry = self.ANCHO_M, self.ALTO_M + 190
        self.cursor_rect.midtop = (self.iniciox + self.offset, self.inicioy)

    # ----------- METODO PARA MOSTRAR MENU SEGUN SI EL JUEGO YA FUE INICIADO ----------
    def display_menu(self):
        self.run_display = True
        if self.game.inicio:
            while self.run_display:
                self.game.chequear_eventos()
                self.chequear_ingreso()
                self.game.ventana_atras.blit(self.game.fondo_menu, (0,0))
                self.game.pintar_texto("Continuar", 20, self.continuarx, self.continuary)
                self.game.pintar_texto("Nuevo Juego", 20, self.iniciox, self.inicioy)
                self.game.pintar_texto("Controles", 20, self.controlesx, self.controlesy)
                self.game.pintar_texto("Creditos", 20, self.creditosx, self.creditosy)
                self.game.pintar_texto("Salir", 20, self.salirx, self.saliry)
                self.pintar_cursor()
                self.pintar_pantalla()
        else:
            while self.run_display:
                self.game.chequear_eventos()
                self.chequear_ingreso()
                self.game.ventana_atras.blit(self.game.fondo_menu, (0,0))
                self.game.pintar_texto("Nuevo Juego", 20, self.iniciox, self.inicioy)
                self.game.pintar_texto("Controles", 20, self.controlesx, self.controlesy)
                self.game.pintar_texto("Creditos", 20, self.creditosx, self.creditosy)
                self.game.pintar_texto("Salir", 20, self.salirx, self.saliry)
                self.pintar_cursor()
                self.pintar_pantalla()


    # ---------- MOVER EL "CURSOR" ENTRE LAS OPCIONES ---------------
    def mover_cursor(self):
        if self.game.TECLA_ABAJO:
            if self.game.inicio:
                if self.estado == 'Continuar':
                    self.cursor_rect.midtop = (self.iniciox + self.offset, self.inicioy)
                    self.estado = 'Inicio'
                elif self.estado == 'Inicio':
                    self.cursor_rect.midtop = (self.controlesx + self.offset, self.controlesy)
                    self.estado = 'Controles'
                elif self.estado == 'Controles':
                    self.cursor_rect.midtop = (self.creditosx + self.offset, self.creditosy)
                    self.estado = 'Creditos'
                elif self.estado == 'Creditos':
                    self.cursor_rect.midtop = (self.salirx + self.offset, self.saliry) 
                    self.estado = 'Salir'
                elif self.estado == 'Salir':
                    self.cursor_rect.midtop = (self.continuarx + self.offset, self.continuary)
                    self.estado = 'Continuar'
            else:
                if self.estado == 'Inicio':
                    self.cursor_rect.midtop = (self.controlesx + self.offset, self.controlesy)
                    self.estado = 'Controles'
                elif self.estado == 'Controles':
                    self.cursor_rect.midtop = (self.creditosx + self.offset, self.creditosy)
                    self.estado = 'Creditos'
                elif self.estado == 'Creditos':
                    self.cursor_rect.midtop = (self.salirx + self.offset, self.saliry) 
                    self.estado = 'Salir'
                elif self.estado == 'Salir':
                    self.cursor_rect.midtop = (self.iniciox + self.offset, self.inicioy)
                    self.estado = 'Inicio'

        elif self.game.TECLA_ARRIBA:
            if self.game.inicio:
                if self.estado == 'Continuar':
                    self.cursor_rect.midtop = (self.salirx + self.offset, self.saliry)
                    self.estado = 'Salir'
                elif self.estado == 'Inicio':
                    self.cursor_rect.midtop = (self.continuarx + self.offset, self.continuary)
                    self.estado = 'Continuar' 
                elif self.estado == 'Controles':
                    self.cursor_rect.midtop = (self.iniciox + self.offset, self.inicioy)
                    self.estado = 'Inicio'
                elif self.estado == 'Creditos':
                    self.cursor_rect.midtop = (self.controlesx + self.offset, self.controlesy)
                    self.estado = 'Controles'
                elif self.estado == 'Salir':
                    self.cursor_rect.midtop = (self.creditosx + self.offset, self.creditosy)
                    self.estado = 'Creditos'
                    
            else:
                if self.estado == 'Inicio':
                    self.cursor_rect.midtop = (self.salirx + self.offset, self.saliry)
                    self.estado = 'Salir' 
                elif self.estado == 'Controles':
                    self.cursor_rect.midtop = (self.iniciox + self.offset, self.inicioy)
                    self.estado = 'Inicio'
                elif self.estado == 'Creditos':
                    self.cursor_rect.midtop = (self.controlesx + self.offset, self.controlesy)
                    self.estado = 'Controles'
                elif self.estado == 'Salir':
                    self.cursor_rect.midtop = (self.creditosx + self.offset, self.creditosy)
                    self.estado = 'Creditos'

    # ---------- DETECTA QUE OPCION DE ELIJIO ----------------
    def chequear_ingreso(self):
        self.mover_cursor()
        if self.game.TECLA_ENTER:
            if self.estado == 'Continuar':
                self.game.jugar = True
            elif self.estado == 'Inicio':
                self.game.estado_menu = self.game.menu_niveles
            elif self.estado == 'Controles':
                self.game.estado_menu = self.game.menu_controles
            elif self.estado == 'Creditos':
                self.game.estado_menu = self.game.menu_creditos
            elif self.estado == 'Salir':
                self.game.jugar = False
                self.game.ejecucion = False
            self.run_display = False

# -------------- CLASE MENU PARA SELECCIONAR NIVEL ------------
class MenuNivel(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.estado = "Nivel 1"
        self.nivel1x, self.nivel1y = self.ANCHO_M, self.ALTO_M + 70
        self.nivel2x, self.nivel2y = self.ANCHO_M, self.ALTO_M + 110
        self.nivel3x, self.nivel3y = self.ANCHO_M, self.ALTO_M + 150
        self.cursor_rect.midtop = (self.nivel1x + self.offset, self.nivel1y)

    # --------- MUESTRA CONTENIDO DEL MENU ----------------
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.chequear_eventos()
            if self.game.TECLA_ATRAS:
                self.game.estado_menu = self.game.menu_principal
                self.run_display = False
            self.chequear_ingreso()
            self.game.ventana_atras.blit(self.game.fondo_menu, (0,0))
            self.game.pintar_texto("Nivel 1", 20, self.nivel1x, self.nivel1y)
            self.game.pintar_texto("Nivel 2", 20, self.nivel2x, self.nivel2y)
            self.game.pintar_texto("Nivel Final", 20, self.nivel3x, self.nivel3y)
            self.pintar_cursor()
            self.pintar_pantalla()

    # ---------- MOVER EL "CURSOR" ENTRE LAS OPCIONES ---------------
    def mover_cursor(self):
        if self.game.TECLA_ABAJO:
            if self.estado == 'Nivel 1':
                self.cursor_rect.midtop = (self.nivel2x + self.offset, self.nivel2y)
                self.estado = 'Nivel 2'
            elif self.estado == 'Nivel 2':
                self.cursor_rect.midtop = (self.nivel3x + self.offset, self.nivel3y)
                self.estado = 'Nivel 3'
            elif self.estado == 'Nivel 3':
                self.cursor_rect.midtop = (self.nivel1x + self.offset, self.nivel1y) 
                self.estado = 'Nivel 1'

        elif self.game.TECLA_ARRIBA:
            if self.estado == 'Nivel 1':
                self.cursor_rect.midtop = (self.nivel3x + self.offset, self.nivel3y)
                self.estado = 'Nivel 3' 
            elif self.estado == 'Nivel 2':
                self.cursor_rect.midtop = (self.nivel1x + self.offset, self.nivel1y)
                self.estado = 'Nivel 1'
            elif self.estado == 'Nivel 3':
                self.cursor_rect.midtop = (self.nivel2x + self.offset, self.nivel2y)
                self.estado = 'Nivel 2'

    # ---------- DETECTA QUE OPCION DE ELIJIO ----------------
    def chequear_ingreso(self):
        self.mover_cursor()
        if self.game.TECLA_ENTER:
            if self.estado == 'Nivel 1':
                self.game.seleccion = "Nivel 1"
                self.game.estado_menu = self.game.menu_datos
            elif self.estado == 'Nivel 2':
                self.game.seleccion = "Nivel 2"
                self.game.estado_menu = self.game.menu_datos
            elif self.estado == 'Nivel 3':
                self.game.seleccion = "Nivel 3"
                self.game.estado_menu = self.game.menu_datos
            self.run_display = False

# ------------ MENU DE CONTROLES ------------------
class MenuControles(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    # --------- MUESTRA CONTENIDO DEL MENU ----------------
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.chequear_eventos()
            if self.game.TECLA_ATRAS:
                self.game.estado_menu = self.game.menu_principal
                self.run_display = False
            self.game.ventana_atras.blit(self.game.fondo_controles, (0,0))
            self.pintar_pantalla()

# ----------- MENU DE CREDITOS -------------------
class MenuCreditos(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    # --------- MUESTRA CONTENIDO DEL MENU ----------------
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.chequear_eventos()
            if self.game.TECLA_ATRAS:
                self.game.estado_menu = self.game.menu_principal
                self.run_display = False
            self.game.ventana_atras.blit(self.game.fondo_creditos, (0,0))
            self.game.pintar_texto('Creditos', 30, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 250)
            self.game.pintar_texto('Braian Gomez', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 100)
            self.game.pintar_texto('Cristian Grageda', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 50)
            self.game.pintar_texto('Facundo Verrastro', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO)
            self.game.pintar_texto('Rodrigo Fernandez', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO + 50)
            self.game.pintar_texto('Thomas Galarza', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO + 100)
            self.pintar_pantalla()


# ------- MENU DE DATOS (Muestra mensajes cuando inicia nivel, cuando pierde, etc) ---------
class MenuDatos(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.fondo_nivel_uno = pygame.image.load("multimedia/nivel_uno.png").convert()
        self.fondo_nivel_dos = pygame.image.load("multimedia/nivel_dos.png").convert()
        self.fondo_nivel_tres = pygame.image.load("multimedia/nivel_tres.png").convert()
        self.fondo_logro = pygame.image.load("multimedia/logro.png").convert()
        self.fondo_derrota = pygame.image.load("multimedia/derrota.png").convert()

    # --------- MUESTRA CONTENIDO DEL MENU ----------------
    def display_menu(self):
        self.run_display = True
        # ---- MUESTRA MENSAJE ANTES DE INICIAR JUEGO ----
        if self.game.seleccion == "Nivel 1":
            while self.run_display:
                self.game.chequear_eventos()
                if self.game.TECLA_ENTER:
                    self.game.jugar = True
                    self.game.nivel = 1
                    self.game.nivel_uno()
                    self.run_display = False
                self.game.ventana_atras.blit(self.fondo_nivel_uno, (0,0))
                self.pintar_pantalla()
        elif self.game.seleccion == "Nivel 2":
            while self.run_display:
                self.game.chequear_eventos()
                if self.game.TECLA_ENTER:
                    self.game.jugar = True
                    self.game.nivel = 2
                    self.game.nivel_dos()
                    self.run_display = False
                self.game.ventana_atras.blit(self.fondo_nivel_dos, (0,0))
                self.pintar_pantalla()
        elif self.game.seleccion == "Nivel 3":
            while self.run_display:
                self.game.chequear_eventos()
                if self.game.TECLA_ENTER:
                    self.game.jugar = True
                    self.game.nivel = 3
                    self.game.nivel_uno()
                    self.run_display = False
                self.game.ventana_atras.blit(self.fondo_nivel_tres, (0,0))
                self.pintar_pantalla()
        # ---- MUESTRA MENSAJE CUANDO TERMINASTE EL NIVEL -----
        elif self.game.seleccion == "Logro":
            while self.run_display:
                self.game.chequear_eventos()
                if self.game.TECLA_ENTER:
                    if self.game.nivel == 1:
                        self.game.seleccion = "Nivel 2"
                        self.game.estado_menu = self.game.menu_datos
                    elif self.game.nivel == 2:
                        self.game.seleccion = "Nivel 3"
                        self.game.estado_menu = self.game.menu_datos
                    elif self.game.nivel == 3:
                        self.game.estado_menu = self.game.menu_creditos
                    self.run_display = False
                self.game.ventana_atras.blit(self.fondo_logro, (0,0))
                if self.game.nivel == 1:
                    self.game.pintar_texto('Felicidades', 30, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 200)
                    self.game.pintar_texto('Has logrado el completar el primer nivel', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO)
                    self.game.pintar_texto('Preparate para el segundo nivel', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO + 30)
                elif self.game.nivel == 2:
                    self.game.pintar_texto('Felicidades', 30, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 200)
                    self.game.pintar_texto('Has logrado el completar el segundo nivel', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO)
                    self.game.pintar_texto('Preparate para el nivel final', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO + 30)
                elif self.game.nivel == 3:
                    self.game.pintar_texto('Felicidades', 30, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 200)
                    self.game.pintar_texto('Has logrado terminar con la invasion alienigena', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO)
                    self.game.pintar_texto('Muchas gracias por jugar', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO + 30)
                    self.game.pintar_texto('Hasta la proxima', 20, self.game.MITAD_ANCHO, self.game.MITAD_ALTO + 60)
                self.pintar_pantalla()
        # ----- MUESTRA MENSAJE CUANDO SE PIERDE LA PARTIDA -----
        elif self.game.seleccion == "Derrota":
            while self.run_display:
                self.game.chequear_eventos()
                if self.game.TECLA_ENTER:
                    self.game.estado_menu = self.game.menu_principal
                    self.run_display = False
                self.game.ventana_atras.blit(self.fondo_derrota, (0,0))
                self.game.pintar_texto('No has logrado vencer', 30, self.game.MITAD_ANCHO, self.game.MITAD_ALTO - 200)
                self.pintar_pantalla()