from util.gol import GameOfLife
from util.parse import *


parse_input = map_func(list)

class CucumberMap(GameOfLife[str]):
	move_direction = "east" # or "south"
	in_gridlock = False

	def cur_value(self, x: int, y: int) -> str:
		return super().cur_value(
			x % self.x_size,
			y % self.y_size,
		)
	
	def new_value(
		self,
		x: int,
		y: int,
		current_value: str,
	) -> str:
		mover = ">" if self.move_direction == "east" else "v"

		if current_value == ".":
			space_to_check_for_mover = (
				(x-1, y) if self.move_direction == "east" else (x, y-1)
			)

			if self.cur_value(*space_to_check_for_mover) == mover:
				return mover

			else:
				return current_value
		
		elif current_value == mover:
			space_to_check_for_space = (
				(x+1, y) if self.move_direction == "east" else (x, y+1)
			)

			if self.cur_value(*space_to_check_for_space) == ".":
				return "."
			
			else:
				return current_value
		
		else:
			return current_value
		
	def step(self) -> None:
		prev_state = self.state

		self.move_direction = "east"
		super().step()
		self.t -= 1
		self.move_direction = "south"
		super().step()

		if self.state == prev_state:
			self.in_gridlock = True

def part1(cucumbers: list[list[str]]) -> int:
	cucumber_map = CucumberMap(cucumbers)
	cucumber_map.stepWhile(lambda cur_map: not cur_map.in_gridlock)

	return cucumber_map.t
