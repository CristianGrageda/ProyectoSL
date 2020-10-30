# --- MODULOS ---
from game import Game

g = Game()

while g.ejecucion:
	g.estado_menu.display_menu()
	g.bucle_juego()