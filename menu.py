import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.ANCHO_M, self.ALTO_M = self.game.ANCHO / 2, self.game.ALTO / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 120

    def pintar_cursor(self):
        self.game.pintar_cursor('T', 40, self.cursor_rect.x, self.cursor_rect.y)

    def pintar_pantalla(self):
        self.game.ventana.blit(self.game.ventana_atras, (0, 0))
        pygame.display.update()
        self.game.resetear_teclas()

class MenuPrincipal(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.estado = "Inicio"
        self.iniciox, self.inicioy = self.ANCHO_M, self.ALTO_M + 30
        self.controlesx, self.controlesy = self.ANCHO_M, self.ALTO_M + 70
        self.creditosx, self.creditosy = self.ANCHO_M, self.ALTO_M + 110
        self.salirx, self.saliry = self.ANCHO_M, self.ALTO_M + 150
        self.cursor_rect.midtop = (self.iniciox + self.offset, self.inicioy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.chequear_eventos()
            self.chequear_ingreso()
            self.game.ventana_atras.blit(self.game.fondo_menu, (0,0))
            self.game.pintar_texto("Iniciar Juego", 20, self.iniciox, self.inicioy)
            self.game.pintar_texto("Controles", 20, self.controlesx, self.controlesy)
            self.game.pintar_texto("Creditos", 20, self.creditosx, self.creditosy)
            self.game.pintar_texto("Salir", 20, self.salirx, self.saliry)
            self.pintar_cursor()
            self.pintar_pantalla()


    def mover_cursor(self):
        if self.game.TECLA_ABAJO:
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

    def chequear_ingreso(self):
        self.mover_cursor()
        if self.game.TECLA_ENTER:
            if self.estado == 'Inicio':
                self.game.jugar = True
            elif self.estado == 'Controles':
                self.game.estado_menu = self.game.menu_controles
            elif self.estado == 'Creditos':
                self.game.estado_menu = self.game.menu_creditos
            elif self.estado == 'Salir':
                self.game.jugar = False
                self.game.ejecucion = False
            self.run_display = False

class MenuControles(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.chequear_eventos()
            if self.game.TECLA_ENTER or self.game.TECLA_ATRAS:
                self.game.estado_menu = self.game.menu_principal
                self.run_display = False
            self.game.ventana_atras.blit(self.game.fondo_controles, (0,0))
            self.pintar_pantalla()


class MenuCreditos(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.chequear_eventos()
            if self.game.TECLA_ENTER or self.game.TECLA_ATRAS:
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








