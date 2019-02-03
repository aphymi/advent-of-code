from util.gol import GameOfLife
from util.parse import *

parse_input = map_func(map_func(lambda c: 1 if c == "#" else 0))

class Lights(GameOfLife):
	def new_value(self, x, y, cur):
		adj = sum(self.adj8(x, y))
		if (cur and adj in (2, 3)) or (not cur and adj == 3):
			return 1
		else:
			return 0

class StuckCornersLights(Lights):
	def __init__(self, *args):
		super().__init__(*args)
		self.corners = {(0, 0),
						(0, self.y_size-1),
						(self.x_size-1, 0),
						(self.x_size-1, self.y_size-1)}
	
	def cur_value(self, x, y):
		if (x, y) in self.corners:
			return 1
		else:
			return super().cur_value(x, y)


def part1(initial):
	lights = Lights(initial)
	lights.stepN(100)
	
	return lights.score()

def part2(initial):
	lights = StuckCornersLights(initial)
	lights.stepN(100)
	
	return lights.score()
