"""
Developer - He1TPOH (Vlad Nikulin) Belarus;
This project is being developed by one developer.
This project will be developed further, but sinc I am alone, updates may not come out quickly.
The quality of the code wants to leave the best, but since my experience in programming is not great,
less than year, the quality corresponds, but as my skills grow, the quality will improve.
Version - 1.0.1
"""

import pygame as pg
pg.init()

points = list()
colors = list()
type_grp = list()

def crt_win(kol_vo_x, kol_vo_y, squre_block):
	global RES, sc, WIDTH, HEIGHT
	RES = WIDTH, HEIGHT = (kol_vo_x + 3) * squre_block, (kol_vo_y + 3) * squre_block
	sc = pg.display.set_mode(RES)
	pg.display.set_caption('Graphics  creator')

def gc_init(x_koeficent: int or float, y_koeficent: int or float, kol_vo_x: int, kol_vo_y: int, squre_block: int):
	global x_kof, y_kof, KOLVO_X, KOLVO_Y, SQURE
	x_kof, y_kof = x_koeficent, y_koeficent
	KOLVO_X, KOLVO_Y = kol_vo_x, kol_vo_y
	SQURE = squre_block
	crt_win(KOLVO_X, KOLVO_Y, SQURE)

def crt_line(point: list, color):
	points.append(point)
	colors.append(color)
	type_grp.append("line")

def crt_fline(point: list, color):
	points.append(point)
	colors.append(color)
	type_grp.append("fline")

def crt_pillar(point: list, color):
	points.append(point)
	colors.append(color)
	type_grp.append("pillar")

def crt_pwl(point: list, color: list or tuple):
	points.append(point)
	colors.append(color)
	type_grp.append("pwl")

