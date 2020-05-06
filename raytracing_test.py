import pygame as pg
import math

tiles_x, tiles_y = 11, 11
tile_width, tile_height = 40, 40

tiles = [[0 for _ in range(tiles_y)] for _ in range(tiles_x)]
# 0 = hit by ray (white) (0,0,0)
# 1 = wall (red) (0,0,0)
# 2 = shadow (grey)
# 3 = shadowed wall (dark red)
WHITE = (255,255,255)
GREY = (100,100,100)
RED = (200,0,0)
D_RED = (100,0,0)
YELLOW = (200,200,0)

pg.init()

win = pg.display.set_mode((tiles_x * tile_width, tiles_y * tile_height))
pg.display.set_caption("Ray Tracing")

def redraw(light_pos):
	win.fill(WHITE)

	for x in range(tiles_x):
		for y in range(tiles_y):
			if tiles[x][y] == 1:
				pg.draw.rect(win, RED, (x * tile_width, y * tile_height, tile_width, tile_height))
			elif tiles[x][y] == 2:
				pg.draw.rect(win, GREY, (x * tile_width, y * tile_height, tile_width, tile_height))
			elif tiles[x][y] == 3:
				pg.draw.rect(win, D_RED, (x * tile_width, y * tile_height, tile_width, tile_height))

	x, y = light_pos
	pg.draw.circle(win, YELLOW, (int((x + 0.5) * tile_width), int((y + 0.5) * tile_height)), int(min(tile_width, tile_height) / 2), 5)
			
def ray_trace(x0, y0):
	for tile in tiles:
		if tile == 2:
			tile = 0
		elif tile == 3:
			tile = 1

	for x1 in range(tiles_x):
		for y1 in range(tiles_y):

			dx = abs(x1 - x0)
			dy = abs(y1 - y0)
			x = x0 + 0.5
			y = y0 + 0.5
			n = 1 + dx + dy
			x_inc = 1 if (x1 > x0) else -1
			y_inc = 1 if (y1 > y0) else -1
			error = dx - dy
			dx *= 2
			dy *= 2

			while n > 0:
				if tiles[math.floor(x)][math.floor(y)] == 1 and (math.floor(x), math.floor(y)) != (x1, y1):
					if tiles[x1][y1] == 1:
						tiles[x1][y1] = 3
					if tiles[x1][y1] == 0:
						tiles[x1][y1] = 2

					n = 0

				if (error > 0):
				    x += x_inc
				    error -= dy
				else:
					y += y_inc
					error += dx

				n -= 1

win.fill(WHITE)
redraw((5, 5))
pg.display.update()

clock = pg.time.Clock()
done = False

while not done:
	clock.tick(5)

	for event in pg.event.get():
	    if event.type == pg.QUIT:
	        done = True

	if pg.mouse.get_pressed()[0]:
		x, y = pg.mouse.get_pos()
		x, y = math.floor(x/tile_width), math.floor(y/tile_height)

		if tiles[x][y] == 1:
			tiles[x][y] = 0
		else:
			tiles[x][y] = 1

		ray_trace(5, 5)
		redraw((5, 5))
		pg.display.update()
