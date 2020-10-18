# --- MODULOS ---
from game import Game

g = Game()

while g.ejecucion:
	g.estado_menu.display_menu()
	g.bucle_juego()

# LOS EVENTOS DE PLAYER Y CAMARA DEBEN FUNCIONAR -----


