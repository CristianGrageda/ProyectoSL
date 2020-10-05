# --- MODULOS ---
import pygame
from metodos_clases import *
from camara import *

# --- INICIAMOS ---
pygame.init()

# --- CONSTANTES ---
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
ANCHO, ALTO = 800, 600
MITAD_ANCHO = ANCHO/2
MITAD_ALTO = ALTO/2

# --- CREAMOS SUPERFICIE Y VENTANA ---
ventana_atras = pygame.Surface((ANCHO, ALTO))
ventana = pygame.display.set_mode(((ANCHO, ALTO)))

# --- CARGA DE MUSICA --- (si las lineas 21 o 22 presentan errores, eliminarlas o comentarlas)
pygame.mixer.music.load("sonidos/fondo1.mp3")
pygame.mixer.music.play()

# --- MAPA ---
"""
Para crear muros de 50x50 debe ser de:
32 columnas <-- (Ancho de imagen)1600/50
24 filas <-- (Alto de images)1200/50
"""
mapa_1 = [
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "MR           R    MI          RM",
    "M                 M            M",
    "M    M            M  R         M",
    "MI   M            MMMM         M",
    "MMMMMM            M            M",
    "MR                M            M",
    "M                 M   I        M",
    "MI M              MMMMMMMMM    M",
    "M                 MI     IM    M",
    "MR                M       M    M",
    "MMMMMMMMMMMMM     M   R   M    M",
    "M           M     M       M    M",
    "M       R   M     M       M    M",
    "M  M        M     M       M    M",
    "M  M        M     M       M    M",
    "MI M        M     M       M    M",
    "MMMM        M     M       M    M",
    "M           M     M       M    M",
    "M           M     M       M    M",
    "M           M     M       M    M",
    "M              R               M",
    "M R                           IM",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
]

# --- CARGA DE IMAGENES PARA MAPA ---
muro = pygame.image.load("multimedia/muro.png")
item = pygame.image.load("multimedia/item.png")
pozo = pygame.image.load("multimedia/pozo.png")

# --- CREACION DE DATOS NECESARIOS ---
reloj = pygame.time.Clock() # Crea Reloj
player = Player(MITAD_ANCHO, MITAD_ALTO) # Crea Jugador
alien = Enemigo(50, 50) # Crea Enemigo
camara = Camara(player) # Crea Camara y sus movimientos
camara_seguir = Seguir(camara,player)
camara_limitada = Limite(camara,player)
camara.cambiar_modo(camara_seguir)
fondo = Fondo(camara, camara_seguir, camara_limitada) # Crea Fondo

# --- CREAMOS EL MAPA ---
nivel_1 = construir_mapa(mapa_1, muro, item, pozo)

# --- AGREGA SPRITES NECESARIOS ---
all_sprites = pygame.sprite.Group()
all_sprites.add(alien)

# --- ESTADO DEL JUEGO ---
juego = True

while juego:

    # --- SI SE CIERRA VENTANA O PRESIONA ESC, SE CIERRA EL JUEGO ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            juego = False


    # --- Eventos de Player y Movimiento de Camara ---
    fondo.modo_de_camara(event)
    player.update(event, nivel_1, all_sprites, camara)
    camara.scroll()
    
    
    # --- Pintamos en la ventana ---
    fondo.update(ventana_atras, camara.offset.x, camara.offset.y)
    pintar_mapa(ventana_atras, nivel_1, camara.offset.x, camara.offset.y)
    all_sprites.update(nivel_1, camara, ventana_atras)
    ventana_atras.blit(player.image, (player.rect.x - camara.offset.x, player.rect.y - camara.offset.y))
    
    ventana.blit(ventana_atras, (0,0))

    # --- Actualiza ventana ---
    pygame.display.flip()

    # --- FPS ---
    reloj.tick(50)

pygame.quit ()