def gc_draw():
	font = pg.font.SysFont('Calibri', int(SQURE // 2.77))
	clock = pg.time.Clock()
	while True:
		sc.fill((0, 0, 0))
		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit()

		x = SQURE * 2
		for run in range(((WIDTH // SQURE) - 4) + 1):
			pg.draw.line(sc, (255, 255, 255), (x, SQURE), (x, HEIGHT - SQURE))
			x += SQURE

		y = SQURE * 2
		for run in range(((HEIGHT // SQURE) - 4) + 1):
			pg.draw.line(sc, (255, 255, 255), (SQURE, y), (WIDTH - SQURE, y))
			y += SQURE
		
		for run in range(len(points)):
			if type_grp[run] == "line":
				for index in range(0, len(points[run]) - 1):
					x1 = int(SQURE * (index + 1)) + SQURE
					y1 = HEIGHT - int(SQURE / y_kof * points[run][index]) - SQURE
					x2 = int(SQURE * (index + 2)) + SQURE
					y2 = HEIGHT - int(SQURE / y_kof * points[run][index + 1]) - SQURE
					pg.draw.line(sc, colors[run], (x1, y1), (x2, y2), SQURE // 15)

				for index in range(len(points[run])):
					x = int(SQURE * (index + 1)) + SQURE
					y = int(HEIGHT - SQURE // y_kof * points[run][index] - SQURE)
					pg.draw.circle(sc, colors[run], (x, y), SQURE // 10)

			elif type_grp[run] == "pillar":
				for index in range(len(points[run])):
					x = int((SQURE * (index + 1)) - (SQURE // 2) + (SQURE // 10)) + SQURE
					y = HEIGHT - int(SQURE / y_kof * points[run][index]) - SQURE
					x_size = int(SQURE - (SQURE // 10 * 2))
					y_size = int((HEIGHT - SQURE) - y)
					pg.draw.rect(sc, colors[run], (x, y, x_size, y_size))
					
			elif type_grp[run] == "fline":
				for index in range(0, len(points[run]) - 1):
					x1 = int(SQURE / x_kof * points[run][index][0]) + SQURE
					y1 = HEIGHT - int(SQURE / y_kof * points[run][index][1]) - SQURE
					x2 = int(SQURE / x_kof * points[run][index + 1][0]) + SQURE
					y2 = HEIGHT - int(SQURE / y_kof * points[run][index + 1][1]) - SQURE
					pg.draw.line(sc, colors[run], (x1, y1), (x2, y2), SQURE // 15)

				for index in range(len(points[run])):
					x = int(SQURE / x_kof * points[run][index][0]) + SQURE
					y = HEIGHT - int(SQURE / y_kof * points[run][index][1]) - SQURE
					pg.draw.circle(sc, colors[run], (x, y), SQURE // 10)

			elif type_grp[run] == "pwl":
				for index in range(len(points[run])):
					x = int((SQURE * (index + 1)) - (SQURE // 2) + (SQURE // 10)) + SQURE
					y = HEIGHT - int(SQURE / y_kof * points[run][index]) - SQURE
					x_size = int(SQURE - (SQURE // 10 * 2))
					y_size = int((HEIGHT - SQURE) - y)
					pg.draw.rect(sc, colors[run][0], (x, y, x_size, y_size))

				for index in range(0, len(points[run]) - 1):
					x1 = int(SQURE * (index + 1)) + SQURE
					y1 = HEIGHT - int(SQURE / y_kof * points[run][index]) - SQURE
					x2 = int(SQURE * (index + 2)) + SQURE
					y2 = HEIGHT - int(SQURE / y_kof * points[run][index + 1]) - SQURE
					pg.draw.line(sc, colors[run][1], (x1, y1), (x2, y2), SQURE // 15)

				for index in range(len(points[run])):
					x = int(SQURE * (index + 1)) + SQURE
					y = int(HEIGHT - SQURE // y_kof * points[run][index] - SQURE)
					pg.draw.circle(sc, colors[run][1], (x, y), SQURE // 10)

		pg.draw.rect(sc, (0, 0, 0), (0, 0, WIDTH, SQURE))
		pg.draw.rect(sc, (0, 0, 0), (0, 0, SQURE, HEIGHT))
		pg.draw.rect(sc, (0, 0, 0), (WIDTH - SQURE, 0, SQURE, HEIGHT))
		pg.draw.rect(sc, (0, 0, 0), (0, HEIGHT - SQURE, WIDTH, SQURE))

		pg.draw.line(sc, (255, 255, 255), (SQURE, SQURE), (WIDTH - SQURE, SQURE), 3)
		pg.draw.line(sc, (255, 255, 255), (SQURE, SQURE), (SQURE, HEIGHT - SQURE), 3)
		pg.draw.line(sc, (255, 255, 255), (WIDTH - SQURE, SQURE), (WIDTH - SQURE, HEIGHT - SQURE), 3)
		pg.draw.line(sc, (255, 255, 255), (SQURE, HEIGHT - SQURE), (WIDTH - SQURE, HEIGHT - SQURE), 3)

		zero = font.render("0", 5, (255, 255, 255))
		sc.blit(zero, (SQURE - SQURE // 3, HEIGHT - 35))

		x_text = font.render("X", 5, (255, 255, 255))
		y_text = font.render("Y", 5, (255, 255, 255))
		sc.blit(y_text, (SQURE - SQURE // 4, SQURE - SQURE // 8))
		sc.blit(x_text, (WIDTH - SQURE, HEIGHT - SQURE + SQURE // 10))

		x_k = x_kof
		x = SQURE * 2
		for run in range(((WIDTH // SQURE) - 4) + 1):
			text = font.render("%.2f" % x_k, 5, (255, 255, 255))
			sc.blit(text, (x - SQURE + SQURE // 1.5, HEIGHT - SQURE + SQURE // 10))
			x_k += x_kof
			x += SQURE

		y_k = y_kof
		y = SQURE * 2
		for run in range(((HEIGHT // SQURE) - 4) + 1):
			text = font.render("%.2f" % y_k, 5, (255, 255, 255))
			sc.blit(text, (SQURE // 10, (HEIGHT - y) - 10))
			y_k += y_kof
			y += SQURE

		pg.display.update()
		clock.tick(4)