from typing import Generator, Generic, TypeVar


T = TypeVar("T")
TileData = tuple[T, int, int]

class TileMap(Generic[T]):
	"""
	A two dimensional grid of a generic type.
	"""

	def __init__(self, state: list[list[T]]) -> None:
		self.state = state
	
	def get_at(self, x: int, y: int) -> T:
		"""
		Return the value at the given x and y coordinates.
		"""

		return self.state[y][x]

	def walk(self) -> Generator[TileData, None, None]:
		"""
		Generate a complete enumeration of the map's state.

		Starts in the top left (x=0, y=0), goes left to right, then up-to-down.
		"""

		for y, row in enumerate(self.state):
			for x, value in enumerate(row):
				yield (value, x, y)
	
	def contains_coords(self, x: int, y: int) -> bool:
		return (
			y in range(len(self.state))
			and x in range(len(self.state[y]))
		)
	
	def print(self) -> None:
		for row in self.state:
			print("".join(str(c) for c in row))
		print()

	def get_adjacent_4(self, x: int, y: int) -> Generator[TileData, None, None]:
		"""
		Generate an enumeration of the tiles directly adjacent to x and y.
		"""

		modifiers = [
			(0, -1),
			(-1, 0),
			(1, 0),
			(0, 1),
		]

		for modifier in modifiers:
			adj_x = x + modifier[0]
			adj_y = y + modifier[1]

			if not self.contains_coords(adj_x, adj_y):
				continue
				
			yield (
				self.state[adj_y][adj_x],
				adj_x,
				adj_y
			)
