import collections
import copy

from util import tile_map
from util.parse import *


class OctopusMap(tile_map.TileMap[int]):
	flashes = 0
	last_flashers = set()
	steps = 0

	def step(self) -> None:
		self.steps += 1

		flash_queue = collections.deque()
		known_flashers = set()

		for value, x, y in self.walk():
			new_value = value + 1
			self.set_at(x, y, new_value)

			if new_value > 9:
				flash_queue.append((x, y))
				known_flashers.add((x, y))
		
		while len(flash_queue) > 0:
			flasher = flash_queue.popleft()
			self.flashes += 1

			for value, x, y in self.get_adjacent_8(*flasher):
				new_value = value + 1
				self.set_at(x, y, new_value)

				if new_value > 9 and (x, y) not in known_flashers:
					flash_queue.append((x, y))
					known_flashers.add((x, y))

		for x, y in known_flashers:
			self.set_at(x, y, 0)
		
		self.last_flashers = known_flashers
	
	def print(self) -> None:
		for y, row in enumerate(self.state):
			for x, value in enumerate(row):
				if (x, y) in self.last_flashers:
					print(f"\033[1m{value}\033[0m", end="")
				else:
					print(value, end="")
				
			print()
		print()


def parse_input(lines: list[str]) -> OctopusMap:
	return OctopusMap([
		[int(c) for c in line]
		for line in lines
	])

def part1(light_map: OctopusMap) -> int:
	for _i in range(100):
		light_map.step()
	
	return light_map.flashes

def part2(light_map: OctopusMap) -> int:
	while len(light_map.last_flashers) < (len(light_map.state) * len(light_map.state[0])):
		light_map.step()
	
	return light_map.steps
